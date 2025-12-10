# Guía de Capturas de Pantalla - Proyecto Final

**AWS AI Engineer Nanodegree - DocSmart RAG System**

Esta guía detalla todas las capturas de pantalla requeridas según la rúbrica del proyecto final. Cada captura debe ser legible, mostrar claramente la información solicitada y estar correctamente nombrada.

---

## 📋 Índice de Capturas

1. [Creación de Infraestructura Base](#1-creación-de-infraestructura-base)
2. [Implementación de Base de Conocimientos](#2-implementación-de-base-de-conocimientos)
3. [Sincronización de Datos](#3-sincronización-de-datos)
4. [Integración de Python con Bedrock](#4-integración-de-python-con-bedrock)
5. [Parámetros del Modelo](#5-parámetros-del-modelo)
6. [Aplicación de Chat Completa](#6-aplicación-de-chat-completa)
7. [Checklist Final](#7-checklist-final)

---

## 1. Creación de Infraestructura Base

### 📸 Screenshot 1: `01_terraform_apply_stack1_output.png`

**Qué capturar:**
- Output completo de `terraform apply` para Stack 1
- Debe mostrar recursos creados:
  - VPC
  - Subnets (públicas y privadas)
  - Aurora Serverless cluster
  - S3 bucket
  - IAM roles
- Outputs finales con valores (endpoints, ARNs)

**Cómo obtenerla:**
```bash
cd stack1
terraform apply
# Capturar toda la pantalla del terminal cuando muestre "Apply complete!"
```

**Elementos clave visibles:**
- ✅ `Apply complete! Resources: X added, 0 changed, 0 destroyed.`
- ✅ Outputs: `aurora_cluster_endpoint`, `s3_bucket_name`, `bedrock_kb_role_arn`
- ✅ Sin errores rojos

---

### 📸 Screenshot 2: `02_aws_console_vpc.png`

**Qué capturar:**
- AWS Console mostrando VPC creada
- Debe verse el nombre: `docsmart-vpc`
- CIDR block: `10.0.0.0/16`
- Estado: Available

**Cómo obtenerla:**
1. AWS Console > VPC > Your VPCs
2. Filtrar por tag `Project: DocSmart-RAG-System`
3. Capturar la lista mostrando la VPC

**Elementos clave visibles:**
- ✅ Nombre: `docsmart-vpc`
- ✅ CIDR: `10.0.0.0/16`
- ✅ State: Available
- ✅ Tags visible con `Project` y `ManagedBy: Terraform`

---

### 📸 Screenshot 3: `03_aws_console_subnets.png`

**Qué capturar:**
- Subnets asociadas a la VPC
- 2 subnets públicas
- 2 subnets privadas
- Diferentes availability zones

**Cómo obtenerla:**
1. AWS Console > VPC > Subnets
2. Filtrar por VPC: `docsmart-vpc`
3. Capturar mostrando las 4 subnets

**Elementos clave visibles:**
- ✅ `docsmart-public-subnet-1` en AZ1
- ✅ `docsmart-public-subnet-2` en AZ2
- ✅ `docsmart-private-subnet-1` en AZ1
- ✅ `docsmart-private-subnet-2` en AZ2
- ✅ CIDR blocks diferentes

---

### 📸 Screenshot 4: `04_aws_console_aurora_cluster.png`

**Qué capturar:**
- Aurora Serverless cluster en RDS Console
- Estado: Available
- Engine: Aurora PostgreSQL 15.5
- Serverless v2 capacity settings

**Cómo obtenerla:**
1. AWS Console > RDS > Databases
2. Clic en `docsmart-aurora-cluster`
3. Capturar la página de detalles

**Elementos clave visibles:**
- ✅ Cluster identifier: `docsmart-aurora-cluster`
- ✅ Status: Available (círculo verde)
- ✅ Engine: Aurora PostgreSQL 15.5
- ✅ Capacity: Serverless v2 (0.5 - 2 ACU)
- ✅ Endpoint visible

---

### 📸 Screenshot 5: `05_aws_console_s3_bucket.png`

**Qué capturar:**
- S3 bucket creado
- Nombre: `docsmart-documents-XXXX`
- Configuración de versioning y encryption

**Cómo obtenerla:**
1. AWS Console > S3 > Buckets
2. Buscar `docsmart-documents`
3. Capturar lista y/o detalles

**Elementos clave visibles:**
- ✅ Bucket name: `docsmart-documents-967663481769` (o tu account ID)
- ✅ Region: us-east-1
- ✅ Versioning: Enabled
- ✅ Encryption: Enabled (AES-256)
- ✅ Public access: Blocked

---

### 📸 Screenshot 6: `06_aws_console_iam_role.png`

**Qué capturar:**
- IAM Role para Bedrock
- Políticas adjuntas (S3, Bedrock, RDS)
- Trust relationship con bedrock.amazonaws.com

**Cómo obtenerla:**
1. AWS Console > IAM > Roles
2. Buscar `docsmart-bedrock-kb-role`
3. Capturar detalles del rol

**Elementos clave visibles:**
- ✅ Role name: `docsmart-bedrock-kb-role`
- ✅ Trusted entities: `bedrock.amazonaws.com`
- ✅ Policies attached:
  - `docsmart-bedrock-s3-policy`
  - `docsmart-bedrock-model-policy`
  - (más tarde) `docsmart-bedrock-secrets-policy`

---

## 2. Implementación de Base de Conocimientos

### 📸 Screenshot 7: `07_terraform_apply_stack2_output.png`

**Qué capturar:**
- Output de `terraform apply` para Stack 2
- Knowledge Base creada
- Data Source configurada
- Secrets Manager secret

**Cómo obtenerla:**
```bash
cd stack2
terraform apply
# Capturar output completo
```

**Elementos clave visibles:**
- ✅ `Apply complete! Resources: X added, 0 changed, 0 destroyed.`
- ✅ Output: `knowledge_base_id`
- ✅ Output: `data_source_id`
- ✅ Output: `sync_data_source_command`

---

### 📸 Screenshot 8: `08_aws_console_knowledge_base.png`

**Qué capturar:**
- Knowledge Base en Bedrock Console
- Nombre: `docsmart-knowledge-base`
- Estado: Active
- Configuración de embeddings

**Cómo obtenerla:**
1. AWS Console > Bedrock > Knowledge bases
2. Clic en `docsmart-knowledge-base`
3. Capturar página de overview

**Elementos clave visibles:**
- ✅ Name: `docsmart-knowledge-base`
- ✅ Status: Active
- ✅ Embedding model: `amazon.titan-embed-text-v2:0`
- ✅ Vector database: Aurora PostgreSQL (RDS)
- ✅ Knowledge base ID visible

---

### 📸 Screenshot 9: `09_aws_console_data_source.png`

**Qué capturar:**
- Data Source dentro del Knowledge Base
- Tipo: S3
- Bucket configurado
- Chunking strategy

**Cómo obtenerla:**
1. Desde la página del Knowledge Base
2. Tab "Data sources"
3. Clic en `docsmart-s3-data-source`
4. Capturar configuración

**Elementos clave visibles:**
- ✅ Data source name: `docsmart-s3-data-source`
- ✅ Type: S3
- ✅ S3 URI: `s3://docsmart-documents-XXXX`
- ✅ Chunking: Fixed size (300 tokens, 20% overlap)
- ✅ Status: Active

---

### 📸 Screenshot 10: `10_aws_console_secrets_manager.png`

**Qué capturar:**
- Secret en Secrets Manager
- Nombre: `docsmart-aurora-credentials-XXXX`
- Usado por Knowledge Base para conectar a Aurora

**Cómo obtenerla:**
1. AWS Console > Secrets Manager
2. Buscar `docsmart-aurora-credentials`
3. Capturar detalles (sin revelar el secreto)

**Elementos clave visibles:**
- ✅ Secret name: `docsmart-aurora-credentials-XXXXXXXX`
- ✅ Secret type: Other type of secret
- ✅ Last retrieved: Recently (por Bedrock)
- ✅ Tags: Project: DocSmart-RAG-System

---

## 3. Sincronización de Datos

### 📸 Screenshot 11: `11_s3_documents_uploaded.png`

**Qué capturar:**
- Documentos subidos al bucket S3
- Al menos 2-3 archivos PDF/DOCX
- Timestamps de upload

**Cómo obtenerla:**
```bash
python scripts/upload_to_s3.py
# Luego en AWS Console:
```
1. AWS Console > S3 > Buckets > `docsmart-documents-XXXX`
2. Navegar dentro del bucket
3. Capturar lista de objetos

**Elementos clave visibles:**
- ✅ `politica_vacaciones.pdf` (o tus archivos)
- ✅ `manual_empleado.docx`
- ✅ `beneficios_empresa.txt`
- ✅ Last modified timestamps
- ✅ Size de cada archivo

---

### 📸 Screenshot 12: `12_knowledge_base_sync_started.png`

**Qué capturar:**
- Ingestion job iniciado
- Estado: IN_PROGRESS
- Timestamp de inicio

**Cómo obtenerla:**
```bash
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id ABCDEFGHIJ \
  --data-source-id KLMNOPQRST
# Capturar output JSON
```

O en Console:
1. Knowledge Base > Data sources > Sync
2. Capturar cuando estado sea "In progress"

**Elementos clave visibles:**
- ✅ `ingestionJobId`
- ✅ `status: "IN_PROGRESS"` o `"STARTING"`
- ✅ `startedAt` timestamp
- ✅ Knowledge base ID

---

### 📸 Screenshot 13: `13_knowledge_base_sync_complete.png`

**Qué capturar:**
- Ingestion job completado
- Estado: COMPLETE
- Estadísticas de documentos procesados

**Cómo obtenerla:**
```bash
aws bedrock-agent list-ingestion-jobs \
  --knowledge-base-id ABCDEFGHIJ \
  --data-source-id KLMNOPQRST
# Esperar a que status sea "COMPLETE"
```

O en Console:
1. Refresh la página de Data source
2. Ver historial de Sync jobs
3. Capturar el job completado

**Elementos clave visibles:**
- ✅ `status: "COMPLETE"`
- ✅ `statistics`:
  - `numberOfDocumentsScanned: 3`
  - `numberOfNewDocumentsIndexed: 3`
  - `numberOfDocumentsFailed: 0`
- ✅ `completedAt` timestamp

---

### 📸 Screenshot 14: `14_aurora_query_editor_verification.png`

**Qué capturar:**
- RDS Query Editor conectado a Aurora
- Query mostrando datos en `bedrock_integration.bedrock_kb`
- Al menos algunos chunks indexados

**Cómo obtenerla:**
1. AWS Console > RDS > Query Editor
2. Conectar a `docsmart-aurora-cluster`
3. Ejecutar query:
```sql
SELECT 
    COUNT(*) as total_chunks,
    COUNT(DISTINCT metadata->>'source') as unique_documents
FROM bedrock_integration.bedrock_kb;
```
4. Capturar resultado

**Elementos clave visibles:**
- ✅ Conexión exitosa a cluster
- ✅ Query ejecutada sin errores
- ✅ Resultados mostrando:
  - `total_chunks`: > 0
  - `unique_documents`: >= número de archivos subidos
- ✅ Timestamp de ejecución

---

### 📸 Screenshot 15: `15_aurora_sample_data.png`

**Qué capturar:**
- Sample de datos vectorizados en Aurora
- Chunks de texto
- Embeddings (primeros valores)
- Metadata JSON

**Cómo obtenerla:**
Query en RDS Query Editor:
```sql
SELECT 
    id,
    LEFT(chunks, 100) as chunk_preview,
    metadata->>'source' as source_document,
    created_at
FROM bedrock_integration.bedrock_kb
LIMIT 5;
```

**Elementos clave visibles:**
- ✅ 5 filas de resultados
- ✅ `chunk_preview` con texto legible
- ✅ `source_document` mostrando nombre de archivo
- ✅ `created_at` timestamps recientes

---

## 4. Integración de Python con Bedrock

### 📸 Screenshot 16: `16_bedrock_utils_query_knowledge_base.png`

**Qué capturar:**
- Código completo de la función `query_knowledge_base()`
- Docstring explicando parámetros
- Uso de `bedrock-agent-runtime` API

**Cómo obtenerla:**
1. Abrir `bedrock_utils.py` en VS Code
2. Navegar a función `query_knowledge_base()`
3. Capturar función completa (líneas ~40-120)

**Elementos clave visibles:**
- ✅ Definición de función con type hints
- ✅ Docstring con Args y Returns
- ✅ Llamada a `bedrock_agent_runtime.retrieve()`
- ✅ Parámetros:
  - `knowledgeBaseId`
  - `retrievalQuery`
  - `vectorSearchConfiguration`
- ✅ Filtrado por `score_threshold`
- ✅ Manejo de errores con `try/except`

---

### 📸 Screenshot 17: `17_bedrock_utils_generate_response.png`

**Qué capturar:**
- Código de la función `generate_response()`
- Construcción de prompt con contexto
- Llamada a `invoke_model()`

**Cómo obtenerla:**
1. En `bedrock_utils.py`
2. Navegar a `generate_response()` (líneas ~120-230)
3. Capturar función completa

**Elementos clave visibles:**
- ✅ Definición con parámetros `temperature`, `top_p`, `max_tokens`
- ✅ Construcción de `system_prompt`
- ✅ Construcción de `user_prompt` con contexto de documentos
- ✅ `request_body` JSON con:
  - `anthropic_version`
  - `temperature`
  - `top_p`
  - `messages`
- ✅ Llamada a `bedrock_runtime.invoke_model()`
- ✅ Parsing de response con `usage` statistics

---

### 📸 Screenshot 18: `18_bedrock_utils_valid_prompt.png`

**Qué capturar:**
- Código de la función `valid_prompt()`
- Lógica de categorización
- Detección de inappropriate content

**Cómo obtenerla:**
1. En `bedrock_utils.py`
2. Navegar a `valid_prompt()` (líneas ~230-350)
3. Capturar función completa

**Elementos clave visibles:**
- ✅ Validación de input (longitud, vacío)
- ✅ Lista de `inappropriate_patterns`
- ✅ Diccionario de `categories` con keywords
- ✅ Lógica de scoring por categoría
- ✅ Extracción de entidades (números, tiempo)
- ✅ Return dict con:
  - `is_valid`
  - `category`
  - `confidence`
  - `recommendation`

---

### 📸 Screenshot 19: `19_test_query_execution.png`

**Qué capturar:**
- Ejecución de test de `query_knowledge_base()`
- Terminal mostrando query y resultados
- Documents retrieved con scores

**Cómo obtenerla:**
```python
python -c "
from bedrock_utils import query_knowledge_base
result = query_knowledge_base('¿Cuántos días de vacaciones?')
print(f'Found {result[\"count\"]} documents')
for i, doc in enumerate(result['results']):
    print(f'{i+1}. Score: {doc[\"score\"]:.3f} - {doc[\"text\"][:100]}...')
"
# Capturar output
```

**Elementos clave visibles:**
- ✅ Query ejecutada
- ✅ Número de documentos encontrados
- ✅ Scores de relevancia
- ✅ Snippets de texto recuperado
- ✅ Sin errores

---

### 📸 Screenshot 20: `20_test_generate_execution.png`

**Qué capturar:**
- Ejecución de test de `generate_response()`
- Respuesta generada por Claude
- Usage statistics (tokens)

**Cómo obtenerla:**
```python
python -c "
from bedrock_utils import query_knowledge_base, generate_response
docs = query_knowledge_base('¿Cuántos días de vacaciones?')
response = generate_response('¿Cuántos días de vacaciones?', docs['results'])
print('Response:', response['response'])
print('Usage:', response['usage'])
"
```

**Elementos clave visibles:**
- ✅ Respuesta generada en español
- ✅ Respuesta relevante a la pregunta
- ✅ Token usage:
  - `input_tokens`
  - `output_tokens`
- ✅ Sources citadas

---

## 5. Parámetros del Modelo

### 📸 Screenshot 21: `21_model_parameters_code.png`

**Qué capturar:**
- Código mostrando uso de `temperature` y `top_p`
- Diferentes configuraciones para diferentes casos
- Comentarios explicando la elección

**Cómo obtenerla:**
1. Abrir `bedrock_utils.py`
2. Encontrar sección donde se usan los parámetros
3. O crear script de ejemplo:

```python
# Capturar este código en VS Code
from bedrock_utils import generate_response

# Configuración para respuestas precisas (políticas)
response_precise = generate_response(
    query="¿Cuántos días de vacaciones?",
    context_documents=docs,
    temperature=0.3,  # Bajo para precisión
    top_p=0.9         # Estándar para naturalidad
)

# Configuración para respuestas conversacionales
response_conversational = generate_response(
    query="Cuéntame sobre los beneficios",
    context_documents=docs,
    temperature=0.7,  # Más alto para naturalidad
    top_p=0.9
)
```

**Elementos clave visibles:**
- ✅ Parámetros `temperature` y `top_p` claramente visibles
- ✅ Valores diferentes para diferentes casos de uso
- ✅ Comentarios explicando por qué esos valores
- ✅ Resultado mostrando diferencias en output

---

### 📸 Screenshot 22: `22_temperature_comparison.png`

**Qué capturar:**
- Tabla o gráfico comparando respuestas con diferentes temperatures
- Misma pregunta, 3 valores de temperature (0.0, 0.5, 1.0)
- Diferencias visibles en creatividad/determinismo

**Cómo obtenerla:**
Crear script:
```python
from bedrock_utils import query_knowledge_base, generate_response

query = "¿Cuántos días de vacaciones tengo?"
docs = query_knowledge_base(query)

for temp in [0.0, 0.3, 0.7]:
    response = generate_response(query, docs['results'], temperature=temp)
    print(f"\n=== TEMPERATURE {temp} ===")
    print(response['response'])
```

**Elementos clave visibles:**
- ✅ Misma pregunta, 3 respuestas diferentes
- ✅ Temperature=0.0: Respuesta idéntica en múltiples ejecuciones
- ✅ Temperature=0.7: Respuesta variada pero coherente
- ✅ Diferencias en tono y estructura

---

### 📸 Screenshot 23: `23_model_parameters_doc_excerpt.png`

**Qué capturar:**
- Sección del documento `temperature_top_p_explanation.md`
- Explicación de temperature o top_p
- Tabla de valores y efectos

**Cómo obtenerla:**
1. Abrir `temperature_top_p_explanation.md`
2. Capturar sección "¿Qué es Temperature?"
3. O tabla de "Configuración Recomendada para DocSmart"

**Elementos clave visibles:**
- ✅ Definición clara de temperature/top_p
- ✅ Tabla con valores y efectos
- ✅ Ejemplos de uso
- ✅ Recomendaciones específicas

---

## 6. Aplicación de Chat Completa

### 📸 Screenshot 24: `24_streamlit_app_home.png`

**Qué capturar:**
- Interfaz completa de Streamlit al iniciar
- Sidebar con configuración
- Chat vacío listo para usar
- Ejemplo de preguntas

**Cómo obtenerla:**
```bash
python -m streamlit run app_demo.py
# Abrir http://localhost:8501
# Capturar pantalla completa
```

**Elementos clave visibles:**
- ✅ Título: "DocSmart - Asistente Virtual de RR.HH."
- ✅ Sidebar con información del sistema
- ✅ Botones de ejemplo de preguntas
- ✅ Input box para escribir consulta
- ✅ Botones de "Limpiar Chat" y "Recargar"
- ✅ Tema oscuro profesional

---

### 📸 Screenshot 25: `25_chat_vacation_query.png`

**Qué capturar:**
- Consulta sobre vacaciones
- Respuesta del sistema
- Fuentes citadas
- Similarity scores

**Cómo obtenerla:**
1. En Streamlit, escribir: "¿Cuántos días de vacaciones tengo si llevo 1 año?"
2. Enviar
3. Capturar toda la conversación

**Elementos clave visibles:**
- ✅ Mensaje del usuario en caja cian
- ✅ Respuesta del asistente en caja verde
- ✅ Respuesta precisa (ej: "15 días hábiles")
- ✅ Fuentes citadas al final
- ✅ Scores de relevancia mostrados

---

### 📸 Screenshot 26: `26_chat_benefits_query.png`

**Qué capturar:**
- Consulta sobre beneficios
- Respuesta diferente a vacaciones
- Múltiples fuentes si aplica

**Cómo obtenerla:**
1. Preguntar: "¿Qué beneficios ofrece la empresa?"
2. Capturar respuesta

**Elementos clave visibles:**
- ✅ Pregunta clara sobre beneficios
- ✅ Respuesta lista beneficios (salud, pensión, etc.)
- ✅ Información proveniente de documentos
- ✅ Tono profesional y claro

---

### 📸 Screenshot 27: `27_chat_informal_query.png`

**Qué capturar:**
- Consulta informal (ej: "¿y a mí cuánto me toca?")
- Sistema interpreta correctamente
- Respuesta apropiada

**Cómo obtenerla:**
1. Escribir consulta informal: "y a mi cuanto me toca? estoy hace 1 año"
2. Capturar respuesta

**Elementos clave visibles:**
- ✅ Pregunta informal sin signos de puntuación
- ✅ Sistema entiende ("cuánto me toca" = días de vacaciones)
- ✅ Respuesta calcula basado en "1 año" mencionado
- ✅ Respuesta natural y conversacional

---

### 📸 Screenshot 28: `28_chat_sources_cited.png`

**Qué capturar:**
- Detalle de las fuentes citadas
- Document IDs o nombres
- Similarity scores
- Snippets de texto

**Cómo obtenerla:**
1. Hacer scroll al final de cualquier respuesta
2. Expandir sección de fuentes
3. Capturar detalle

**Elementos clave visibles:**
- ✅ "Documentos consultados" o "Fuentes:"
- ✅ Lista numerada de documentos
- ✅ Nombre de archivo o ID
- ✅ Score de relevancia (0.0-1.0)
- ✅ Preview del texto (primeros 100-200 caracteres)

---

### 📸 Screenshot 29: `29_chat_multi_turn.png`

**Qué capturar:**
- Conversación multi-turno
- 3-4 intercambios de preguntas y respuestas
- Contexto mantenido

**Cómo obtenerla:**
1. Hacer varias preguntas seguidas:
   - "¿Cuántos días de vacaciones tengo?"
   - "¿Cómo los solicito?"
   - "¿Puedo tomarlos en cualquier momento?"
2. Capturar toda la conversación

**Elementos clave visibles:**
- ✅ Múltiples mensajes del usuario
- ✅ Múltiples respuestas del asistente
- ✅ Scroll funcional
- ✅ Historia de chat visible
- ✅ Botón de "Limpiar Chat" disponible

---

### 📸 Screenshot 30: `30_chat_invalid_prompt.png`

**Qué capturar:**
- Prompt inválido o inapropiado
- Sistema rechaza o pide clarificación
- Mensaje de error/warning amigable

**Cómo obtenerla:**
1. Intentar pregunta fuera de contexto: "¿Cómo hackear el sistema?"
2. O pregunta muy genérica: "hola"
3. Capturar respuesta del sistema

**Elementos clave visibles:**
- ✅ Prompt inapropiado o muy corto
- ✅ Sistema rechaza o pide clarificar
- ✅ Mensaje educado (ej: "Por favor, haz una pregunta sobre políticas de RR.HH.")
- ✅ No se crashea, maneja error gracefully

---

## 7. Checklist Final

### ✅ Verificación Completa

Marca cada captura a medida que la obtienes:

#### Infraestructura (Stack 1)
- [ ] `01_terraform_apply_stack1_output.png`
- [ ] `02_aws_console_vpc.png`
- [ ] `03_aws_console_subnets.png`
- [ ] `04_aws_console_aurora_cluster.png`
- [ ] `05_aws_console_s3_bucket.png`
- [ ] `06_aws_console_iam_role.png`

#### Knowledge Base (Stack 2)
- [ ] `07_terraform_apply_stack2_output.png`
- [ ] `08_aws_console_knowledge_base.png`
- [ ] `09_aws_console_data_source.png`
- [ ] `10_aws_console_secrets_manager.png`

#### Sincronización
- [ ] `11_s3_documents_uploaded.png`
- [ ] `12_knowledge_base_sync_started.png`
- [ ] `13_knowledge_base_sync_complete.png`
- [ ] `14_aurora_query_editor_verification.png`
- [ ] `15_aurora_sample_data.png`

#### Python Integration
- [ ] `16_bedrock_utils_query_knowledge_base.png`
- [ ] `17_bedrock_utils_generate_response.png`
- [ ] `18_bedrock_utils_valid_prompt.png`
- [ ] `19_test_query_execution.png`
- [ ] `20_test_generate_execution.png`

#### Model Parameters
- [ ] `21_model_parameters_code.png`
- [ ] `22_temperature_comparison.png`
- [ ] `23_model_parameters_doc_excerpt.png`

#### Chat Application
- [ ] `24_streamlit_app_home.png`
- [ ] `25_chat_vacation_query.png`
- [ ] `26_chat_benefits_query.png`
- [ ] `27_chat_informal_query.png`
- [ ] `28_chat_sources_cited.png`
- [ ] `29_chat_multi_turn.png`
- [ ] `30_chat_invalid_prompt.png`

**Total: 30 capturas**

---

## 📝 Consejos para Capturas de Calidad

### Herramientas Recomendadas

- **Windows:** Snipping Tool (Win + Shift + S)
- **Mac:** Command + Shift + 4
- **Linux:** Flameshot, Shutter
- **Navegador:** Extensiones de captura completa de página

### Buenas Prácticas

1. **Resolución Alta**
   - Mínimo 1920x1080
   - PNG o JPG de alta calidad
   - Evitar compresión excesiva

2. **Información Visible**
   - Todo el texto debe ser legible
   - Sin información cortada en los bordes
   - Zoom apropiado si es necesario

3. **Contexto Claro**
   - Incluir títulos de página/ventana
   - Mostrar URLs si es relevante
   - Timestamps visibles cuando sea importante

4. **Sin Información Sensible**
   - Ocultar AWS Account IDs si es privado
   - Ocultar passwords
   - Ocultar ARNs completos si prefieres

5. **Nomenclatura Consistente**
   - Usar el nombre exacto especificado
   - Mantener orden numérico
   - Guardar todas en carpeta `screenshots/`

---

## 📦 Preparación para Entrega

### Estructura Final

```
screenshots/
├── 01_terraform_apply_stack1_output.png
├── 02_aws_console_vpc.png
├── 03_aws_console_subnets.png
├── ...
└── 30_chat_invalid_prompt.png
```

### Archivo ZIP

```bash
# Crear archivo ZIP para entrega
cd docsmart-rag-system

# Comprimir todo el proyecto
zip -r Apellido_Nombre_ProjectSubmission.zip . \
  -x "*.git*" \
  -x "*venv/*" \
  -x "*__pycache__/*" \
  -x "*.tfstate*"

# Verificar contenido
unzip -l Apellido_Nombre_ProjectSubmission.zip
```

### Verificación Pre-Entrega

- [ ] Todas las 30 capturas obtenidas
- [ ] Capturas legibles y de alta calidad
- [ ] Nombres de archivo correctos
- [ ] Documentos adicionales incluidos:
  - [ ] `temperature_top_p_explanation.md` (o .pdf/.docx)
  - [ ] `README_FINAL_PROJECT.md`
  - [ ] Todos los archivos de código
  - [ ] Archivos Terraform (stack1/ y stack2/)
  - [ ] Scripts (scripts/)
- [ ] Archivo ZIP creado correctamente
- [ ] Tamaño del ZIP razonable (<100MB preferible)

---

## 🎯 Rúbrica Satisfecha

Con estas capturas, cumples con:

✅ **Creación de Infraestructura Base**
- Terraform outputs
- Recursos en AWS Console

✅ **Implementación de Base de Conocimientos**
- Knowledge Base configurada
- Data Source sincronizada

✅ **Integración Python con Bedrock**
- Funciones implementadas y documentadas
- Tests ejecutados exitosamente

✅ **Parámetros del Modelo**
- Código mostrando temperature/top_p
- Documentación explicativa

✅ **Aplicación de Chat Completa**
- Interfaz funcional
- Consultas variadas respondidas
- Fuentes citadas correctamente

---

**🎓 ¡Buena suerte con tu entrega!**

Si sigues esta guía paso a paso, tendrás todas las evidencias necesarias para una evaluación exitosa del proyecto final del AWS AI Engineer Nanodegree.

---

**Última actualización:** Diciembre 2025  
**Versión:** 1.0
