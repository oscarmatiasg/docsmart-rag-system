# 📸 REQUISITOS OFICIALES DE SCREENSHOTS - RÚBRICA UDACITY

**Proyecto Final - AWS AI Engineer Nanodegree**

Este documento lista los requisitos **EXACTOS** según la rúbrica oficial de Udacity.

---

## ✅ ESTADO ACTUAL

**Capturados**: 1 de ~10 requisitos críticos  
**Pendientes**: 9 screenshots críticos + documentación

---

## 1️⃣ BASE INFRASTRUCTURE CREATION

### ✅ Screenshot 1: Terraform Apply Output (Stack 1)
**Requisito**: "Screenshot of Terraform apply output showing successful resource creation"

**Estado**: ⏳ PENDIENTE  
**Acción**: Capturar output completo del último `terraform apply` en stack1

**Debe mostrar**:
- `Apply complete! Resources: X added`
- Outputs: VPC, Aurora, S3, IAM roles
- Sin errores

---

### ❌ Screenshot 2: Secrets Manager - RDS Secret
**Requisito**: "Screenshot of secret manager showing RDS secret created successfully"

**Estado**: ⏳ PENDIENTE  
**Ubicación**: AWS Console > Secrets Manager
**Buscar**: `docsmart-aurora-credentials-8f9d2ccb`

**Debe mostrar**:
- Secret name completo
- Type: "Other type of secret"
- Created date
- Tags (Project: DocSmart-RAG-System)

---

### ❌ Screenshot 3: Query pg_extension
**Requisito**: "Show screenshot of the results of the following query: `SELECT * FROM pg_extension;`"

**Estado**: ✅ EJECUTADO - PENDIENTE CAPTURA  
**Comando ejecutado**:
```powershell
aws rds-data execute-statement \
  --resource-arn "arn:aws:rds:us-east-1:389252695754:cluster:docsmart-aurora-cluster" \
  --database "docsmart_kb" \
  --secret-arn "arn:aws:secretsmanager:us-east-1:389252695754:secret:docsmart-aurora-credentials-8f9d2ccb-ZHc2Yk" \
  --sql "SELECT * FROM pg_extension;"
```

**Resultado obtenido**:
```json
{
    "records": [
        [plpgsql, version 1.0],
        [vector, version 0.8.0]  ← CRÍTICO: Muestra pgvector instalado
    ]
}
```

**Acción**: Capturar pantalla del output del terminal

---

### ❌ Screenshot 4: bedrock_integration.bedrock_kb Table
**Requisito**: "Screenshot showing the information of the bedrock_integration.bedrock_kb table by running the following query"

**Query requerida**:
```sql
SELECT 
    table_schema || '.' || table_name as show_tables
FROM 
    information_schema.tables
WHERE 
    table_type = 'BASE TABLE'
    AND table_schema = 'bedrock_integration';
```

**Estado**: ✅ EJECUTADO - PENDIENTE CAPTURA  
**Resultado**:
```json
{
    "records": [
        ["bedrock_integration.bedrock_kb"]
    ]
}
```

**Acción**: Capturar pantalla del output del terminal

---

## 2️⃣ KNOWLEDGE BASE DEPLOYMENT AND DATA SYNC

### ✅ Screenshot 5: Knowledge Base Deployed
**Requisito**: "Screenshot of deployed knowledge base interface"

**Estado**: ✅ CAPTURADO (Screenshot 7: Stack 2 output)  
**Ubicación**: `screenshots/07_terraform_apply_stack2_output.png`

**Muestra**:
- Knowledge Base ID: `YYIBMDUAYW`
- Data Source ID: `EWNM5DPO3S`
- Apply complete!

---

### ❌ Screenshot 6: Successful Data Sync
**Requisito**: "Screenshot of successful data sync from the AWS console"

**Estado**: ⏳ PENDIENTE  
**Acción requerida**:
1. Subir documentos a S3
2. Iniciar ingestion job
3. Esperar a estado "COMPLETE"
4. Capturar pantalla

**Comando**:
```bash
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id YYIBMDUAYW \
  --data-source-id EWNM5DPO3S

# Luego monitorear hasta COMPLETE
aws bedrock-agent list-ingestion-jobs \
  --knowledge-base-id YYIBMDUAYW \
  --data-source-id EWNM5DPO3S
```

---

## 3️⃣ PYTHON INTEGRATION WITH BEDROCK

### ❌ Screenshot 7: query_knowledge_base Function
**Requisito**: "Code snippet of the implemented function for query_knowledge_base"

**Estado**: ⏳ PENDIENTE  
**Archivo**: `bedrock_utils.py`
**Líneas**: ~40-120

**Debe mostrar**:
- Definición completa de la función
- Docstring con Args/Returns
- Uso de `bedrock_agent_runtime.retrieve()`
- Parámetros: knowledgeBaseId, retrievalQuery, vectorSearchConfiguration

**Acción**: Abrir `bedrock_utils.py` en VS Code y capturar función completa

---

### ❌ Screenshot 8: generate_response Function
**Requisito**: "Code snippet for the generate_response function"

**Estado**: ⏳ PENDIENTE  
**Archivo**: `bedrock_utils.py`
**Líneas**: ~120-230

**Debe mostrar**:
- Construcción de system_prompt
- Construcción de user_prompt con contexto
- request_body JSON con temperature, top_p, messages
- Llamada a `bedrock_runtime.invoke_model()`

---

### ❌ Screenshot 9: valid_prompt Function
**Requisito**: "Code snippet of the valid_prompt function and sample output filtering undesired prompts"

**Estado**: ⏳ PENDIENTE  
**Archivo**: `bedrock_utils.py`
**Líneas**: ~230-350

**Debe mostrar**:
- Validación de input
- Lista de inappropriate_patterns
- Categorización de queries
- Return dict con is_valid, category, confidence

**PLUS**: Ejecutar ejemplo mostrando rechazo de prompt inapropiado

---

## 4️⃣ MODEL PARAMETERS

### ❌ Screenshot 10: Written Explanation
**Requisito**: "Written explanation of these concepts in 1-2 paragraphs"

**Estado**: ⏳ PENDIENTE  
**Concepto**: Temperature y top_p

**Acción**: Crear documento o sección en README explicando:

**Temperature** (0.0-1.0):
- Controla aleatoriedad/creatividad
- Valores bajos (0.0-0.3): Determinista, preciso, ideal para respuestas factuales
- Valores altos (0.7-1.0): Creativo, variado, ideal para contenido generativo
- En DocSmart: Usamos 0.3-0.7 según el caso de uso

**Top_p** (0.0-1.0):
- Nucleus sampling
- Controla diversidad de tokens considerados
- Valores bajos (0.1-0.5): Respuestas más focalizadas
- Valores altos (0.9-1.0): Mayor diversidad
- En DocSmart: Usamos 0.9 para balance entre diversidad y coherencia

---

## 📊 RESUMEN DE ACCIONES INMEDIATAS

### 🚨 CRÍTICO (Requisitos de rúbrica)

1. **Capturar Terminal Outputs** (10 min):
   - [ ] pg_extension query (ya ejecutado)
   - [ ] bedrock_kb table query (ya ejecutado)
   
2. **AWS Console Screenshots** (15 min):
   - [ ] Secrets Manager secret
   - [ ] Data sync complete
   
3. **Code Screenshots** (15 min):
   - [ ] query_knowledge_base función
   - [ ] generate_response función
   - [ ] valid_prompt función
   
4. **Documentación** (20 min):
   - [ ] Explicación Temperature y top_p (1-2 párrafos)

### ⏰ TIEMPO TOTAL ESTIMADO: ~60 minutos

---

## 📝 COMANDOS RÁPIDOS

### Para pg_extension (ya ejecutado - solo capturar):
```powershell
aws rds-data execute-statement `
  --resource-arn "arn:aws:rds:us-east-1:389252695754:cluster:docsmart-aurora-cluster" `
  --database "docsmart_kb" `
  --secret-arn "arn:aws:secretsmanager:us-east-1:389252695754:secret:docsmart-aurora-credentials-8f9d2ccb-ZHc2Yk" `
  --sql "SELECT * FROM pg_extension;"
```

### Para bedrock_kb table (ya ejecutado - solo capturar):
```powershell
aws rds-data execute-statement `
  --resource-arn "arn:aws:rds:us-east-1:389252695754:cluster:docsmart-aurora-cluster" `
  --database "docsmart_kb" `
  --secret-arn "arn:aws:secretsmanager:us-east-1:389252695754:secret:docsmart-aurora-credentials-8f9d2ccb-ZHc2Yk" `
  --sql "SELECT table_schema || '.' || table_name as show_tables FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema = 'bedrock_integration';"
```

### Para subir documentos y sincronizar:
```powershell
# 1. Subir documentos
cd scripts
python upload_to_s3.py

# 2. Iniciar sync
cd ..\stack2
aws bedrock-agent start-ingestion-job `
  --knowledge-base-id YYIBMDUAYW `
  --data-source-id EWNM5DPO3S `
  --region us-east-1
```

---

## ✅ CHECKLIST FINAL

Antes de subir a GitHub:

- [ ] Screenshot 1: Terraform Stack 1 output
- [ ] Screenshot 2: Secrets Manager
- [ ] Screenshot 3: pg_extension query
- [ ] Screenshot 4: bedrock_kb table query
- [ ] Screenshot 5: Knowledge Base deployed ✅
- [ ] Screenshot 6: Data sync complete
- [ ] Screenshot 7: query_knowledge_base code
- [ ] Screenshot 8: generate_response code
- [ ] Screenshot 9: valid_prompt code
- [ ] Screenshot 10: Temperature/top_p explanation

---

**Total Screenshots Requeridos por Rúbrica**: 10 (mínimo)  
**Screenshots Capturados**: 1  
**Screenshots Pendientes**: 9

**⚠️ IMPORTANTE**: Estos son los requisitos MÍNIMOS. La guía de screenshots incluye 30 capturas totales para documentación completa, pero estos 10 son CRÍTICOS para aprobar la rúbrica.

---

**Última Actualización**: Diciembre 10, 2025  
**Estado**: En progreso (10% completado)
