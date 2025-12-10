# Instrucciones de Instalación Rápida

**Proyecto Final - AWS AI Engineer Nanodegree**

## Resumen de Pasos

1. **Clonar y configurar dependencias**
   ```bash
   git clone <repo>
   cd docsmart-rag-system
   pip install -r requirements.txt
   ```

2. **Desplegar Stack 1 (Infraestructura)**
   ```bash
   cd stack1
   cp terraform.tfvars.example terraform.tfvars
   # Editar terraform.tfvars con tus valores
   terraform init
   terraform apply
   ```

3. **Inicializar base de datos**
   - Usar AWS Console > RDS > Query Editor
   - Ejecutar `scripts/aurora_init.sql`
   - Verificar con `scripts/aurora_verify.sql`

4. **Desplegar Stack 2 (Knowledge Base)**
   ```bash
   cd ../stack2
   cp terraform.tfvars.example terraform.tfvars
   # Usar outputs de Stack 1
   terraform init
   terraform apply
   ```

5. **Cargar documentos**
   ```bash
   cd ..
   # Agregar archivos a spec-sheets/
   python scripts/upload_to_s3.py
   ```

6. **Sincronizar Knowledge Base**
   ```bash
   aws bedrock-agent start-ingestion-job \
     --knowledge-base-id <KB_ID> \
     --data-source-id <DS_ID> \
     --region us-east-1
   ```

7. **Lanzar aplicación**
   ```bash
   python -m streamlit run app_demo.py
   ```

Ver documentación completa en `README_FINAL_PROJECT.md`
