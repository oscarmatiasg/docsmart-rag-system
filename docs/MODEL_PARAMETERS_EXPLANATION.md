# 🎛️ Model Parameters: Temperature and Top_p Explained

**DocSmart RAG System - AWS AI Engineer Nanodegree**

---

## Understanding Temperature and Top_p in LLM Generation

Large Language Models like Claude 3.5 Sonnet use sampling strategies to generate text. Two critical parameters control this process: **temperature** and **top_p**. These parameters fundamentally shape how the model balances between deterministic accuracy and creative diversity in its responses.

**Temperature** (range: 0.0 to 1.0) controls the randomness or "creativity" of the model's output by adjusting the probability distribution over possible next tokens. At temperature 0.0, the model always selects the most probable token, resulting in deterministic and highly consistent responses—ideal for factual queries like "How many vacation days do I have?" where precision is paramount. As temperature increases toward 1.0, the model samples from a broader distribution of tokens, introducing more variation and creativity but potentially sacrificing accuracy. In DocSmart, we strategically use low temperatures (0.3-0.5) for HR policy queries where factual correctness is critical, and moderate temperatures (0.6-0.7) for conversational interactions where natural language flow is desired without compromising accuracy.

**Top_p** (range: 0.0 to 1.0), also known as nucleus sampling, works complementarily by defining a cumulative probability threshold for token selection. Instead of considering all possible tokens, the model only samples from the smallest set of tokens whose cumulative probability exceeds the top_p value. For instance, with top_p=0.9, the model considers only the top tokens that together account for 90% of the probability mass, effectively filtering out highly unlikely options while maintaining sufficient diversity. This approach is more dynamic than traditional top-k sampling because it adapts to the confidence level of each prediction—when the model is confident, fewer tokens are considered; when uncertain, more options remain viable. In DocSmart, we maintain top_p at 0.9 to ensure responses remain coherent and contextually appropriate while allowing enough flexibility to handle the nuanced phrasing of user queries. This combination of temperature=0.5 and top_p=0.9 achieves an optimal balance: precise enough for enterprise HR documentation retrieval, yet natural enough for genuine conversational interaction.

---

## Practical Implementation in DocSmart

### Configuration for Different Use Cases

```python
# Configuration 1: Precise Factual Queries (HR Policies)
response_precise = generate_response(
    query="¿Cuántos días de vacaciones tengo según mi antigüedad?",
    context_documents=retrieved_docs,
    temperature=0.3,  # Low - Emphasizes most probable (accurate) answers
    top_p=0.9         # Standard - Maintains natural language flow
)
# Result: Deterministic, fact-based answer directly from policy documents

# Configuration 2: Conversational Interactions
response_conversational = generate_response(
    query="Cuéntame sobre los beneficios de la empresa",
    context_documents=retrieved_docs,
    temperature=0.7,  # Higher - More natural, varied explanations
    top_p=0.9         # Standard - Good diversity without randomness
)
# Result: Natural, engaging explanation while staying grounded in documents
```

### Why These Values?

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Temperature** | 0.3-0.7 | DocSmart requires factual accuracy (low temp) but must sound natural (not robotic). We avoid extremes: 0.0 would be too rigid, 1.0 too unpredictable. |
| **Top_p** | 0.9 | Standard setting that filters the long tail of unlikely tokens while preserving enough options for contextually appropriate phrasing. |

### Observable Impact

When testing the same query with different parameters:

**Query**: "¿Cuántos días de vacaciones tengo?"

| Temperature | Typical Response Style |
|-------------|------------------------|
| 0.0 | "Según la política de vacaciones, empleados con 1 año tienen 15 días hábiles." (Identical on every run) |
| 0.5 | "Tienes 15 días hábiles de vacaciones si has completado 1 año de antigüedad." (Slight variations in phrasing) |
| 1.0 | "¡Bueno! Mirando las políticas... parece que después del primer año trabajando aquí, se te otorgan aproximadamente 15 días..." (More varied, potentially overly casual) |

**Conclusion**: For DocSmart's HR use case, temperature=0.5 and top_p=0.9 provide the "Goldilocks zone"—accurate enough to be trustworthy as an HR resource, natural enough to feel conversational and helpful.

---

## Technical Details

### Bedrock API Request with Parameters

```python
request_body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4096,
    "temperature": 0.5,    # ← Controls randomness
    "top_p": 0.9,          # ← Controls diversity
    "messages": [
        {
            "role": "user",
            "content": f"Context: {context}\n\nQuestion: {query}"
        }
    ]
}

response = bedrock_runtime.invoke_model(
    modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
    body=json.dumps(request_body)
)
```

### Mathematical Intuition

**Temperature** scales logits before softmax:
```
probability_i = exp(logit_i / temperature) / Σ exp(logit_j / temperature)
```
- Lower temp → sharper distribution (argmax-like)
- Higher temp → flatter distribution (more uniform)

**Top_p** filters cumulative probability:
```
selected_tokens = {tokens where Σ P(token) ≤ top_p}
```
- Dynamically adjusts to model confidence
- More robust than fixed top-k

---

## References

- Anthropic Claude Documentation: https://docs.anthropic.com/claude/docs/
- AWS Bedrock Best Practices: https://docs.aws.amazon.com/bedrock/
- Holtzman et al. (2019): "The Curious Case of Neural Text Degeneration" (Top-p sampling paper)

---

**Author**: [Your Name]  
**Course**: AWS AI Engineer Nanodegree - Udacity x AWS  
**Date**: December 2025
