# 🚀 Guía de Instalación Detallada - DocSmart RAG System

## 📋 Índice
1. [Prerrequisitos](#prerrequisitos)
2. [Configuración de AWS](#configuración-de-aws)
3. [Instalación Local](#instalación-local)
4. [Despliegue de Infraestructura](#despliegue-de-infraestructura)
5. [Verificación](#verificación)
6. [Troubleshooting](#troubleshooting)

---

## 1️⃣ Prerrequisitos

### Cuentas y Servicios

#### AWS Account
- Cuenta de AWS activa
- Acceso a Amazon Bedrock
- Permisos para crear:
  - Aurora PostgreSQL
  - S3 Buckets
  - VPC y Networking
  - IAM Roles

#### Software Local
- **Python 3.9 o superior**
  ```bash
  python --version  # Debe ser >= 3.9
  ```

- **Git**
  ```bash
  git --version
  ```

- **Terraform** (>= 1.0)
  ```bash
  # Descargar de: https://www.terraform.io/downloads
  terraform version
  ```

- **AWS CLI**
  ```bash
  # Instalar:
  # Windows: https://aws.amazon.com/cli/
  # Linux: sudo apt install awscli
  # Mac: brew install awscli
  
  aws --version
  ```

### Hardware Recomendado
- **RAM**: Mínimo 4GB (8GB recomendado)
- **Disco**: 5GB libres
- **Internet**: Conexión estable

---

## 2️⃣ Configuración de AWS

### Paso 1: Configurar AWS CLI

```bash
aws configure
```

Ingresa:
- **AWS Access Key ID**: `AKIAIOSFODNN7EXAMPLE`
- **AWS Secret Access Key**: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
- **Default region**: `us-west-2`
- **Default output**: `json`

**Verificar configuración:**
```bash
aws sts get-caller-identity
```

### Paso 2: Habilitar Amazon Bedrock

1. **Ir a AWS Console** → Buscar "Bedrock"
2. **Ir a "Model access"** en el menú lateral
3. **Click en "Modify model access"**
4. **Seleccionar modelos**:
   - ✅ `Amazon Titan Embeddings G1 - Text v2`
   - ✅ `Anthropic Claude 3.5 Sonnet`
5. **Click "Request model access"**
6. **Esperar aprobación** (típicamente instantánea)

**Verificar acceso:**
```bash
aws bedrock list-foundation-models --region us-west-2
```

### Paso 3: Crear S3 Bucket (Opcional - Terraform lo hará)

Si quieres crearlo manualmente:
```bash
aws s3 mb s3://docsmart-documents-YOUR-ACCOUNT-ID --region us-west-2
```

---

## 3️⃣ Instalación Local

### Windows

#### Opción A: Script Automático
```cmd
cd docsmart-rag-system
setup.bat
```

#### Opción B: Manual
```cmd
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate.bat

# 2. Actualizar pip
python -m pip install --upgrade pip

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar configuración
copy .env.example .env

# 5. Editar .env con tu editor favorito
notepad .env
```

### Linux / macOS

#### Opción A: Script Automático
```bash
cd docsmart-rag-system
chmod +x setup.sh
./setup.sh
```

#### Opción B: Manual
```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Actualizar pip
pip install --upgrade pip

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar configuración
cp .env.example .env

# 5. Editar .env
nano .env  # o vim .env
```

### Configurar .env

Edita `.env` con tus credenciales:

```env
# AWS Configuration
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# S3 Configuration
S3_BUCKET_NAME=docsmart-documents-123456789012

# Aurora PostgreSQL Configuration (llenar después de Terraform)
DB_HOST=
DB_PORT=5432
DB_NAME=docsmart_db
DB_USER=postgres
DB_PASSWORD=TuPasswordSeguro123!

# Bedrock Configuration
BEDROCK_EMBEDDING_MODEL=amazon.titan-embed-text-v2:0
BEDROCK_LLM_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0

# Application Configuration
MAX_TOKENS=4096
TEMPERATURE=0.7
TOP_P=0.9
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5

# Security
ENABLE_GUARDRAILS=true
MAX_QUERY_LENGTH=2000
ALLOWED_FILE_TYPES=pdf,docx,txt,md
```

---

## 4️⃣ Despliegue de Infraestructura

### Paso 1: Preparar Terraform

```bash
cd terraform
terraform init
```

**Salida esperada:**
```
Initializing provider plugins...
- Reusing previous version of hashicorp/aws from the dependency lock file
- Using previously-installed hashicorp/aws v5.x.x

Terraform has been successfully initialized!
```

### Paso 2: Revisar Plan

```bash
terraform plan -var="db_master_password=TuPasswordSeguro123!"
```

Esto mostrará todos los recursos que se crearán:
- VPC con subnets públicas y privadas
- Security Groups
- Aurora PostgreSQL Serverless cluster
- S3 Bucket con encriptación
- Parameter Groups

### Paso 3: Aplicar Infraestructura

```bash
terraform apply -var="db_master_password=TuPasswordSeguro123!"
```

Terraform preguntará confirmación:
```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: 
```

Escribe `yes` y presiona Enter.

**Tiempo estimado:** 10-15 minutos

### Paso 4: Guardar Outputs

```bash
terraform output > ../terraform_outputs.txt
cd ..
cat terraform_outputs.txt
```

**Outputs importantes:**
```
aurora_cluster_endpoint = "docsmart-dev-aurora-cluster.cluster-xxxxx.us-west-2.rds.amazonaws.com"
s3_bucket_name = "docsmart-dev-documents-123456789012"
database_connection_string = "postgresql://postgres:PASSWORD@endpoint:5432/docsmart_db"
```

### Paso 5: Actualizar .env con Outputs

Copia el endpoint de Aurora al `.env`:

```env
DB_HOST=docsmart-dev-aurora-cluster.cluster-xxxxx.us-west-2.rds.amazonaws.com
S3_BUCKET_NAME=docsmart-dev-documents-123456789012
DB_PASSWORD=TuPasswordSeguro123!
```

---

## 5️⃣ Inicialización de Base de Datos

### Paso 1: Verificar Conexión

```bash
# Test de conexión con psql (opcional)
psql -h YOUR_AURORA_ENDPOINT -U postgres -d docsmart_db
# Ingresa password cuando se solicite
# Si conecta exitosamente, escribir \q para salir
```

### Paso 2: Inicializar Schema

```bash
python cli.py setup
```

**Salida esperada:**
```
Initializing database...
Connected to Aurora PostgreSQL successfully
✓ Database initialized successfully
```

Esto crea:
- Extensión `pgvector`
- Tabla `documents` con campos:
  - id, file_name, text, embedding, metadata
- Índice vectorial IVFFlat
- Tabla `query_logs` para analytics

### Paso 3: Verificar Schema

```bash
# Conectar a DB
psql -h YOUR_AURORA_ENDPOINT -U postgres -d docsmart_db

# Listar tablas
\dt

# Ver estructura de tabla documents
\d documents

# Salir
\q
```

---

## 6️⃣ Verificación del Sistema

### Test 1: Ingestar Documento de Prueba

Crea un documento de prueba:

```bash
mkdir -p sample_docs
```

Crea `sample_docs/test.txt`:
```text
Política de Vacaciones

Los empleados tienen derecho a 15 días de vacaciones al año.
Los días de vacaciones se acumulan mensualmente.
Se debe solicitar vacaciones con 2 semanas de anticipación.
```

Ingesta el documento:
```bash
python cli.py ingest -f sample_docs/test.txt
```

**Salida esperada:**
```
============================================================
Ingesting: sample_docs/test.txt
============================================================
Processing document...
Created 1 chunks
Generating embeddings...
Generated 1 embeddings
Storing in database...
Inserted 1 documents successfully

✓ Successfully ingested in 3.45 seconds
============================================================
```

### Test 2: Realizar Consulta

```bash
python cli.py query "¿Cuántos días de vacaciones tengo?"
```

**Salida esperada:**
```
🔍 Query: ¿Cuántos días de vacaciones tengo?

Searching knowledge base...

================================================================================
ANSWER
================================================================================
Según la política de vacaciones, los empleados tienen derecho a 15 días de 
vacaciones al año. Estos días se acumulan mensualmente.

================================================================================
SOURCES
================================================================================

[1] test.txt (Similarity: 0.892)
    Política de Vacaciones Los empleados tienen derecho a 15 días de...

================================================================================
METADATA
================================================================================
Total Time: 2847ms
Sources Used: 1
Model: anthropic.claude-3-5-sonnet-20241022-v2:0
```

### Test 3: Ver Estadísticas

```bash
python cli.py stats
```

**Salida esperada:**
```
================================================================================
SYSTEM STATISTICS
================================================================================

Total Chunks: 1
Total Files: 1

Indexed Files:
  - test.txt: 1 chunks
```

### Test 4: Lanzar Aplicación Web

```bash
streamlit run app.py
```

**Salida esperada:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

Abre `http://localhost:8501` en tu navegador.

**Verificaciones en la UI:**
- ✅ La página carga sin errores
- ✅ Puedes navegar entre pestañas
- ✅ Puedes hacer una consulta en el chat
- ✅ Puedes subir un documento en "Ingestar Documentos"
- ✅ Puedes ver estadísticas

---

## 7️⃣ Troubleshooting

### Problema: "ModuleNotFoundError"

```
ModuleNotFoundError: No module named 'boto3'
```

**Solución:**
```bash
# Asegúrate de estar en el entorno virtual
# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: "Error connecting to database"

```
Error connecting to database: could not connect to server
```

**Soluciones:**

1. **Verificar que Aurora está corriendo:**
   ```bash
   aws rds describe-db-clusters --db-cluster-identifier docsmart-dev-aurora-cluster
   ```
   Status debe ser "available"

2. **Verificar endpoint en .env:**
   ```bash
   cat .env | grep DB_HOST
   ```

3. **Verificar Security Group permite tu IP:**
   - Ve a AWS Console → RDS → Security Groups
   - Agrega tu IP actual a ingress rules

4. **Test de conectividad:**
   ```bash
   telnet YOUR_ENDPOINT 5432
   ```

### Problema: "AccessDenied" en Bedrock

```
AccessDeniedException: You don't have access to the model
```

**Solución:**
1. Ve a AWS Console → Bedrock
2. "Model access" → Verifica que los modelos estén "Access granted"
3. Si no, solicita acceso nuevamente
4. Espera 5-10 minutos y reintenta

### Problema: Terraform "already exists"

```
Error: resource already exists
```

**Solución:**
```bash
# Importar recursos existentes
terraform import aws_s3_bucket.documents docsmart-dev-documents-123

# O destruir y recrear
terraform destroy
terraform apply
```

### Problema: "Out of memory" durante ingesta

```
MemoryError: Unable to allocate array
```

**Solución:**
1. Reducir CHUNK_SIZE en .env:
   ```env
   CHUNK_SIZE=500
   ```

2. Procesar documentos en batches más pequeños

3. Aumentar memoria disponible para Python

### Problema: Respuestas de baja calidad

**Soluciones:**

1. **Aumentar TOP_K:**
   ```env
   TOP_K_RESULTS=10
   ```

2. **Mejorar calidad de documentos:**
   - Asegurar PDFs son text-based, no escaneados
   - Limpiar documentos antes de ingestar

3. **Ajustar prompts:**
   Modificar `system_role` en `rag_system.py`

### Problema: S3 Upload falla

```
S3UploadFailedError: Failed to upload
```

**Soluciones:**

1. **Verificar permisos IAM:**
   ```bash
   aws s3 ls s3://your-bucket-name/
   ```

2. **Verificar bucket existe:**
   ```bash
   aws s3api head-bucket --bucket your-bucket-name
   ```

3. **Deshabilitar S3 upload temporalmente:**
   ```bash
   python cli.py ingest -f doc.pdf --no-s3
   ```

---

## 8️⃣ Configuraciones Avanzadas

### Multi-Region Setup

Para alta disponibilidad, despliega en múltiples regiones:

```bash
# Region 1
cd terraform
terraform apply -var="aws_region=us-west-2"

# Region 2
terraform apply -var="aws_region=us-east-1"
```

### Custom VPC

Si ya tienes una VPC, modifica `terraform/network.tf`:

```hcl
# Comentar creación de VPC
# resource "aws_vpc" "main" { ... }

# Usar VPC existente
data "aws_vpc" "existing" {
  id = "vpc-xxxxxxxxx"
}
```

### Backup Automático

Configurar snapshots automáticos:

```hcl
# terraform/aurora.tf
resource "aws_rds_cluster" "aurora" {
  backup_retention_period   = 30  # 30 días
  preferred_backup_window   = "03:00-04:00"
}
```

---

## 9️⃣ Checklist Final

Antes de usar en producción:

- [ ] ✅ Infraestructura desplegada exitosamente
- [ ] ✅ Base de datos inicializada
- [ ] ✅ Documento de prueba ingestado
- [ ] ✅ Consulta de prueba funciona
- [ ] ✅ Aplicación web carga correctamente
- [ ] ✅ Credenciales en .env (NO en git)
- [ ] ✅ Security Groups configurados
- [ ] ✅ Backups habilitados
- [ ] ✅ CloudWatch logs funcionando
- [ ] ✅ Documentación leída

---

## 🎉 ¡Felicitaciones!

Tu sistema DocSmart RAG está listo para usar.

**Próximos pasos:**
1. Ingesta tus documentos reales
2. Personaliza system roles para tu caso de uso
3. Configura monitoreo y alertas
4. Comparte con tu equipo

**Recursos:**
- [README.md](README.md) - Documentación completa
- [EXAMPLES.md](EXAMPLES.md) - Ejemplos de uso
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detalles técnicos

**Soporte:**
- GitHub Issues: [URL]
- Documentation: [URL]
- Email: support@docsmart.ai

---

**¡Bienvenido a DocSmart! 🚀📚**
