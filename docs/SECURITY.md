# 🔒 Guía de Seguridad - DocSmart RAG System

## 📋 Índice
1. [Gestión de Credenciales](#gestión-de-credenciales)
2. [Configuración Segura](#configuración-segura)
3. [Mejores Prácticas](#mejores-prácticas)
4. [Rotación de Credenciales](#rotación-de-credenciales)
5. [Troubleshooting de Seguridad](#troubleshooting)

---

## 🔐 Gestión de Credenciales

### Método Recomendado: Script de Configuración Interactivo

El sistema incluye `configure.py`, un script que te guía paso a paso:

```bash
python configure.py
```

**Características:**
- ✅ Validación en tiempo real de credenciales
- ✅ Verificación de acceso a Bedrock
- ✅ Passwords ocultos (no se muestran al escribir)
- ✅ Backup automático de configuración anterior
- ✅ Validación de permisos AWS

---

## ⚙️ Configuración Segura

### Opción 1: Configuración Automática (Recomendada)

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Ejecutar configurador
python configure.py
```

El script te preguntará:
1. **Tipo de credenciales**: Permanentes vs Temporales
2. **AWS Access Key ID**
3. **AWS Secret Access Key** (oculto)
4. **AWS Session Token** (si aplica, oculto)
5. **Región AWS**
6. **Bucket S3** (con creación automática)
7. **Modelos Bedrock**
8. **Configuración de DB**

### Opción 2: Variables de Entorno del Sistema

Para mayor seguridad, puedes usar variables de entorno del sistema:

**Windows (PowerShell):**
```powershell
# Temporal (solo esta sesión)
$env:AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
$env:AWS_SECRET_ACCESS_KEY="wJalrXUtn..."

# Permanente (perfil de usuario)
[Environment]::SetEnvironmentVariable("AWS_ACCESS_KEY_ID", "AKIAIO...", "User")
[Environment]::SetEnvironmentVariable("AWS_SECRET_ACCESS_KEY", "wJalrX...", "User")
```

**Linux/Mac:**
```bash
# Agregar a ~/.bashrc o ~/.zshrc
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtn..."
export AWS_SESSION_TOKEN="IQoJb3..."  # Si aplica
export AWS_REGION="us-east-1"
```

### Opción 3: AWS CLI Profile

Configura perfiles de AWS CLI:

```bash
# Configurar perfil
aws configure --profile docsmart

# Usar el perfil
export AWS_PROFILE=docsmart
```

En `.env`:
```env
AWS_PROFILE=docsmart
AWS_REGION=us-east-1
```

### Opción 4: AWS IAM Roles (Producción)

Para EC2/ECS/Lambda, usa IAM Roles en lugar de credenciales:

```python
# El SDK automáticamente usa el IAM Role
# No necesitas AWS_ACCESS_KEY_ID ni AWS_SECRET_ACCESS_KEY
```

---

## 🛡️ Mejores Prácticas

### 1. Nunca Hardcodear Credenciales

❌ **MAL:**
```python
aws_access_key = "AKIAIOSFODNN7EXAMPLE"  # NUNCA HAGAS ESTO
```

✅ **BIEN:**
```python
import os
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
```

### 2. Archivo .env NUNCA en Git

El archivo `.gitignore` ya incluye `.env`, pero verifica:

```bash
# Verificar que .env está ignorado
git check-ignore .env
# Debe retornar: .env

# Si ya lo committeaste por error:
git rm --cached .env
git commit -m "Remove .env from git"
```

### 3. Permisos Mínimos (Least Privilege)

Crea un usuario IAM específico con solo los permisos necesarios:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:ListFoundationModels"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::docsmart-documents-*",
        "arn:aws:s3:::docsmart-documents-*/*"
      ]
    }
  ]
}
```

### 4. Rotación Regular de Credenciales

**Frecuencia recomendada:**
- Desarrollo: Cada 90 días
- Producción: Cada 30-45 días
- Credenciales comprometidas: Inmediatamente

**Proceso:**
1. Crear nuevas credenciales en AWS Console
2. Ejecutar `python configure.py` con nuevas credenciales
3. Probar que funciona
4. Desactivar/eliminar credenciales antiguas

### 5. Credenciales Temporales

Para entornos educativos (AWS Academy, voclabs):

```bash
# Las credenciales temporales incluyen Session Token
python configure.py
# Selecciona opción "2. Credenciales temporales"
```

**Nota:** Las credenciales temporales expiran (típicamente 3-4 horas). Regenera desde AWS Academy cuando expiren.

### 6. Auditoría de Accesos

Revisa regularmente CloudTrail:

```bash
# Ver últimas acciones
aws cloudtrail lookup-events --max-results 10
```

### 7. Encriptación de .env (Opcional)

Para mayor seguridad, encripta el archivo `.env`:

```bash
# Instalar herramienta
pip install cryptography

# Encriptar
python -c "
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(f'Key: {key.decode()}')
f = Fernet(key)
with open('.env', 'rb') as file:
    encrypted = f.encrypt(file.read())
with open('.env.encrypted', 'wb') as file:
    file.write(encrypted)
"

# Guardar la key de forma segura (¡NO en git!)
```

---

## 🔄 Rotación de Credenciales

### Script de Verificación de Expiración

```bash
# Verificar si credenciales temporales están por expirar
python -c "
import boto3
sts = boto3.client('sts')
try:
    identity = sts.get_caller_identity()
    print('✅ Credenciales válidas')
    print(f'Account: {identity[\"Account\"]}')
except Exception as e:
    print('❌ Credenciales expiradas o inválidas')
    print('Por favor regenera desde AWS Academy')
"
```

### Proceso de Rotación Paso a Paso

#### 1. Obtener Nuevas Credenciales

**AWS Academy/voclabs:**
1. Ve a tu curso en AWS Academy
2. Click en "AWS Details"
3. Click en "Show" en AWS CLI credentials
4. Copia las nuevas credenciales

**IAM User:**
1. AWS Console → IAM → Users → Tu usuario
2. Security Credentials tab
3. "Create access key"
4. Descarga CSV o copia credenciales

#### 2. Actualizar Configuración

```bash
# Opción A: Re-ejecutar configurador
python configure.py

# Opción B: Editar manualmente .env
notepad .env  # Windows
nano .env     # Linux/Mac
```

#### 3. Verificar Nuevas Credenciales

```bash
# Test rápido
aws sts get-caller-identity

# Test completo
python test_bedrock.py
```

#### 4. Desactivar Credenciales Antiguas

Solo después de verificar que las nuevas funcionan:

1. AWS Console → IAM → Users
2. Security Credentials
3. "Make inactive" o "Delete" en access key antigua

---

## 🚨 Qué Hacer Si Credenciales Se Comprometen

### Acción Inmediata (Dentro de 5 minutos)

1. **Desactivar credenciales comprometidas:**
   ```bash
   aws iam update-access-key --access-key-id AKIAI... --status Inactive
   ```

2. **Crear nuevas credenciales:**
   ```bash
   aws iam create-access-key --user-name tu-usuario
   ```

3. **Actualizar configuración:**
   ```bash
   python configure.py
   ```

4. **Eliminar credenciales comprometidas:**
   ```bash
   aws iam delete-access-key --access-key-id AKIAI...
   ```

### Revisión Post-Incidente

1. **Revisar CloudTrail:**
   ```bash
   aws cloudtrail lookup-events --start-time 2024-01-01
   ```

2. **Verificar recursos creados:**
   ```bash
   aws ec2 describe-instances
   aws s3 ls
   ```

3. **Rotar todas las credenciales relacionadas**

4. **Notificar al equipo de seguridad**

---

## 🔍 Troubleshooting de Seguridad

### Error: "Access Denied"

```
ClientError: An error occurred (AccessDenied) when calling the PutObject operation
```

**Causa:** Permisos insuficientes

**Solución:**
1. Verifica políticas IAM
2. Verifica bucket policies
3. Usa `python configure.py` para re-validar

### Error: "Invalid security token"

```
ClientError: An error occurred (InvalidToken) when calling the GetCallerIdentity operation
```

**Causa:** Credenciales temporales expiradas

**Solución:**
```bash
# Regenerar desde AWS Academy
# Luego:
python configure.py
```

### Error: ".env not found"

```
FileNotFoundError: .env file not found
```

**Solución:**
```bash
# Crear configuración
python configure.py

# O copiar template
cp .env.example .env
notepad .env  # Editar manualmente
```

### Advertencia: "Credentials in clear text"

**Solución:**
```bash
# Verificar permisos del archivo
# Windows
icacls .env /inheritance:r /grant:r "%USERNAME%:F"

# Linux/Mac
chmod 600 .env
```

---

## 📝 Checklist de Seguridad

Antes de usar en producción:

- [ ] ✅ Credenciales NUNCA en código fuente
- [ ] ✅ `.env` en `.gitignore`
- [ ] ✅ Permisos IAM mínimos necesarios
- [ ] ✅ Credenciales rotadas regularmente
- [ ] ✅ CloudTrail habilitado
- [ ] ✅ MFA habilitado en cuenta AWS
- [ ] ✅ Backup de configuración en lugar seguro
- [ ] ✅ Equipo capacitado en seguridad
- [ ] ✅ Plan de respuesta a incidentes documentado
- [ ] ✅ Variables de entorno en producción (no .env)

---

## 📚 Recursos Adicionales

- [AWS Security Best Practices](https://docs.aws.amazon.com/security/latest/userguide/best-practices.html)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Bedrock Security](https://docs.aws.amazon.com/bedrock/latest/userguide/security.html)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## 🆘 Contacto de Seguridad

Si descubres una vulnerabilidad de seguridad:

1. **NO** abras un issue público
2. Envía email a: security@docsmart.example.com
3. Incluye detalles técnicos y pasos para reproducir
4. Espera respuesta en 48 horas

---

**🔒 La seguridad es responsabilidad de todos. ¡Mantén tus credenciales seguras! 🔒**
