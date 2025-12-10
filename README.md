# 📚 DocSmart - Sistema Inteligente de Consulta de Documentos con RAG

![Architecture](https://img.shields.io/badge/Architecture-RAG-blue)
![AWS](https://img.shields.io/badge/AWS-Bedrock-orange)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Descripción del Proyecto

**DocSmart** es un sistema empresarial de consulta inteligente de documentos que aprovecha el poder de **Retrieval-Augmented Generation (RAG)** con **Amazon Bedrock**, **Aurora PostgreSQL** y **Amazon S3**. Permite a las organizaciones transformar su documentación en una base de conocimiento consultable mediante lenguaje natural, proporcionando respuestas precisas y contextualizadas basadas en documentos corporativos.

### 🌟 Características Principales

- **🤖 IA Generativa Avanzada**: Utiliza Claude 3.5 Sonnet de Anthropic vía Amazon Bedrock
- **🔍 Búsqueda Semántica**: Embeddings vectoriales con Amazon Titan para búsquedas por significado
- **📊 Base de Datos Vectorial**: Aurora PostgreSQL Serverless con extensión pgvector
- **🪣 Almacenamiento Escalable**: Amazon S3 para gestión de documentos
- **🛡️ Seguridad Integrada**: Validación de inputs, sanitización y guardrails
- **💬 Interfaz Interactiva**: Aplicación web con Streamlit
- **⚙️ CLI Completo**: Herramientas de línea de comandos para automatización
- **🏗️ Infrastructure as Code**: Terraform para despliegue automatizado

---

## 🏛️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │   Chat Application            │
         │   (Streamlit / CLI)           │
         └───────────┬───────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌───────────┐  ┌──────────┐  ┌──────────────┐
│  Security │  │ Ingestion│  │  RAG System  │
│ Guardrails│  │ Pipeline │  │              │
└───────────┘  └────┬─────┘  └──────┬───────┘
                    │                │
        ┌───────────┴────────────────┴──────────┐
        │                                        │
        ▼                                        ▼
┌────────────────┐                    ┌──────────────────┐
│   Amazon S3    │                    │ Amazon Bedrock   │
│   Documents    │                    │ - Titan Embed    │
│   Storage      │                    │ - Claude 3.5     │
└────────────────┘                    └──────────────────┘
        │
        ▼
┌────────────────────────────────────┐
│  Aurora PostgreSQL Serverless      │
│  + pgvector Extension              │
│  - Document Chunks                 │
│  - Vector Embeddings (1024-dim)    │
│  - Metadata                        │
│  - Query Logs                      │
└────────────────────────────────────┘
```

### 🔄 Flujo de Datos

#### **1. Ingesta de Documentos**
```
Documento → Procesamiento → Chunks → Embeddings → Vector DB + S3
```

1. **Carga**: El documento se sube al sistema (PDF, DOCX, TXT, MD)
2. **Procesamiento**: Se extrae y limpia el texto
3. **Chunking**: Se divide en fragmentos de ~1000 caracteres con overlap de 200
4. **Embedding**: Cada chunk se convierte en un vector de 1024 dimensiones usando Titan
5. **Almacenamiento**: 
   - Documento original → S3
   - Chunks + embeddings + metadata → Aurora PostgreSQL

#### **2. Consulta (RAG Pipeline)**
```
Pregunta → Embedding → Búsqueda Vectorial → Contexto → LLM → Respuesta
```

1. **Query Embedding**: La pregunta del usuario se convierte en vector (Titan)
2. **Retrieval**: Búsqueda de los K chunks más similares usando cosine similarity
3. **Contexto**: Se extraen los textos de los chunks relevantes
4. **Augmentation**: Se construye un prompt con contexto + pregunta
5. **Generation**: Claude 3.5 Sonnet genera la respuesta basada en el contexto
6. **Respuesta**: Se devuelve la respuesta con fuentes citadas

---

## 💼 Casos de Uso Empresariales

### 1. 👥 **Recursos Humanos (RRHH)**

**Escenario**: Gestión de políticas, procedimientos y documentación de empleados

**Documentos típicos**:
- Manuales de empleado
- Políticas de la empresa
- Procedimientos de contratación
- Beneficios y compensaciones
- Regulaciones laborales

**Consultas ejemplo**:
- "¿Cuál es la política de vacaciones para empleados con 5 años de antigüedad?"
- "¿Qué pasos debo seguir para solicitar un permiso parental?"
- "¿Cuáles son los beneficios de salud disponibles?"

**Beneficios**:
- ✅ Respuestas instantáneas 24/7
- ✅ Reducción de carga en equipo de RRHH
- ✅ Consistencia en información
- ✅ Onboarding más eficiente

---

### 2. 💰 **Ventas y Soporte Comercial**

**Escenario**: Base de conocimiento de productos y respuesta rápida a clientes

**Documentos típicos**:
- Fichas técnicas de productos
- Manuales de usuario
- Políticas de garantía
- FAQ de productos
- Casos de éxito

**Consultas ejemplo**:
- "¿Qué características tiene el modelo X comparado con el modelo Y?"
- "¿Cuál es la política de devoluciones para productos electrónicos?"
- "¿Qué casos de uso exitosos tenemos en el sector financiero?"

**Beneficios**:
- ✅ Aceleración del ciclo de ventas
- ✅ Respuestas precisas a clientes
- ✅ Capacitación rápida de nuevos vendedores
- ✅ Mejor experiencia del cliente

---

### 3. ⚖️ **Legal y Compliance**

**Escenario**: Consulta de contratos, regulaciones y jurisprudencia

**Documentos típicos**:
- Contratos
- Políticas de compliance
- Regulaciones sectoriales
- Precedentes legales
- Auditorías

**Consultas ejemplo**:
- "¿Qué cláusulas de indemnización tenemos en contratos tipo A?"
- "¿Cumplimos con la regulación GDPR en procesamiento de datos?"
- "¿Qué precedentes tenemos sobre disputas contractuales?"

**Beneficios**:
- ✅ Búsqueda rápida en documentación legal
- ✅ Identificación de riesgos
- ✅ Ahorro de tiempo en research
- ✅ Mejor compliance

---

### 4. 🏥 **Healthcare y Farmacéutica**

**Escenario**: Consulta de protocolos médicos y documentación clínica

**Documentos típicos**:
- Protocolos clínicos
- Resultados de estudios
- Información de medicamentos
- Guías de tratamiento

**Consultas ejemplo**:
- "¿Cuál es el protocolo para tratamiento de diabetes tipo 2?"
- "¿Qué interacciones tiene el medicamento X con Y?"
- "¿Cuáles son las contraindicaciones del tratamiento Z?"

**Beneficios**:
- ✅ Acceso rápido a información crítica
- ✅ Mejora en decisiones clínicas
- ✅ Reducción de errores médicos
- ✅ Cumplimiento de protocolos

---

### 5. 🏭 **Manufactura y Operaciones**

**Escenario**: Manuales técnicos y procedimientos operativos

**Documentos típicos**:
- Manuales de equipos
- SOPs (Standard Operating Procedures)
- Guías de mantenimiento
- Protocolos de seguridad

**Consultas ejemplo**:
- "¿Cómo realizar mantenimiento preventivo del equipo de producción línea 3?"
- "¿Qué protocolo de seguridad seguir en caso de fuga química?"
- "¿Cuáles son los parámetros óptimos para proceso de inyección?"

**Beneficios**:
- ✅ Reducción de downtime
- ✅ Mejora en seguridad operacional
- ✅ Capacitación más eficiente
- ✅ Estandarización de procesos

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Python 3.9+**
- **Cuenta de AWS** con acceso a:
  - Amazon Bedrock
  - Amazon S3
  - Aurora PostgreSQL
- **Terraform** (para infraestructura)
- **Credenciales de AWS** configuradas

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd docsmart-rag-system
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Configuración en `.env`:**

```env
# AWS Configuration
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key

# S3 Configuration
S3_BUCKET_NAME=docsmart-documents-bucket

# Aurora PostgreSQL Configuration
DB_HOST=tu-aurora-endpoint.us-west-2.rds.amazonaws.com
DB_PORT=5432
DB_NAME=docsmart_db
DB_USER=postgres
DB_PASSWORD=tu_password_seguro

# Bedrock Configuration
BEDROCK_EMBEDDING_MODEL=amazon.titan-embed-text-v2:0
BEDROCK_LLM_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
```

### 5. Aprovisionar Infraestructura con Terraform

```bash
cd terraform

# Inicializar Terraform
terraform init

# Revisar plan de recursos
terraform plan -var="db_master_password=TuPasswordSeguro123!"

# Aplicar infraestructura
terraform apply -var="db_master_password=TuPasswordSeguro123!"

# Guardar outputs
terraform output > ../terraform_outputs.txt
```

**Importante**: Actualiza el `.env` con los outputs de Terraform (endpoints de Aurora y nombre del bucket S3).

### 6. Inicializar Base de Datos

```bash
cd ..
python cli.py setup
```

Esto creará:
- Extensión `pgvector`
- Tabla `documents` con índice vectorial
- Tabla `query_logs` para analytics

---

## 📖 Uso del Sistema

### Opción 1: Interfaz Web (Streamlit)

```bash
streamlit run app.py
```

Accede a `http://localhost:8501` y:

1. **Ingerir Documentos**: Ve a la pestaña "Ingestar Documentos"
   - Sube archivos PDF, DOCX, TXT o MD
   - Selecciona categoría (RRHH, Ventas, Legal, etc.)
   - Click en "Ingerir Documentos"

2. **Consultar**: Ve a la pestaña "Chat"
   - Escribe tu pregunta
   - Recibe respuesta con fuentes citadas
   - Ajusta parámetros de búsqueda en el sidebar

3. **Ver Estadísticas**: Pestaña "Estadísticas"
   - Total de documentos indexados
   - Archivos en la base de conocimiento

### Opción 2: CLI (Línea de Comandos)

#### **Ingestar un Documento**

```bash
python cli.py ingest -f "documentos/manual_empleado.pdf"
```

#### **Ingestar Directorio Completo**

```bash
python cli.py ingest -d "documentos/politicas_rrhh/"
```

#### **Realizar Consulta**

```bash
python cli.py query "¿Cuál es la política de vacaciones?" -k 5
```

#### **Ver Estadísticas**

```bash
python cli.py stats
```

---

## 🔧 Configuración Avanzada

### Ajustar Parámetros de Chunking

En `config.py` o `.env`:

```python
CHUNK_SIZE=1000          # Tamaño de cada chunk en caracteres
CHUNK_OVERLAP=200        # Overlap entre chunks
```

**Recomendaciones**:
- Documentos técnicos: chunks más pequeños (500-800)
- Documentos narrativos: chunks más grandes (1000-1500)

### Ajustar Parámetros de LLM

```python
MAX_TOKENS=4096          # Máximo de tokens en respuesta
TEMPERATURE=0.7          # 0=determinista, 1=creativo
TOP_P=0.9               # Nucleus sampling
TOP_K_RESULTS=5         # Número de documentos a recuperar
```

### Personalizar System Role

En `rag_system.py`, modifica el `system_role` para casos de uso específicos:

```python
# Para RRHH
system_role = """Eres un asistente de RRHH especializado en políticas de empresa.
Proporciona respuestas precisas, cita las políticas relevantes y mantén un tono profesional."""

# Para Soporte Técnico
system_role = """Eres un experto en soporte técnico. Proporciona instrucciones paso a paso,
destaca precauciones de seguridad y referencias los manuales relevantes."""
```

---

## 🛡️ Seguridad y Mejores Prácticas

### 1. **Gestión de Credenciales**

❌ **NO** hardcodees credenciales en el código:
```python
# MAL
password = "mi_password_123"
```

✅ **SÍ** usa variables de entorno:
```python
# BIEN
password = os.getenv("DB_PASSWORD")
```

### 2. **Validación de Inputs**

El sistema incluye validación automática:
- Longitud máxima de consultas (2000 caracteres)
- Detección de patrones maliciosos (SQL injection, XSS)
- Validación de tipos de archivo
- Límites de tamaño de archivo (50 MB)

### 3. **Seguridad de Red**

Terraform configura:
- VPC aislada
- Security Groups restrictivos
- Subnets públicas y privadas
- Aurora en subnet privada

### 4. **Cifrado**

- **En tránsito**: TLS/SSL para comunicaciones
- **En reposo**: 
  - S3 con AES-256
  - Aurora con encryption at rest

### 5. **Control de Acceso**

Implementa IAM roles con permisos mínimos:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 📊 Monitoreo y Analytics

### Logs de Consultas

Todas las consultas se registran en la tabla `query_logs`:

```sql
SELECT 
    query_text,
    results_count,
    response_time_ms,
    created_at
FROM query_logs
ORDER BY created_at DESC
LIMIT 10;
```

### Métricas Clave

```sql
-- Consultas más frecuentes
SELECT query_text, COUNT(*) as frequency
FROM query_logs
GROUP BY query_text
ORDER BY frequency DESC
LIMIT 10;

-- Tiempo promedio de respuesta
SELECT AVG(response_time_ms) as avg_response_time
FROM query_logs;

-- Documentos más consultados
SELECT 
    d.file_name,
    COUNT(*) as access_count
FROM query_logs ql
JOIN documents d ON d.embedding <=> ql.query_embedding < 0.5
GROUP BY d.file_name
ORDER BY access_count DESC;
```

### CloudWatch Integration

El sistema exporta logs a CloudWatch:
- Application logs
- Query performance
- Error tracking

---

## 🔄 Mantenimiento y Actualizaciones

### Actualizar Documentos

Para reingestar un documento actualizado:

```bash
python cli.py ingest -f "documento_actualizado.pdf" --reingest
```

Esto:
1. Elimina la versión anterior
2. Procesa la nueva versión
3. Actualiza embeddings

### Backup de Base de Datos

Aurora realiza backups automáticos (configurado en Terraform):
- Backup window: 03:00-04:00 AM
- Retention: 7 días
- Point-in-time recovery habilitado

### Limpieza de Documentos Antiguos

```python
# Script de limpieza
from vector_database import VectorDatabase

db = VectorDatabase()
db.connect()

# Eliminar documentos específicos
db.delete_documents_by_file("documento_obsoleto.pdf")

db.close()
```

---

## 🧪 Testing y Validación

### Test del Pipeline Completo

```bash
# 1. Ingestar documento de prueba
python cli.py ingest -f "tests/sample.pdf"

# 2. Realizar consulta de prueba
python cli.py query "¿Cuál es el contenido principal del documento?"

# 3. Verificar estadísticas
python cli.py stats
```

### Validar Calidad de Embeddings

```python
from embedding_service import EmbeddingService

embedding_service = EmbeddingService()

# Test de similitud
text1 = "El gato está sobre la mesa"
text2 = "El felino está encima del mueble"
text3 = "El clima está soleado hoy"

emb1 = embedding_service.generate_embedding(text1)
emb2 = embedding_service.generate_embedding(text2)
emb3 = embedding_service.generate_embedding(text3)

sim_1_2 = EmbeddingService.cosine_similarity(emb1, emb2)
sim_1_3 = EmbeddingService.cosine_similarity(emb1, emb3)

print(f"Similitud 1-2 (relacionados): {sim_1_2:.3f}")
print(f"Similitud 1-3 (no relacionados): {sim_1_3:.3f}")

# Esperado: sim_1_2 > sim_1_3
```

---

## 🎓 Conceptos Clave de RAG

### ¿Qué es RAG?

**Retrieval-Augmented Generation** combina:
1. **Retrieval**: Búsqueda de información relevante
2. **Augmentation**: Enriquecimiento del prompt con contexto
3. **Generation**: Generación de respuesta por LLM

### Ventajas vs LLM Directo

| Característica | LLM Directo | RAG |
|---------------|-------------|-----|
| Conocimiento | Limitado a training data | Documentos actualizados |
| Precisión | Puede alucinar | Basado en fuentes reales |
| Trazabilidad | No tiene fuentes | Cita documentos |
| Actualización | Requiere reentrenamiento | Agregar documentos |
| Costo | Alto (tokens) | Optimizado |

### Embeddings y Búsqueda Vectorial

**Embeddings**: Representación numérica del significado semántico

```
"política de vacaciones" → [0.12, -0.45, 0.78, ..., 0.34] (1024 dims)
"días de descanso"       → [0.15, -0.42, 0.81, ..., 0.31] (1024 dims)
```

**Similitud de Coseno**: Mide ángulo entre vectores
- 1.0 = idénticos
- 0.0 = no relacionados
- -1.0 = opuestos

---

## 🚧 Troubleshooting

### Error: "Connection to database failed"

**Solución**:
1. Verifica que Aurora esté running en AWS Console
2. Revisa security group permite tu IP
3. Confirma endpoint en `.env`

```bash
# Test de conexión
psql -h your-endpoint.rds.amazonaws.com -U postgres -d docsmart_db
```

### Error: "Bedrock model not accessible"

**Solución**:
1. Ve a AWS Console → Bedrock
2. En "Model access", solicita acceso a:
   - amazon.titan-embed-text-v2:0
   - anthropic.claude-3-5-sonnet-20241022-v2:0
3. Espera aprobación (puede tardar minutos)

### Error: "No documents found" en consultas

**Solución**:
1. Verifica que hay documentos ingresados: `python cli.py stats`
2. Si no hay documentos, ingesta algunos: `python cli.py ingest -d docs/`
3. Verifica embeddings se generaron correctamente

### Respuestas de baja calidad

**Soluciones**:
1. **Aumentar TOP_K**: Recupera más contexto
   ```python
   TOP_K_RESULTS=10  # en vez de 5
   ```

2. **Ajustar chunk size**: Chunks más pequeños = más precisión
   ```python
   CHUNK_SIZE=800
   CHUNK_OVERLAP=150
   ```

3. **Mejorar quality de documentos**: 
   - Asegura que PDFs son text-based (no imágenes)
   - Limpia metadatos irrelevantes
   - Estructura clara en documentos fuente

---

## 📚 Recursos Adicionales

### Documentación de AWS

- [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Aurora PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/)
- [Amazon S3](https://docs.aws.amazon.com/s3/)

### Papers y Referencias

- [RAG Paper (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)
- [Embeddings for Everything](https://arxiv.org/abs/2112.09146)
- [pgvector Documentation](https://github.com/pgvector/pgvector)

### Comunidad

- [AWS Bedrock Samples](https://github.com/aws-samples/amazon-bedrock-samples)
- [LangChain Documentation](https://python.langchain.com/)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork del repositorio
2. Crea una branch para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

## 👨‍💻 Autor

Desarrollado como parte del proyecto de **Building GenAI Applications with Amazon Bedrock and Python** - Udacity Nanodegree Program.

---

## 🎯 Roadmap Futuro

### Versión 2.0
- [ ] Multi-modal support (imágenes, tablas)
- [ ] Fine-tuning de embeddings personalizados
- [ ] Agents con tool calling
- [ ] Integración con Slack/Teams
- [ ] Dashboard de analytics avanzado
- [ ] Support para más idiomas
- [ ] Feedback loop para mejorar calidad

### Optimizaciones
- [ ] Caching de embeddings frecuentes
- [ ] Hybrid search (keyword + semantic)
- [ ] Re-ranking de resultados
- [ ] Query expansion automática

---

## 📞 Soporte

Para preguntas o problemas:
- 📧 Email: oscarmatiasg@lutflow.com
- 💬 Issues: GitHub Issues
- 📖 Docs: [documentation-url]

---

**¡Gracias por usar DocSmart! 🚀📚**
