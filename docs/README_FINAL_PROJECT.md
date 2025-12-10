# DocSmart RAG System - Proyecto Final

**AWS AI Engineer Nanodegree Program**  
**Udacity + Amazon Web Services**

![AWS](https://img.shields.io/badge/AWS-Bedrock-orange)
![Terraform](https://img.shields.io/badge/IaC-Terraform-blue)
![Python](https://img.shields.io/badge/Python-3.12-green)
![Aurora](https://img.shields.io/badge/Database-Aurora_PostgreSQL-blue)

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Requisitos Previos](#-requisitos-previos)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación y Configuración](#-instalación-y-configuración)
  - [Paso 1: Clonar el Repositorio](#paso-1-clonar-el-repositorio)
  - [Paso 2: Desplegar Stack 1 (Infraestructura Base)](#paso-2-desplegar-stack-1-infraestructura-base)
  - [Paso 3: Inicializar Base de Datos](#paso-3-inicializar-base-de-datos)
  - [Paso 4: Desplegar Stack 2 (Knowledge Base)](#paso-4-desplegar-stack-2-knowledge-base)
  - [Paso 5: Cargar Documentos](#paso-5-cargar-documentos)
  - [Paso 6: Sincronizar Knowledge Base](#paso-6-sincronizar-knowledge-base)
- [Uso del Sistema](#-uso-del-sistema)
- [Funciones Implementadas](#-funciones-implementadas)
- [Parámetros del Modelo](#-parámetros-del-modelo)
- [Pruebas y Validación](#-pruebas-y-validación)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)

---

## 🎯 Descripción General

**DocSmart RAG System** es un sistema de Retrieval-Augmented Generation (RAG) construido sobre Amazon Bedrock que permite consultar políticas de recursos humanos de manera conversacional e inteligente.

### Características Principales

- ✅ **Infraestructura como Código (IaC)** con Terraform
- ✅ **Base de Datos Vectorial** con Aurora Serverless PostgreSQL + pgvector
- ✅ **Knowledge Base de Bedrock** para almacenamiento de documentos
- ✅ **Búsqueda Híbrida** (semántica + palabras clave)
- ✅ **Interfaz Web** con Streamlit (tema oscuro profesional)
- ✅ **Procesamiento de Lenguaje Natural** con Claude 3.5 Sonnet
- ✅ **Validación de Prompts** para seguridad y categorización
- ✅ **Soporte Multilingüe** (español e inglés)

### Tecnologías Utilizadas

- **AWS Bedrock**: Claude 3.5 Sonnet, Titan Embeddings v2
- **AWS Aurora Serverless v2**: PostgreSQL 15.5 con pgvector
- **AWS S3**: Almacenamiento de documentos
- **Terraform**: Gestión de infraestructura
- **Python 3.12**: Lógica de aplicación
- **Streamlit**: Interfaz de usuario web
- **boto3**: SDK de AWS para Python

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         Usuario Final                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                       │
│                      (app_demo.py)                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     bedrock_utils.py                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │valid_prompt()│  │query_kb()    │  │generate()    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────┬──────────────────┬─────────────────┬─────────────────┘
          │                  │                 │
          ▼                  ▼                 ▼
┌─────────────────┐ ┌─────────────────┐ ┌──────────────────┐
│  AWS Bedrock    │ │  Bedrock        │ │  Bedrock         │
│  Agent Runtime  │ │  Knowledge Base │ │  Runtime         │
│  (Validation)   │ │  (Retrieval)    │ │  (Generation)    │
└─────────────────┘ └────────┬────────┘ └──────────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │    Aurora PostgreSQL         │
              │    + pgvector extension      │
              │                              │
              │  bedrock_integration schema  │
              │  bedrock_kb table            │
              │  1024-dim vectors            │
              └──────────────────────────────┘
                             ▲
                             │
                             │ (Ingestion)
                             │
              ┌──────────────────────────────┐
              │         S3 Bucket            │
              │    (Document Storage)        │
              │                              │
              │  spec-sheets/                │
              │  politica_vacaciones.pdf     │
              │  manual_empleado.docx        │
              └──────────────────────────────┘
```

### Flujo de Datos

1. **Usuario** hace una pregunta en la interfaz Streamlit
2. **valid_prompt()** valida y categoriza la consulta
3. **query_knowledge_base()** busca documentos relevantes en Aurora
4. **Bedrock Knowledge Base** retorna chunks con embeddings similares
5. **generate_response()** genera respuesta usando Claude + contexto
6. **Respuesta** se muestra en la interfaz con fuentes citadas

---

## 📦 Requisitos Previos

### Software Requerido

- **Terraform**: >= 1.0
  ```bash
  terraform --version
  ```

- **AWS CLI**: >= 2.0
  ```bash
  aws --version
  ```

- **Python**: >= 3.11
  ```bash
  python --version
  ```

- **Git**: Para clonar el repositorio
  ```bash
  git --version
  ```

### Credenciales AWS

- Cuenta de AWS con permisos para:
  - VPC, EC2 (Subnets, Security Groups)
  - RDS (Aurora Serverless)
  - S3 (Buckets, Objetos)
  - Bedrock (Knowledge Base, Models)
  - IAM (Roles, Policies)
  - Secrets Manager
  - CloudWatch Logs

- Credenciales configuradas:
  ```bash
  aws configure
  # O usar AWS Academy Learner Lab credentials
  ```

### Modelos de Bedrock Habilitados

Habilitar en AWS Console > Bedrock > Model Access:
- ✅ **Claude 3.5 Sonnet v1** (anthropic.claude-3-5-sonnet-20240620-v1:0)
- ✅ **Titan Embeddings Text v2** (amazon.titan-embed-text-v2:0)

---

## 📁 Estructura del Proyecto

```
docsmart-rag-system/
│
├── stack1/                          # Infraestructura base
│   ├── main.tf                      # VPC, Aurora, S3, IAM
│   ├── variables.tf                 # Variables de configuración
│   ├── outputs.tf                   # Outputs para Stack 2
│   └── terraform.tfvars.example     # Ejemplo de configuración
│
├── stack2/                          # Bedrock Knowledge Base
│   ├── main.tf                      # KB, Data Source, Secrets
│   ├── variables.tf                 # Variables de KB
│   ├── outputs.tf                   # IDs y configuración
│   └── terraform.tfvars.example     # Ejemplo de configuración
│
├── scripts/                         # Scripts de utilidad
│   ├── aurora_init.sql              # Inicialización de DB
│   ├── aurora_verify.sql            # Verificación de setup
│   └── upload_to_s3.py              # Carga de documentos
│
├── spec-sheets/                     # Documentos a indexar
│   └── (tus archivos PDF, DOCX, TXT)
│
├── screenshots/                     # Capturas para entrega
│   └── (capturas de pantalla aquí)
│
├── bedrock_utils.py                 # Funciones principales
├── app_demo.py                      # Interfaz Streamlit
├── config.py                        # Configuración global
├── rag_system.py                    # Sistema RAG (alternativo)
├── requirements.txt                 # Dependencias Python
│
├── temperature_top_p_explanation.md # Documentación de parámetros
├── README_FINAL_PROJECT.md          # Este archivo
└── SCREENSHOT_GUIDE.md              # Guía de capturas
```

---

## 🚀 Instalación y Configuración

### Paso 1: Clonar el Repositorio

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/docsmart-rag-system.git
cd docsmart-rag-system

# Instalar dependencias Python
pip install -r requirements.txt
```

### Paso 2: Desplegar Stack 1 (Infraestructura Base)

**Stack 1** crea: VPC, Aurora Serverless PostgreSQL, S3 Bucket, IAM Roles

```bash
# Navegar a stack1
cd stack1

# Copiar y editar variables
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars

# Editar estos valores:
# - s3_bucket_name: Debe ser único globalmente
# - database_master_password: Contraseña segura (min 8 caracteres)
# - aws_region: Tu región preferida (ej: us-east-1)

# Inicializar Terraform
terraform init

# Revisar plan de despliegue
terraform plan

# Desplegar infraestructura
terraform apply

# Escribir "yes" para confirmar
```

**Tiempo estimado:** 10-15 minutos

**Outputs importantes:**
```bash
# Guardar estos valores para Stack 2
aurora_cluster_endpoint = "docsmart-aurora-cluster.cluster-xxxxx.us-east-1.rds.amazonaws.com"
aurora_cluster_arn = "arn:aws:rds:us-east-1:123456789012:cluster:docsmart-aurora-cluster"
s3_bucket_name = "docsmart-documents-967663481769"
bedrock_kb_role_arn = "arn:aws:iam::123456789012:role/docsmart-bedrock-kb-role"
database_name = "docsmart_kb"
```

### Paso 3: Inicializar Base de Datos

Ejecutar scripts SQL usando **RDS Query Editor** o **psql**:

#### Opción A: AWS Console (Query Editor)

1. Ir a **AWS Console > RDS > Query Editor**
2. Seleccionar cluster `docsmart-aurora-cluster`
3. Autenticarse con credenciales de Stack 1
4. Abrir y ejecutar `scripts/aurora_init.sql`
5. Verificar con `scripts/aurora_verify.sql`

#### Opción B: psql (CLI)

```bash
# Obtener endpoint de Stack 1 output
export DB_ENDPOINT="docsmart-aurora-cluster.cluster-xxxxx.us-east-1.rds.amazonaws.com"
export DB_NAME="docsmart_kb"
export DB_USER="dbadmin"
export DB_PASSWORD="YourSecurePassword123!"

# Conectar y ejecutar
psql -h $DB_ENDPOINT -U $DB_USER -d $DB_NAME -f scripts/aurora_init.sql

# Verificar
psql -h $DB_ENDPOINT -U $DB_USER -d $DB_NAME -f scripts/aurora_verify.sql
```

**Verificación exitosa:**
```
✓ pgvector is installed
✓ Schema exists
✓ bedrock_kb table
✓ Required indexes (4)
✓ Search function
✓ Monitoring views
✓✓✓ DATABASE IS READY FOR BEDROCK KNOWLEDGE BASE ✓✓✓
```

### Paso 4: Desplegar Stack 2 (Knowledge Base)

**Stack 2** crea: Bedrock Knowledge Base, Data Source (S3), Secrets Manager

```bash
# Navegar a stack2
cd ../stack2

# Copiar y editar variables
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars

# IMPORTANTE: Usar los outputs de Stack 1
# - s3_bucket_name: De Stack 1 output
# - aurora_cluster_arn: De Stack 1 output
# - database_name: De Stack 1 output
# - database_master_username: Mismo que Stack 1
# - database_master_password: Mismo que Stack 1
# - bedrock_kb_role_name: De Stack 1 output

# Inicializar Terraform
terraform init

# Revisar plan
terraform plan

# Desplegar Knowledge Base
terraform apply

# Escribir "yes" para confirmar
```

**Tiempo estimado:** 5-10 minutos

**Outputs importantes:**
```bash
knowledge_base_id = "ABCDEFGHIJ"
data_source_id = "KLMNOPQRST"
sync_data_source_command = "aws bedrock-agent start-ingestion-job ..."
```

### Paso 5: Cargar Documentos

Subir documentos HR a S3 para indexación:

```bash
# Volver al directorio raíz
cd ..

# Agregar tus documentos a spec-sheets/
cp /path/to/your/politica_vacaciones.pdf spec-sheets/
cp /path/to/your/manual_empleado.docx spec-sheets/

# Editar script de carga
nano scripts/upload_to_s3.py
# Actualizar BUCKET_NAME con tu bucket de Stack 1

# Ejecutar script de carga
python scripts/upload_to_s3.py
```

**Output esperado:**
```
======================================================================
Starting upload from 'spec-sheets' to s3://docsmart-documents-967663481769/
======================================================================

Found 3 file(s) to upload.

  Uploading politica_vacaciones.pdf (0.25 MB)... ✓
  Uploading manual_empleado.docx (0.50 MB)... ✓
  Uploading beneficios_empresa.txt (0.05 MB)... ✓

======================================================================
Upload Summary:
  ✓ Successful: 3
  Total files: 3
======================================================================
```

### Paso 6: Sincronizar Knowledge Base

Indexar documentos en Bedrock Knowledge Base:

#### Opción A: AWS CLI (Recomendado)

```bash
# Usar comando de Stack 2 output
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id ABCDEFGHIJ \
  --data-source-id KLMNOPQRST \
  --region us-east-1

# Monitorear progreso
aws bedrock-agent list-ingestion-jobs \
  --knowledge-base-id ABCDEFGHIJ \
  --data-source-id KLMNOPQRST \
  --region us-east-1
```

#### Opción B: AWS Console

1. Ir a **AWS Console > Bedrock > Knowledge Bases**
2. Seleccionar `docsmart-knowledge-base`
3. Ir a **Data Sources**
4. Clic en `docsmart-s3-data-source`
5. Clic en **Sync**
6. Esperar a que el estado sea `COMPLETE`

**Tiempo de sincronización:** 2-5 minutos (depende del tamaño de documentos)

**Verificación:**
```bash
# Estado del job debe ser "COMPLETE"
{
  "ingestionJobId": "xxxxx",
  "status": "COMPLETE",
  "statistics": {
    "numberOfDocumentsScanned": 3,
    "numberOfNewDocumentsIndexed": 3,
    "numberOfModifiedDocumentsIndexed": 0,
    "numberOfDocumentsDeleted": 0,
    "numberOfDocumentsFailed": 0
  }
}
```

---

## 🎮 Uso del Sistema

### Configurar Variables de Entorno

```bash
# Crear archivo .env en el directorio raíz
cat > .env << EOF
AWS_REGION=us-east-1
KNOWLEDGE_BASE_ID=ABCDEFGHIJ
EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0
LLM_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
EOF
```

### Lanzar Interfaz Web

```bash
# Ejecutar Streamlit
python -m streamlit run app_demo.py --server.port 8501

# Abrir navegador en:
# http://localhost:8501
```

### Probar Consultas

Ejemplos de preguntas:

```
✅ "¿Cuántos días de vacaciones tengo?"
✅ "¿A mí cuánto me toca? Estoy hace 1 año"
✅ "¿Cómo solicito vacaciones?"
✅ "¿Qué beneficios tiene la empresa?"
✅ "¿Cuál es el proceso de renovación de contrato?"
```

### Usar desde Python

```python
from bedrock_utils import rag_pipeline

# Ejecutar pipeline completo
result = rag_pipeline(
    user_query="¿Cuántos días de vacaciones tengo?",
    knowledge_base_id="ABCDEFGHIJ",
    temperature=0.3,
    top_p=0.9
)

print(result['final_response'])
print(f"\nFuentes consultadas: {len(result['retrieval']['results'])}")
```

---

## ⚙️ Funciones Implementadas

### 1. `query_knowledge_base()`

**Ubicación:** `bedrock_utils.py`

Consulta Bedrock Knowledge Base para recuperar documentos relevantes.

```python
def query_knowledge_base(
    query: str,
    knowledge_base_id: str = KNOWLEDGE_BASE_ID,
    max_results: int = 5,
    score_threshold: float = 0.1
) -> Dict[str, Any]:
    """
    Retrieves relevant documents from Bedrock Knowledge Base.
    
    Returns:
        {
            'results': List[Dict],  # Retrieved documents
            'count': int,           # Number of results
            'query': str            # Original query
        }
    """
```

**Características:**
- ✅ Búsqueda híbrida (semántica + keywords)
- ✅ Filtrado por score threshold
- ✅ Metadata de documentos incluida
- ✅ Manejo de errores AWS

### 2. `generate_response()`

**Ubicación:** `bedrock_utils.py`

Genera respuesta usando Claude 3.5 Sonnet con contexto recuperado.

```python
def generate_response(
    query: str,
    context_documents: List[Dict[str, Any]],
    model_id: str = LLM_MODEL_ID,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 1000
) -> Dict[str, Any]:
    """
    Generates response using Bedrock LLM with retrieved context.
    
    Returns:
        {
            'response': str,         # Generated text
            'model_id': str,         # Model used
            'sources': List[Dict],   # Source documents
            'usage': Dict            # Token usage stats
        }
    """
```

**Características:**
- ✅ Prompt engineering con sistema y contexto
- ✅ Parámetros configurables (temperature, top_p)
- ✅ Citación de fuentes
- ✅ Estadísticas de tokens

### 3. `valid_prompt()`

**Ubicación:** `bedrock_utils.py`

Valida y categoriza prompts del usuario.

```python
def valid_prompt(user_prompt: str) -> Dict[str, Any]:
    """
    Validates and categorizes user prompts.
    
    Returns:
        {
            'is_valid': bool,         # Prompt is acceptable
            'category': str,          # vacation, benefits, etc.
            'confidence': float,      # 0.0 - 1.0
            'entities': Dict,         # Extracted numbers, dates
            'recommendation': str,    # process, reject, clarify
            'reason': str             # Explanation
        }
    """
```

**Categorías detectadas:**
- `vacation` - Vacaciones, días libres
- `benefits` - Beneficios, seguros
- `salary` - Salario, compensación
- `contract` - Contratos, renovación
- `attendance` - Asistencia, horarios
- `general` - Consultas generales

---

## 🎛️ Parámetros del Modelo

Ver documentación completa en: `temperature_top_p_explanation.md`

### Temperature

Controla la aleatoriedad de las respuestas:

| Valor | Comportamiento | Uso |
|-------|----------------|-----|
| 0.0 - 0.3 | Determinista, preciso | Políticas, cálculos |
| 0.4 - 0.7 | Balanceado | Conversacional |
| 0.8 - 1.0 | Creativo, variado | Brainstorming |

### Top_p

Controla la diversidad del vocabulario:

| Valor | Comportamiento | Uso |
|-------|----------------|-----|
| 0.1 - 0.5 | Restrictivo | Respuestas técnicas |
| 0.6 - 0.9 | Balanceado | General |
| 0.9 - 1.0 | Diverso | Conversacional |

### Configuración Recomendada para DocSmart

```python
# Para consultas de políticas HR
OPTIMAL_CONFIG = {
    'temperature': 0.3,  # Precisión factual
    'top_p': 0.9,        # Lenguaje natural
    'max_tokens': 1000   # Respuestas completas
}
```

---

## 🧪 Pruebas y Validación

### Test de Conexión AWS

```bash
python test_aws_credentials.py
```

**Output esperado:**
```
✓ STS credentials valid
✓ S3 bucket accessible
✓ Bedrock models available
✓ Knowledge Base accessible
```

### Test de Funciones

```bash
# Ejecutar tests de bedrock_utils
python -c "from bedrock_utils import valid_prompt; print(valid_prompt('¿Cuántos días de vacaciones?'))"
```

### Test de RAG Pipeline

```python
from bedrock_utils import rag_pipeline

result = rag_pipeline(
    user_query="¿Cuántos días de vacaciones tengo si llevo 1 año?",
    temperature=0.3
)

assert result['validation']['is_valid'] == True
assert result['validation']['category'] == 'vacation'
assert result['retrieval']['count'] > 0
assert len(result['generation']['response']) > 0
print("✓ All tests passed")
```

---

## 📸 Capturas de Pantalla

Ver guía completa en: `screenshots/SCREENSHOT_GUIDE.md`

### Checklist de Capturas Requeridas

#### Creación de Infraestructura Base (Stack 1)

- [ ] `terraform_apply_stack1_output.png` - Output completo de `terraform apply` Stack 1
- [ ] `aws_console_vpc.png` - VPC creada en AWS Console
- [ ] `aws_console_aurora_cluster.png` - Aurora cluster en RDS Console
- [ ] `aws_console_s3_bucket.png` - S3 bucket creado

#### Implementación de Base de Conocimientos (Stack 2)

- [ ] `terraform_apply_stack2_output.png` - Output de `terraform apply` Stack 2
- [ ] `aws_console_knowledge_base.png` - Knowledge Base en Bedrock Console
- [ ] `aws_console_data_source.png` - Data Source configurada

#### Sincronización de Datos

- [ ] `s3_documents_uploaded.png` - Documentos en S3 bucket
- [ ] `knowledge_base_sync_started.png` - Ingestion job iniciado
- [ ] `knowledge_base_sync_complete.png` - Ingestion job completado
- [ ] `aurora_query_editor_verification.png` - Verificación de datos en Aurora

#### Integración de Python con Bedrock

- [ ] `bedrock_utils_query_knowledge_base.png` - Código de `query_knowledge_base()`
- [ ] `bedrock_utils_generate_response.png` - Código de `generate_response()`
- [ ] `bedrock_utils_valid_prompt.png` - Código de `valid_prompt()`

#### Parámetros del Modelo

- [ ] `model_parameters_code.png` - Código mostrando temperature y top_p
- [ ] `model_parameters_explanation_doc.png` - Sección del documento de explicación

#### Aplicación de Chat Completa

- [ ] `streamlit_app_interface.png` - Interfaz completa de Streamlit
- [ ] `chat_example_vacation_query.png` - Consulta sobre vacaciones
- [ ] `chat_example_benefits_query.png` - Consulta sobre beneficios
- [ ] `chat_example_sources_cited.png` - Respuesta con fuentes citadas

---

## 🔧 Solución de Problemas

### Problema: Terraform Apply Falla

**Error:** `Error creating RDS Cluster: InvalidParameterValue`

**Solución:**
```bash
# Verificar password cumple requisitos (min 8 caracteres)
# Verificar región soporta Aurora Serverless v2
# Verificar quotas de cuenta AWS
```

### Problema: Conexión a Aurora Falla

**Error:** `could not connect to server: Connection timed out`

**Solución:**
```bash
# 1. Verificar Security Group permite puerto 5432
# 2. Verificar subnet group tiene subnets privadas
# 3. Usar Query Editor en AWS Console en su lugar
```

### Problema: Knowledge Base Sync Falla

**Error:** `Ingestion job failed with status: FAILED`

**Solución:**
```bash
# 1. Verificar documentos en S3 tienen formatos soportados
# 2. Verificar IAM role tiene permisos de S3 y Secrets Manager
# 3. Verificar Aurora cluster está disponible
# 4. Revisar CloudWatch Logs para detalles
```

### Problema: Bedrock Model Not Found

**Error:** `ValidationException: The provided model identifier is invalid`

**Solución:**
```bash
# 1. Habilitar model access en AWS Console > Bedrock > Model Access
# 2. Verificar modelo disponible en tu región:
aws bedrock list-foundation-models --region us-east-1 | grep claude-3-5-sonnet

# 3. Usar modelo correcto en config.py
LLM_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
```

### Problema: Empty Results from Knowledge Base

**Error:** `No documents found` o `count: 0`

**Solución:**
```bash
# 1. Verificar sincronización completada
aws bedrock-agent list-ingestion-jobs --knowledge-base-id ABCDEFGHIJ

# 2. Reducir score_threshold
query_knowledge_base(query, score_threshold=0.1)

# 3. Verificar datos en Aurora
psql -h $DB_ENDPOINT -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) FROM bedrock_integration.bedrock_kb;"
```

---

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte del **AWS AI Engineer Nanodegree Program** de Udacity.

### Autor

- **Estudiante:** [Tu Nombre]
- **Programa:** AWS AI Engineer Nanodegree
- **Fecha:** Diciembre 2025

### Agradecimientos

- **Udacity** por el programa educativo
- **Amazon Web Services** por Bedrock y servicios cloud
- **Anthropic** por Claude 3.5 Sonnet

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Aurora PostgreSQL with pgvector](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Claude 3.5 Sonnet Documentation](https://docs.anthropic.com/claude/docs)

### Tutoriales y Guías

- [Building RAG Systems with Bedrock](https://aws.amazon.com/blogs/machine-learning/building-rag-systems/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [pgvector for PostgreSQL](https://github.com/pgvector/pgvector)

---

## 📞 Contacto y Soporte

Para preguntas sobre este proyecto:

- **Email:** [tu-email@example.com]
- **GitHub Issues:** [Link al repositorio]
- **Udacity Workspace:** [Link al workspace]

---

**🎓 Este proyecto fue desarrollado como requisito para el AWS AI Engineer Nanodegree Program de Udacity.**

**Última actualización:** Diciembre 2025
