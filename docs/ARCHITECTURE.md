# 🏗️ Arquitectura Técnica - DocSmart RAG System

## 📋 Tabla de Contenidos
1. [Visión General](#visión-general)
2. [Componentes del Sistema](#componentes-del-sistema)
3. [Flujo de Datos](#flujo-de-datos)
4. [Decisiones de Diseño](#decisiones-de-diseño)
5. [Escalabilidad](#escalabilidad)
6. [Seguridad](#seguridad)

---

## 🎯 Visión General

DocSmart es un sistema RAG (Retrieval-Augmented Generation) empresarial que implementa las mejores prácticas de arquitectura de IA generativa, combinando:

- **Vector Search**: Búsqueda semántica de alta precisión
- **LLM Generation**: Generación de respuestas contextualizadas
- **Serverless Architecture**: Auto-escalamiento y pay-per-use
- **Enterprise Security**: Múltiples capas de seguridad

### Principios de Arquitectura

1. **Separation of Concerns**: Cada componente tiene una responsabilidad única
2. **Modularity**: Componentes intercambiables e independientes
3. **Scalability**: Diseñado para crecer horizontalmente
4. **Security First**: Seguridad integrada en cada capa
5. **Observability**: Logs y métricas en todos los componentes

---

## 🔧 Componentes del Sistema

### 1. **Document Processor**
```python
document_processor.py
```

**Responsabilidad**: Extracción y preparación de documentos

**Funcionalidades**:
- Soporte multi-formato (PDF, DOCX, TXT, MD)
- Extracción de texto limpio
- Chunking inteligente con overlap
- Preservación de estructura semántica

**Algoritmo de Chunking**:
```
1. Dividir en chunks de tamaño CHUNK_SIZE
2. Buscar límites de oración
3. Aplicar CHUNK_OVERLAP para continuidad
4. Generar metadata por chunk
```

**Trade-offs**:
- ✅ Chunks pequeños → Mayor precisión
- ❌ Chunks pequeños → Más embeddings → Mayor costo
- ✅ Overlap → Mejor contexto
- ❌ Overlap → Redundancia

**Configuración Recomendada**:
| Tipo de Documento | Chunk Size | Overlap |
|------------------|------------|---------|
| Técnico/Legal | 500-800 | 100-150 |
| Narrativo | 1000-1500 | 200-300 |
| FAQ/Short | 300-500 | 50-100 |

---

### 2. **Embedding Service**
```python
embedding_service.py
```

**Responsabilidad**: Generación de vectores semánticos

**Modelo**: Amazon Titan Embeddings v2
- Dimensiones: 1024
- Max input tokens: 8192
- Multilingual support

**Proceso**:
```python
text → tokenize → embed_model → vector[1024]
```

**Optimizaciones**:
- Batch processing para múltiples textos
- Caching de embeddings frecuentes (futuro)
- Normalización de vectores

**Métricas de Similitud**:

1. **Cosine Similarity** (Usado)
```python
similarity = dot(v1, v2) / (||v1|| * ||v2||)
Range: [-1, 1]
```
- ✅ Invariante a magnitud
- ✅ Rápido de calcular
- ✅ Estándar en la industria

2. **Euclidean Distance** (Alternativa)
```python
distance = sqrt(sum((v1 - v2)^2))
Range: [0, ∞]
```
- ✅ Intuitivo
- ❌ Sensible a magnitud

---

### 3. **Vector Database**
```python
vector_database.py
```

**Responsabilidad**: Almacenamiento y búsqueda vectorial

**Tecnología**: Aurora PostgreSQL + pgvector

**Schema**:
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(255),
    text TEXT,
    embedding vector(1024),
    metadata JSONB,
    created_at TIMESTAMP
);

CREATE INDEX ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

**Índice IVFFlat**:
- Inverted File with Flat Compression
- Trade-off: Velocidad vs Precisión
- `lists=100`: 100 particiones para búsqueda

**Consulta Vectorial**:
```sql
SELECT * FROM documents
ORDER BY embedding <=> query_vector
LIMIT k;
```
- `<=>`: Operador de distancia de coseno
- `k`: Top-K documentos más similares

**Performance**:
| Documentos | Búsqueda (avg) | Índice |
|-----------|----------------|--------|
| 1K | ~10ms | IVFFlat |
| 10K | ~50ms | IVFFlat |
| 100K | ~200ms | IVFFlat |
| 1M+ | ~500ms | IVFFlat + Sharding |

---

### 4. **RAG System**
```python
rag_system.py
```

**Responsabilidad**: Orquestación del pipeline RAG

**Pipeline Completo**:
```
Query → Embed → Search → Context → Prompt → LLM → Response
```

**Pasos Detallados**:

1. **Query Embedding**
   ```python
   query_vector = embed_service.generate_embedding(query)
   ```

2. **Retrieval**
   ```python
   docs = vector_db.search_similar(query_vector, top_k=5)
   ```

3. **Context Formation**
   ```python
   context = format_context(docs)
   ```

4. **Prompt Engineering**
   ```python
   prompt = f"""
   <context>{context}</context>
   <question>{query}</question>
   Answer based on context only.
   """
   ```

5. **LLM Generation**
   ```python
   response = bedrock.invoke_model(
       modelId="claude-3-5-sonnet",
       body={"messages": [{"role": "user", "content": prompt}]}
   )
   ```

**Configuración de LLM**:
```python
{
    "max_tokens": 4096,      # Longitud máxima de respuesta
    "temperature": 0.7,      # Creatividad (0=determinista, 1=creativo)
    "top_p": 0.9,           # Nucleus sampling
    "top_k": 50             # Top-K sampling
}
```

**Prompt Engineering Best Practices**:
- ✅ Instrucciones claras y específicas
- ✅ Contexto estructurado (XML tags)
- ✅ Ejemplos (few-shot) cuando sea necesario
- ✅ Restricciones explícitas ("solo del contexto")
- ✅ Formato de salida deseado

---

### 5. **Ingestion Pipeline**
```python
ingestion_pipeline.py
```

**Responsabilidad**: Ingesta end-to-end de documentos

**Proceso**:
```
Upload → Extract → Clean → Chunk → Embed → Store
```

**Componentes**:
1. **S3 Upload**: Almacenamiento original
2. **Text Extraction**: PyPDF2, python-docx
3. **Cleaning**: Eliminación de noise
4. **Chunking**: División semántica
5. **Embedding**: Generación vectorial
6. **Database Storage**: PostgreSQL

**Optimizaciones**:
- Procesamiento paralelo de chunks
- Batch embedding (reduce API calls)
- Transacciones atómicas
- Retry logic con exponential backoff

**Manejo de Errores**:
```python
try:
    process_document(doc)
except PDFError:
    log_error("PDF corrupto")
except EmbeddingError:
    retry_with_backoff()
except DatabaseError:
    rollback_transaction()
```

---

### 6. **Security Module**
```python
security.py
```

**Responsabilidad**: Validación y protección

**Capas de Seguridad**:

1. **Input Validation**
   - Longitud máxima
   - Caracteres permitidos
   - Tipos de archivo

2. **Injection Prevention**
   - SQL injection patterns
   - XSS detection
   - Command injection

3. **Content Policy**
   - Violence detection
   - Illegal activity
   - PII protection

4. **Output Sanitization**
   - Masking de PII
   - Content filtering
   - Safe rendering

**Patterns Detectados**:
```python
sql_patterns = [
    r"(?i)(union\s+select)",
    r"(?i)(drop\s+table)",
    r"(?i)(delete\s+from)"
]

xss_patterns = [
    r"<script.*?>.*?</script>",
    r"javascript:",
    r"onerror="
]
```

---

## 🔄 Flujo de Datos Completo

### Escenario 1: Ingesta de Documento

```
┌─────────────────────────────────────────────────────────┐
│ 1. Usuario sube "policy.pdf"                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Security: Validate file (type, size)                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 3. S3: Upload original file                             │
│    → s3://bucket/policy.pdf                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Document Processor:                                  │
│    - Extract text: "Vacation policy..."                │
│    - Clean: Remove headers/footers                     │
│    - Chunk: Split into 5 chunks                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Embedding Service:                                   │
│    Chunk 1: [0.12, -0.45, ..., 0.78] (1024 dims)      │
│    Chunk 2: [0.15, -0.42, ..., 0.81]                  │
│    ...                                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Vector Database:                                     │
│    INSERT INTO documents (text, embedding, metadata)   │
│    CREATE INDEX for vector search                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 7. Success: Document indexed & searchable              │
└─────────────────────────────────────────────────────────┘
```

### Escenario 2: Consulta RAG

```
┌─────────────────────────────────────────────────────────┐
│ 1. Usuario: "¿Cuántos días de vacaciones tengo?"       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Security: Validate & sanitize query                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Embedding Service:                                   │
│    Query → [0.23, -0.56, ..., 0.89]                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Vector Search:                                       │
│    SELECT * ORDER BY embedding <=> query_vec LIMIT 5   │
│    Results:                                             │
│    - Doc1 (similarity: 0.89)                           │
│    - Doc2 (similarity: 0.85)                           │
│    - Doc3 (similarity: 0.82)                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Context Formation:                                   │
│    "[Doc1] Employees get 15 vacation days..."          │
│    "[Doc2] Vacation accrues monthly..."                │
│    "[Doc3] Request vacation 2 weeks advance..."        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Prompt Engineering:                                  │
│    <context>                                            │
│      [Doc1] Employees get 15 vacation days...          │
│      [Doc2] Vacation accrues monthly...                │
│    </context>                                           │
│    <question>                                           │
│      ¿Cuántos días de vacaciones tengo?                │
│    </question>                                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 7. Bedrock LLM (Claude 3.5):                           │
│    Invoke model with prompt                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 8. Response Generation:                                 │
│    "Según la política de la empresa, los empleados     │
│     reciben 15 días de vacaciones al año..."           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 9. Log Query:                                           │
│    INSERT INTO query_logs (query, response_time, ...)  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 10. Return to User:                                     │
│     - Answer                                            │
│     - Sources (Doc1, Doc2)                             │
│     - Metadata (time, confidence)                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Decisiones de Diseño

### 1. **Aurora PostgreSQL vs Alternatives**

| Factor | Aurora + pgvector | Pinecone | FAISS | OpenSearch |
|--------|------------------|----------|-------|------------|
| Managed | ✅ Sí | ✅ Sí | ❌ No | ⚠️ Parcial |
| Cost | 💰💰 | 💰💰💰 | 💰 | 💰💰 |
| Scale | Excelente | Excelente | Manual | Bueno |
| SQL Support | ✅ Nativo | ❌ No | ❌ No | ⚠️ Limitado |
| Metadata | ✅ JSONB | ⚠️ Limitado | ❌ No | ✅ Sí |

**Decisión**: Aurora PostgreSQL
- ✅ Aprovecha SQL nativo para queries complejas
- ✅ JSONB para metadata flexible
- ✅ Serverless auto-scaling
- ✅ Integración con ecosistema AWS

### 2. **Claude 3.5 Sonnet vs Alternatives**

| Modelo | Context | Speed | Cost | Quality |
|--------|---------|-------|------|---------|
| Claude 3.5 | 200K | ⚡⚡⚡ | 💰💰 | ⭐⭐⭐⭐⭐ |
| GPT-4 | 128K | ⚡⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ |
| Titan | 32K | ⚡⚡⚡⚡ | 💰 | ⭐⭐⭐ |
| Llama 2 | 4K | ⚡⚡⚡ | 💰 | ⭐⭐⭐ |

**Decisión**: Claude 3.5 Sonnet
- ✅ Balance óptimo precio/calidad
- ✅ 200K tokens de contexto
- ✅ Excelente en seguir instrucciones
- ✅ Nativo en Bedrock

### 3. **Chunking Strategy**

**Fixed-size vs Semantic Chunking**:

```python
# Fixed-size (Usado)
chunk_size = 1000
overlap = 200

# Semantic (Futuro)
chunk_on_sentences()
chunk_on_paragraphs()
chunk_on_topics()
```

**Decisión**: Fixed-size con sentence boundary
- ✅ Predecible y consistente
- ✅ Fácil de implementar
- ✅ Buen performance
- ⚠️ Puede romper contexto (mitigado con overlap)

---

## 📈 Escalabilidad

### Límites Actuales

| Métrica | Límite Actual | Solución para Escalar |
|---------|---------------|----------------------|
| Documentos | ~100K | Sharding, partitioning |
| Queries/seg | ~50 | Read replicas |
| Tamaño DB | 1TB | Aurora auto-scaling |
| Embeddings/min | 1000 | Batch processing |

### Estrategias de Escalamiento

#### 1. **Horizontal Scaling**
```
Read Replicas:
Aurora Writer ──┬──> Reader 1 (Queries)
                ├──> Reader 2 (Queries)
                └──> Reader 3 (Analytics)
```

#### 2. **Caching Layer**
```python
# Redis para embeddings frecuentes
cache.get(query_hash) or generate_embedding(query)
```

#### 3. **Async Processing**
```python
# Celery para ingesta asíncrona
@celery.task
def ingest_document(file_path):
    ...
```

#### 4. **CDN para S3**
```
CloudFront → S3 (Documents)
TTL: 24h
```

### Monitoreo de Performance

**Métricas Clave**:
```python
- p50 query latency: < 500ms
- p99 query latency: < 2s
- Embedding generation: < 100ms
- Vector search: < 50ms
- LLM response: < 2s
```

**CloudWatch Alarms**:
```terraform
resource "aws_cloudwatch_metric_alarm" "high_latency" {
  alarm_name          = "docsmartquery_high_latency"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "QueryLatency"
  namespace           = "DocSmart"
  period              = "60"
  statistic           = "Average"
  threshold           = "2000"  # 2s
}
```

---

## 🔒 Seguridad en Profundidad

### Capa 1: Network Security

```
Internet Gateway
    │
    ▼
ALB (public subnet)
    │
    ▼
Application (private subnet)
    │
    ▼
Aurora (private subnet, no internet)
```

**Security Groups**:
```terraform
# Application SG
ingress {
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

# Database SG
ingress {
  from_port       = 5432
  to_port         = 5432
  protocol        = "tcp"
  security_groups = [app_sg.id]  # Solo desde app
}
```

### Capa 2: IAM & Authentication

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude*",
        "arn:aws:bedrock:*::foundation-model/amazon.titan*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::docsmart-documents/*"
    }
  ]
}
```

### Capa 3: Data Encryption

**En tránsito**:
- TLS 1.3 para todas las comunicaciones
- Certificate Manager para certificados

**En reposo**:
- S3: AES-256
- Aurora: KMS encryption
- Secrets Manager para credenciales

### Capa 4: Application Security

**Input Validation**:
```python
def validate_query(query):
    # Length
    if len(query) > MAX_LENGTH:
        raise ValidationError()
    
    # SQL injection
    if re.search(sql_pattern, query):
        raise SecurityError()
    
    # XSS
    if re.search(xss_pattern, query):
        raise SecurityError()
```

**Output Sanitization**:
```python
def sanitize_response(response):
    # Mask PII
    response = mask_email(response)
    response = mask_phone(response)
    response = mask_ssn(response)
    return response
```

### Capa 5: Audit & Logging

```python
# Todos los eventos se loguean
logger.info(f"Query: {query[:100]}, User: {user_id}, IP: {ip}")
logger.info(f"Results: {len(results)}, Time: {response_time}ms")

# CloudTrail para AWS API calls
# VPC Flow Logs para tráfico de red
# CloudWatch Logs para application logs
```

---

## 🎓 Lecciones Aprendidas

### ✅ Qué Funcionó Bien

1. **Modularity**: Fácil de testear y mantener
2. **Terraform**: Infraestructura reproducible
3. **pgvector**: Performance excelente para < 1M docs
4. **Bedrock**: Sin gestión de modelos
5. **Streamlit**: Prototipado rápido de UI

### ⚠️ Desafíos y Soluciones

1. **Problema**: Respuestas genéricas
   - **Solución**: Mejor prompt engineering + TOP_K más alto

2. **Problema**: Embeddings lentos
   - **Solución**: Batch processing

3. **Problema**: Costos de Bedrock altos
   - **Solución**: Caching + prompts más cortos

4. **Problema**: Chunks perdiendo contexto
   - **Solución**: Mayor overlap + semantic chunking

---

## 🔮 Evolución Futura

### Fase 2: Optimizaciones
- [ ] Hybrid search (keyword + vector)
- [ ] Re-ranking de resultados
- [ ] Caching inteligente
- [ ] Async ingestion con Celery

### Fase 3: Features Avanzados
- [ ] Multi-modal (imágenes, tablas)
- [ ] Agents con tool calling
- [ ] Fine-tuned embeddings
- [ ] Feedback loop

### Fase 4: Enterprise
- [ ] Multi-tenancy
- [ ] RBAC avanzado
- [ ] Compliance (SOC2, HIPAA)
- [ ] SLA 99.9%

---

**Documentado por**: DocSmart Team  
**Última actualización**: 2024  
**Versión**: 1.0
