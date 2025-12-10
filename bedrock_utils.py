"""
Bedrock Utilities for DocSmart RAG System
AWS AI Engineer Nanodegree - Final Project

This module provides utility functions for interacting with Amazon Bedrock:
- query_knowledge_base: Retrieve relevant documents from Bedrock Knowledge Base
- generate_response: Generate responses using Bedrock LLM
- valid_prompt: Validate and categorize user prompts

Author: AWS AI Engineer Nanodegree Student
Course: Building GenAI Applications with Bedrock and Python
"""

import boto3
import json
import os
from typing import Dict, List, Optional, Any
from botocore.exceptions import ClientError

# ============================================================================
# Configuration
# ============================================================================

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "")
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

# Initialize Bedrock clients
bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)
bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

# ============================================================================
# Knowledge Base Query Function
# ============================================================================

def query_knowledge_base(
    query: str,
    knowledge_base_id: str = KNOWLEDGE_BASE_ID,
    max_results: int = 5,
    score_threshold: float = 0.1
) -> Dict[str, Any]:
    """
    Query the Bedrock Knowledge Base to retrieve relevant documents.
    
    This function uses the Bedrock Agent Runtime API to perform a similarity
    search against the knowledge base, retrieving the most relevant document
    chunks based on the user's query.
    
    Args:
        query (str): The user's search query
        knowledge_base_id (str): ID of the Bedrock Knowledge Base
        max_results (int): Maximum number of results to return (1-100)
        score_threshold (float): Minimum similarity score threshold (0.0-1.0)
        
    Returns:
        Dict containing:
            - 'results': List of retrieved documents with text and metadata
            - 'count': Number of results returned
            - 'query': Original query
            
    Example:
        >>> result = query_knowledge_base("¿Cuántos días de vacaciones tengo?")
        >>> print(f"Found {result['count']} relevant documents")
        >>> for doc in result['results']:
        ...     print(doc['text'])
    """
    try:
        # Input validation
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        if not knowledge_base_id:
            raise ValueError("Knowledge Base ID is required. Set KNOWLEDGE_BASE_ID environment variable.")
        
        if not 1 <= max_results <= 100:
            raise ValueError("max_results must be between 1 and 100")
        
        if not 0.0 <= score_threshold <= 1.0:
            raise ValueError("score_threshold must be between 0.0 and 1.0")
        
        # Call Bedrock Agent Runtime API to retrieve documents
        response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId=knowledge_base_id,
            retrievalQuery={
                'text': query.strip()
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': max_results,
                    'overrideSearchType': 'HYBRID'  # Use both semantic and keyword search
                }
            }
        )
        
        # Process and filter results based on score threshold
        results = []
        for item in response.get('retrievalResults', []):
            score = item.get('score', 0.0)
            
            # Only include results above threshold
            if score >= score_threshold:
                result_doc = {
                    'text': item['content']['text'],
                    'score': score,
                    'metadata': item.get('metadata', {}),
                    'location': item.get('location', {}),
                    'document_id': item.get('location', {}).get('s3Location', {}).get('uri', 'unknown')
                }
                results.append(result_doc)
        
        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'results': results,
            'count': len(results),
            'query': query,
            'knowledge_base_id': knowledge_base_id
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"AWS Error: {error_code} - {error_message}")
        
        return {
            'results': [],
            'count': 0,
            'query': query,
            'error': f"{error_code}: {error_message}"
        }
        
    except Exception as e:
        print(f"Error querying knowledge base: {e}")
        return {
            'results': [],
            'count': 0,
            'query': query,
            'error': str(e)
        }

# ============================================================================
# Response Generation Function
# ============================================================================

def generate_response(
    query: str,
    context_documents: List[Dict[str, Any]],
    model_id: str = LLM_MODEL_ID,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 1000
) -> Dict[str, Any]:
    """
    Generate a response using Bedrock LLM with retrieved context.
    
    This function takes the user's query and relevant documents from the
    knowledge base, constructs a prompt, and generates a contextual response
    using Claude 3.5 Sonnet.
    
    Args:
        query (str): The user's question
        context_documents (List[Dict]): Retrieved documents from knowledge base
        model_id (str): Bedrock model ID to use
        temperature (float): Controls randomness (0.0-1.0)
            - Lower values (0.0-0.3): More focused and deterministic
            - Medium values (0.4-0.7): Balanced creativity
            - Higher values (0.8-1.0): More creative and varied
        top_p (float): Nucleus sampling parameter (0.0-1.0)
            - Controls diversity of token selection
            - 0.9 = consider tokens with cumulative probability of 90%
        max_tokens (int): Maximum tokens in response
        
    Returns:
        Dict containing:
            - 'response': Generated text response
            - 'model_id': Model used
            - 'sources': List of source documents used
            - 'usage': Token usage statistics
            
    Example:
        >>> docs = query_knowledge_base("¿Cuántos días de vacaciones?")
        >>> response = generate_response(
        ...     query="¿Cuántos días de vacaciones tengo?",
        ...     context_documents=docs['results'],
        ...     temperature=0.3  # Lower for factual responses
        ... )
        >>> print(response['response'])
    """
    try:
        # Input validation
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        if not 0.0 <= temperature <= 1.0:
            raise ValueError("temperature must be between 0.0 and 1.0")
        
        if not 0.0 <= top_p <= 1.0:
            raise ValueError("top_p must be between 0.0 and 1.0")
        
        # Build context from retrieved documents
        context_text = ""
        sources = []
        
        if context_documents:
            context_text = "\n\n".join([
                f"Documento {i+1} (relevancia: {doc['score']:.2f}):\n{doc['text']}"
                for i, doc in enumerate(context_documents[:5])  # Limit to top 5
            ])
            
            sources = [
                {
                    'document_id': doc['document_id'],
                    'score': doc['score'],
                    'preview': doc['text'][:200] + '...' if len(doc['text']) > 200 else doc['text']
                }
                for doc in context_documents[:5]
            ]
        else:
            context_text = "No se encontraron documentos relevantes en la base de conocimientos."
        
        # Construct system prompt
        system_prompt = """Eres un asistente de recursos humanos especializado en responder preguntas sobre políticas de la empresa DocSmart.

Tu rol:
- Responder preguntas de manera clara, concisa y profesional en español
- Basar tus respuestas EXCLUSIVAMENTE en los documentos proporcionados
- Si la información no está en los documentos, indicarlo claramente
- Interpretar preguntas informales (ej: "cuánto me toca" = "cuántos días de vacaciones")
- Realizar cálculos cuando sea necesario (ej: días proporcionales por antigüedad)
- Mantener un tono amigable pero profesional

Importante:
- NO inventes información que no esté en los documentos
- Si no tienes suficiente información, admítelo
- Cita el documento específico cuando sea posible"""

        # Construct user prompt with context
        user_prompt = f"""<documentos_disponibles>
{context_text}
</documentos_disponibles>

<pregunta_empleado>
{query.strip()}
</pregunta_empleado>

Por favor, responde a la pregunta del empleado basándote en los documentos proporcionados. Si la pregunta es informal (como "cuánto me toca" o "estoy hace X tiempo"), interpreta su intención y calcula la respuesta apropiada según las políticas documentadas."""

        # Prepare request body for Claude
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        }
        
        # Call Bedrock Runtime API
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        
        # Extract generated text
        generated_text = response_body['content'][0]['text']
        
        # Extract usage statistics
        usage = {
            'input_tokens': response_body.get('usage', {}).get('input_tokens', 0),
            'output_tokens': response_body.get('usage', {}).get('output_tokens', 0),
            'total_tokens': response_body.get('usage', {}).get('input_tokens', 0) + 
                           response_body.get('usage', {}).get('output_tokens', 0)
        }
        
        return {
            'response': generated_text,
            'model_id': model_id,
            'sources': sources,
            'usage': usage,
            'parameters': {
                'temperature': temperature,
                'top_p': top_p,
                'max_tokens': max_tokens
            }
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"AWS Error: {error_code} - {error_message}")
        
        return {
            'response': f"Error generando respuesta: {error_message}",
            'model_id': model_id,
            'sources': [],
            'error': f"{error_code}: {error_message}"
        }
        
    except Exception as e:
        print(f"Error generating response: {e}")
        return {
            'response': f"Error inesperado: {str(e)}",
            'model_id': model_id,
            'sources': [],
            'error': str(e)
        }

# ============================================================================
# Prompt Validation Function
# ============================================================================

def valid_prompt(user_prompt: str) -> Dict[str, Any]:
    """
    Validate and categorize user prompts for safety and appropriate handling.
    
    This function analyzes user input to:
    1. Check for harmful, inappropriate, or irrelevant content
    2. Categorize the prompt type (HR policy, vacation, benefits, etc.)
    3. Extract key entities (dates, numbers, departments)
    4. Provide recommendations for handling
    
    Args:
        user_prompt (str): The user's input prompt
        
    Returns:
        Dict containing:
            - 'is_valid': Boolean indicating if prompt is acceptable
            - 'category': Prompt category (hr_policy, vacation, benefits, general, inappropriate)
            - 'confidence': Confidence score (0.0-1.0)
            - 'entities': Extracted entities (dates, numbers, keywords)
            - 'recommendation': How to handle the prompt
            - 'reason': Explanation of validation decision
            
    Example:
        >>> result = valid_prompt("¿Cuántos días de vacaciones tengo después de 1 año?")
        >>> print(f"Valid: {result['is_valid']}, Category: {result['category']}")
        Valid: True, Category: vacation
    """
    try:
        # Input validation
        if not user_prompt or not user_prompt.strip():
            return {
                'is_valid': False,
                'category': 'empty',
                'confidence': 1.0,
                'entities': {},
                'recommendation': 'reject',
                'reason': 'El prompt está vacío'
            }
        
        prompt_lower = user_prompt.lower().strip()
        
        # Check length
        if len(user_prompt) > 1000:
            return {
                'is_valid': False,
                'category': 'too_long',
                'confidence': 1.0,
                'entities': {},
                'recommendation': 'reject',
                'reason': 'El prompt es demasiado largo (máximo 1000 caracteres)'
            }
        
        # Define inappropriate content patterns
        inappropriate_patterns = [
            'hack', 'exploit', 'bypass', 'jailbreak',
            'ignore previous', 'ignore instructions',
            'violence', 'violent', 'violento',
            'illegal', 'ilegal',
            'discriminat', 'racist', 'sexist'
        ]
        
        # Check for inappropriate content
        for pattern in inappropriate_patterns:
            if pattern in prompt_lower:
                return {
                    'is_valid': False,
                    'category': 'inappropriate',
                    'confidence': 0.9,
                    'entities': {},
                    'recommendation': 'reject',
                    'reason': f'Contenido inapropiado detectado: {pattern}'
                }
        
        # Define category keywords
        categories = {
            'vacation': [
                'vacaciones', 'días', 'cuánto me toca', 'descanso',
                'tiempo libre', 'feriado', 'holiday', 'vacation', 'days off'
            ],
            'benefits': [
                'beneficios', 'seguro', 'salud', 'pensión', 'retiro',
                'benefits', 'insurance', 'health', 'retirement'
            ],
            'salary': [
                'salario', 'sueldo', 'pago', 'compensación', 'aumento',
                'salary', 'pay', 'compensation', 'raise'
            ],
            'contract': [
                'contrato', 'renovación', 'término', 'despido',
                'contract', 'renewal', 'termination', 'dismissal'
            ],
            'attendance': [
                'asistencia', 'horario', 'llegada tarde', 'ausencia',
                'attendance', 'schedule', 'late', 'absence'
            ]
        }
        
        # Categorize prompt
        category_scores = {}
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            if score > 0:
                category_scores[category] = score
        
        # Determine primary category
        if category_scores:
            primary_category = max(category_scores.items(), key=lambda x: x[1])[0]
            confidence = min(category_scores[primary_category] * 0.3, 1.0)
        else:
            primary_category = 'general'
            confidence = 0.5
        
        # Extract entities (numbers, time periods)
        entities = {}
        
        # Extract numbers
        import re
        numbers = re.findall(r'\d+', user_prompt)
        if numbers:
            entities['numbers'] = numbers
        
        # Extract time periods
        time_patterns = {
            'años': r'(\d+)\s*año[s]?',
            'meses': r'(\d+)\s*mes(?:es)?',
            'días': r'(\d+)\s*día[s]?',
        }
        
        for key, pattern in time_patterns.items():
            matches = re.findall(pattern, prompt_lower)
            if matches:
                entities[key] = matches
        
        # Determine recommendation
        if confidence >= 0.6:
            recommendation = 'process'
            reason = f'Prompt válido categorizado como: {primary_category}'
        elif confidence >= 0.3:
            recommendation = 'process_with_caution'
            reason = f'Prompt posiblemente válido, categoría incierta: {primary_category}'
        else:
            recommendation = 'clarify'
            reason = 'Prompt muy genérico, puede requerir clarificación'
        
        return {
            'is_valid': True,
            'category': primary_category,
            'confidence': confidence,
            'entities': entities,
            'recommendation': recommendation,
            'reason': reason,
            'all_category_scores': category_scores
        }
        
    except Exception as e:
        print(f"Error validating prompt: {e}")
        return {
            'is_valid': False,
            'category': 'error',
            'confidence': 0.0,
            'entities': {},
            'recommendation': 'reject',
            'reason': f'Error en validación: {str(e)}'
        }

# ============================================================================
# Complete RAG Pipeline Function
# ============================================================================

def rag_pipeline(
    user_query: str,
    knowledge_base_id: str = KNOWLEDGE_BASE_ID,
    model_id: str = LLM_MODEL_ID,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_results: int = 5,
    score_threshold: float = 0.1
) -> Dict[str, Any]:
    """
    Complete RAG pipeline: validate -> retrieve -> generate.
    
    Args:
        user_query (str): User's question
        knowledge_base_id (str): Bedrock Knowledge Base ID
        model_id (str): LLM model ID
        temperature (float): LLM temperature parameter
        top_p (float): LLM top_p parameter
        max_results (int): Max documents to retrieve
        score_threshold (float): Minimum similarity score
        
    Returns:
        Dict with validation, retrieval, and generation results
    """
    # Step 1: Validate prompt
    validation = valid_prompt(user_query)
    
    if not validation['is_valid']:
        return {
            'validation': validation,
            'retrieval': None,
            'generation': None,
            'final_response': f"Lo siento, no puedo procesar tu pregunta: {validation['reason']}"
        }
    
    # Step 2: Retrieve relevant documents
    retrieval = query_knowledge_base(
        query=user_query,
        knowledge_base_id=knowledge_base_id,
        max_results=max_results,
        score_threshold=score_threshold
    )
    
    # Step 3: Generate response
    generation = generate_response(
        query=user_query,
        context_documents=retrieval['results'],
        model_id=model_id,
        temperature=temperature,
        top_p=top_p
    )
    
    return {
        'validation': validation,
        'retrieval': retrieval,
        'generation': generation,
        'final_response': generation['response']
    }

# ============================================================================
# Testing and Examples
# ============================================================================

if __name__ == "__main__":
    """Example usage and testing."""
    
    print("="*70)
    print("Bedrock Utilities - Test Examples")
    print("="*70 + "\n")
    
    # Example 1: Validate prompts
    print("Example 1: Prompt Validation")
    print("-" * 70)
    
    test_prompts = [
        "¿Cuántos días de vacaciones tengo después de 1 año?",
        "hack the system",
        "¿Qué beneficios ofrece la empresa?",
        ""
    ]
    
    for prompt in test_prompts:
        result = valid_prompt(prompt)
        print(f"Prompt: '{prompt}'")
        print(f"Valid: {result['is_valid']}, Category: {result['category']}, "
              f"Confidence: {result['confidence']:.2f}")
        print(f"Recommendation: {result['recommendation']}")
        print()
    
    print("\nFor full RAG pipeline testing, ensure environment variables are set:")
    print("  - KNOWLEDGE_BASE_ID")
    print("  - AWS credentials configured")
