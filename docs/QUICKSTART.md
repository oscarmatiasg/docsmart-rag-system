# DocSmart - Guía Rápida de Inicio

## ⚡ Setup en 5 Minutos

### 1️⃣ Instalar dependencias
```bash
# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh
./setup.sh
```

### 2️⃣ Configurar credenciales
Edita `.env`:
```env
AWS_ACCESS_KEY_ID=tu_key
AWS_SECRET_ACCESS_KEY=tu_secret
DB_HOST=tu-aurora-endpoint.rds.amazonaws.com
DB_PASSWORD=tu_password
```

### 3️⃣ Desplegar infraestructura
```bash
cd terraform
terraform init
terraform apply -var="db_master_password=TuPassword123!"
```

### 4️⃣ Inicializar base de datos
```bash
cd ..
python cli.py setup
```

### 5️⃣ Ingestar documentos de prueba
```bash
# Crear carpeta de documentos
mkdir sample_docs

# Ingestar
python cli.py ingest -d sample_docs/
```

### 6️⃣ Lanzar aplicación
```bash
streamlit run app.py
```

¡Listo! Accede a http://localhost:8501

## 🎯 Primer Consulta

1. Ve a "Ingestar Documentos"
2. Sube un PDF
3. Ve a "Chat"
4. Pregunta: "¿De qué trata este documento?"

## 📋 Comandos Útiles

```bash
# Ver estadísticas
python cli.py stats

# Consulta rápida
python cli.py query "tu pregunta aquí"

# Ingestar archivo específico
python cli.py ingest -f documento.pdf
```

## 🆘 Ayuda Rápida

### Error de conexión a BD
```bash
# Verificar endpoint
cat .env | grep DB_HOST

# Test de conexión
psql -h YOUR_ENDPOINT -U postgres -d docsmart_db
```

### Error de Bedrock
1. AWS Console → Bedrock
2. "Model access" → Solicitar acceso a:
   - Titan Embeddings
   - Claude 3.5 Sonnet

### Documentación completa
Ver [README.md](README.md)
