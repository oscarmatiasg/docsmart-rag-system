"""Script de prueba rápida para verificar Bedrock"""
import boto3
import json
import os
from dotenv import load_dotenv

# Cargar configuración
load_dotenv()

print("🧪 Probando Amazon Bedrock...")
print("-" * 50)

region = os.getenv('AWS_REGION', 'us-east-1')
embed_model = os.getenv('BEDROCK_EMBEDDING_MODEL', 'amazon.titan-embed-text-v2:0')
llm_model = os.getenv('BEDROCK_LLM_MODEL', 'anthropic.claude-3-5-sonnet-20240620-v1:0')

# Test 1: Embeddings
print("\n1️⃣ Probando Titan Embeddings...")
print(f"   Modelo: {embed_model}")
try:
    bedrock = boto3.client('bedrock-runtime', region_name=region)
    response = bedrock.invoke_model(
        modelId=embed_model,
        body=json.dumps({"inputText": "Hola mundo"})
    )
    result = json.loads(response['body'].read())
    embedding_dim = len(result['embedding'])
    print(f"✅ Embeddings funcionan! Dimensiones: {embedding_dim}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Claude LLM
print("\n2️⃣ Probando Claude 3.5 Sonnet...")
print(f"   Modelo: {llm_model}")
try:
    response = bedrock.invoke_model(
        modelId=llm_model,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user",
                    "content": "Di 'Hola, estoy funcionando correctamente' en una oración."
                }
            ]
        })
    )
    result = json.loads(response['body'].read())
    answer = result['content'][0]['text']
    print(f"✅ Claude funciona! Respuesta: {answer}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("🎉 ¡Todas las pruebas completadas!")
