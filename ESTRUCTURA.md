# 📁 Estructura del Proyecto DocSmart

Esta guía describe la estructura organizacional del repositorio DocSmart RAG System para el proyecto final del AWS AI Engineer Nanodegree.

---

## 📊 Estructura de Carpetas

```
docsmart-rag-system/
│
├── 📄 README.md                       # Documentación principal del proyecto
├── 📄 requirements.txt                # Dependencias Python
├── 📄 .env.example                    # Template de variables de entorno
├── 📄 .gitignore                      # Archivos excluidos de Git
├── 📄 LICENSE                         # Licencia del proyecto
│
├── 🐍 bedrock_utils.py                # ⭐ Funciones principales Bedrock (3 requeridas)
├── 🐍 app_demo.py                     # ⭐ Aplicación Streamlit de chat
├── 🐍 quick_credentials.py            # Setup rápido de credenciales AWS
│
├── 📁 stack1/                         # ⭐ TERRAFORM - Infraestructura Base
│   ├── main.tf                        # VPC, Aurora, S3, IAM, Security Groups
│   ├── variables.tf                   # Variables de entrada
│   ├── outputs.tf                     # Outputs (ARNs, endpoints, IDs)
│   ├── terraform.tfvars.example       # Template de valores
│   └── README.md                      # Documentación de Stack 1
│
├── 📁 stack2/                         # ⭐ TERRAFORM - Bedrock Knowledge Base
│   ├── main.tf                        # Knowledge Base, Data Source, Secrets
│   ├── variables.tf                   # Variables de entrada
│   ├── outputs.tf                     # Outputs (KB ID, Data Source ID)
│   ├── terraform.tfvars.example       # Template de valores
│   └── README.md                      # Documentación de Stack 2
│
├── 📁 scripts/                        # Scripts de utilidad
│   ├── aurora_init.sql                # ⭐ Inicialización PostgreSQL + pgvector
│   ├── aurora_verify.sql              # Verificación de base de datos
│   ├── upload_to_s3.py                # Script para subir documentos a S3
│   └── README.md                      # Documentación de scripts
│
├── 📁 screenshots/                    # ⭐ CAPTURAS REQUERIDAS (30 total)
│   ├── SCREENSHOT_GUIDE.md            # Guía detallada de las 30 capturas
│   ├── 01_terraform_apply_stack1_output.jpeg
│   ├── 02_aws_console_vpc.jpeg
│   ├── 03_aws_console_aurora.jpeg
│   └── ... (27 más)
│
├── 📁 docs/                           # Documentación completa
│   ├── README_FINAL_PROJECT.md        # Documentación detallada del proyecto
│   ├── ARCHITECTURE.md                # Arquitectura del sistema
│   ├── CREDENTIALS_SETUP.md           # Configuración de credenciales
│   ├── QUICK_START.md                 # Guía rápida de inicio
│   ├── FINAL_PROJECT_CHECKLIST.md     # Checklist de entrega
│   ├── temperature_top_p_explanation.md  # ⭐ Explicación parámetros LLM
│   └── PRESENTACION_COMPLETA.md       # Guía de presentación
│
├── 📁 spec-sheets/                    # ⭐ DOCUMENTOS FUENTE (subir a S3)
│   ├── employee_handbook.pdf
│   ├── vacation_policy.pdf
│   ├── benefits_guide.pdf
│   └── ... (tus documentos aquí)
│
├── 📁 config/                         # Configuración y utilidades
│   ├── setup_env.ps1                  # Setup de entorno PowerShell
│   ├── load_credentials.ps1           # Carga de credenciales desde .env
│   └── terraform.ps1                  # Wrapper de Terraform (opcional)
│
├── 📁 tests/                          # Scripts de prueba
│   ├── test_bedrock.py                # Pruebas de funciones Bedrock
│   ├── test_aws_credentials.py        # Validación de credenciales
│   └── README.md                      # Documentación de tests
│
├── 📁 .backups/                       # Backups automáticos (ignorado por Git)
│   └── .env.backup.*
│
└── 📁 deprecated/                     # Código antiguo/deprecado (ignorado por Git)
    └── (archivos antiguos)
```

---

## 📦 Archivos Principales

### Raíz del Proyecto

| Archivo | Descripción | Requerido |
|---------|-------------|-----------|
| `README.md` | Documentación principal, quick start | ✅ Sí |
| `bedrock_utils.py` | 3 funciones requeridas por Udacity | ⭐ CRÍTICO |
| `app_demo.py` | Aplicación Streamlit de chat | ⭐ CRÍTICO |
| `quick_credentials.py` | Setup de credenciales AWS Academy | ✅ Sí |
| `requirements.txt` | Dependencias Python (boto3, streamlit) | ✅ Sí |
| `.env.example` | Template de variables de entorno | ✅ Sí |
| `.gitignore` | Excluir .env, venv, *.tfstate | ✅ Sí |
| `LICENSE` | Licencia del proyecto | Recomendado |

### Stack 1 - Infraestructura Base

| Archivo | Propósito | Recursos |
|---------|-----------|----------|
| `main.tf` | Definición de infraestructura | VPC, Subnets, Aurora, S3, IAM, SG |
| `variables.tf` | Variables de entrada | region, vpc_cidr, project_name |
| `outputs.tf` | Salidas del stack | vpc_id, aurora_endpoint, s3_bucket |
| `terraform.tfvars` | Valores de variables | (usuario crea desde .example) |

### Stack 2 - Knowledge Base

| Archivo | Propósito | Recursos |
|---------|-----------|----------|
| `main.tf` | Bedrock Knowledge Base | KB, Data Source, Secrets Manager |
| `variables.tf` | Variables de entrada | kb_name, embedding_model |
| `outputs.tf` | Salidas del stack | knowledge_base_id, data_source_id |
| `terraform.tfvars` | Valores de variables | Incluye outputs de Stack 1 |

### Scripts de Utilidad

| Script | Propósito | Cuándo Usar |
|--------|-----------|-------------|
| `aurora_init.sql` | Inicializar PostgreSQL + pgvector | Después de terraform apply stack1 |
| `aurora_verify.sql` | Verificar configuración de BD | Después de init, antes de Stack 2 |
| `upload_to_s3.py` | Subir documentos a S3 | Antes de sincronizar KB |

### Documentación

| Documento | Contenido | Tamaño Aprox |
|-----------|-----------|--------------|
| `README_FINAL_PROJECT.md` | Documentación completa del proyecto | 5000+ palabras |
| `ARCHITECTURE.md` | Diagrama y explicación de arquitectura | 2000+ palabras |
| `CREDENTIALS_SETUP.md` | Guía de configuración AWS | 1500+ palabras |
| `temperature_top_p_explanation.md` | ⭐ Explicación de parámetros LLM | 7000+ palabras |
| `SCREENSHOT_GUIDE.md` | Guía de las 30 capturas requeridas | 3000+ palabras |

---

## 🎯 Archivos Críticos para Entrega

### Obligatorios según Rubric de Udacity

1. ⭐ **bedrock_utils.py**
   - Función `query_knowledge_base()`
   - Función `generate_response()`
   - Función `valid_prompt()`

2. ⭐ **stack1/main.tf**
   - VPC con 4 subnets (2 públicas, 2 privadas)
   - Aurora PostgreSQL Serverless v2 con pgvector
   - S3 bucket para documentos
   - IAM roles y policies

3. ⭐ **stack2/main.tf**
   - Bedrock Knowledge Base
   - Data Source apuntando a S3
   - Secrets Manager para credenciales de BD

4. ⭐ **scripts/aurora_init.sql**
   - CREATE EXTENSION pgvector
   - CREATE SCHEMA bedrock_integration
   - CREATE TABLE bedrock_kb.bedrock_integration.bedrock_kb
   - CREATE INDEX usando HNSW

5. ⭐ **docs/temperature_top_p_explanation.md**
   - Explicación de temperature (0.0 - 1.0)
   - Explicación de top_p (0.0 - 1.0)
   - Ejemplos prácticos con DocSmart
   - Recomendaciones por caso de uso

6. ⭐ **screenshots/** (30 capturas)
   - Infrastructure (6): Terraform outputs, VPC, Aurora, S3, IAM
   - Knowledge Base (4): Stack 2 outputs, Bedrock console
   - Data Sync (5): S3 objects, ingestion jobs, Aurora data
   - Python Integration (5): Código + ejecución de las 3 funciones
   - Model Parameters (3): Temperature, top_p en UI
   - Chat Application (7): Interfaz, consultas, respuestas, fuentes

---

## 🚫 Archivos Excluidos de Git

### Por Seguridad

- `.env` - **NUNCA** commitear credenciales
- `.backups/.env.backup.*` - Backups de credenciales
- `aws_credentials.txt` - Credenciales en texto plano

### Por Tamaño/Temporalidad

- `venv/` - Entorno virtual Python (recrear con requirements.txt)
- `__pycache__/` - Compilados Python
- `*.tfstate` - Estado de Terraform (contiene outputs sensibles)
- `.terraform/` - Providers de Terraform (descargar con terraform init)

### Por Obsolescencia

- `deprecated/` - Código antiguo no funcional
- `.backups/` - Backups automáticos

---

## 📋 Checklist de Estructura

Antes de crear el ZIP final, verificar:

### ✅ Raíz Limpia
- [ ] Solo 9 archivos en raíz (README, bedrock_utils, app_demo, quick_credentials, requirements, .env.example, .gitignore, LICENSE)
- [ ] No hay archivos *.pyc, *.db, *.html deprecados
- [ ] No hay backups de .env en raíz

### ✅ Terraform Completo
- [ ] stack1/main.tf con VPC + Aurora + S3 + IAM
- [ ] stack1/outputs.tf con todos los ARNs y endpoints
- [ ] stack2/main.tf con Knowledge Base
- [ ] Ambos tienen terraform.tfvars.example

### ✅ Scripts Funcionales
- [ ] scripts/aurora_init.sql con pgvector + schema
- [ ] scripts/aurora_verify.sql para validación
- [ ] scripts/upload_to_s3.py funcional

### ✅ Documentación Completa
- [ ] README.md principal con quick start
- [ ] docs/README_FINAL_PROJECT.md detallado
- [ ] docs/temperature_top_p_explanation.md (7000+ palabras)
- [ ] docs/ARCHITECTURE.md con diagramas

### ✅ Screenshots (30 total)
- [ ] 6 de infraestructura (Terraform, AWS Console)
- [ ] 4 de Knowledge Base (Bedrock Console)
- [ ] 5 de sincronización de datos
- [ ] 5 de Python (código + ejecución)
- [ ] 3 de parámetros del modelo
- [ ] 7 de aplicación de chat

### ✅ Código Python
- [ ] bedrock_utils.py con 3 funciones documentadas
- [ ] app_demo.py funcional con Streamlit
- [ ] requirements.txt actualizado

### ✅ Limpieza
- [ ] .gitignore actualizado
- [ ] No hay carpeta terraform/ duplicada
- [ ] deprecated/ y .backups/ excluidos
- [ ] venv/ excluido

---

## 🔄 Flujo de Trabajo Recomendado

1. **Desarrollo**:
   - Trabajar en raíz y subcarpetas normalmente
   - quick_credentials.py para renovar credenciales
   - terraform apply en stack1/, luego stack2/

2. **Pre-Entrega**:
   - Mover archivos deprecados a `deprecated/`
   - Mover backups a `.backups/`
   - Verificar .gitignore excluye todo lo sensible

3. **Captura de Screenshots**:
   - Seguir SCREENSHOT_GUIDE.md sistemáticamente
   - Nombrar archivos: 01_descripcion.jpeg, 02_descripcion.jpeg
   - Guardar en screenshots/

4. **Empaquetado Final**:
   - Excluir: venv/, deprecated/, .backups/, __pycache__/, .git/, .env, *.tfstate
   - Incluir: Todo lo demás
   - Crear ZIP: `Apellido_Nombre_ProjectSubmission.zip`

---

## 📞 Soporte

Para dudas sobre la estructura:

1. **Organización**: Ver esta guía (ESTRUCTURA.md)
2. **Contenido**: Ver docs/README_FINAL_PROJECT.md
3. **Screenshots**: Ver screenshots/SCREENSHOT_GUIDE.md
4. **Quick Start**: Ver docs/QUICK_START.md

---

**Última actualización**: Diciembre 10, 2025  
**Autor**: [Tu Nombre]  
**Proyecto**: AWS AI Engineer Nanodegree - Udacity
