#!/usr/bin/env python3
"""
Configurador Simple para AWS Academy
Solo pide: Access Key ID, Secret Access Key y Session Token
"""

import os
import sys
import getpass
from pathlib import Path
from datetime import datetime

def main():
    print("\n" + "=" * 70)
    print("  🎓 Configuración de Credenciales AWS Academy")
    print("=" * 70 + "\n")
    
    print("ℹ️  Ingresa las 3 credenciales de AWS Academy:\n")
    
    # 1. Access Key ID
    print("1️⃣  ID de clave de acceso AWS")
    print("    Ejemplo: ASIAVVIKEY3FMCTKCQA2")
    access_key = input("    Pega aquí: ").strip()
    
    # 2. Secret Access Key  
    print("\n2️⃣  Clave de acceso secreta AWS")
    print("    Ejemplo: low16lq6Y8e2LroLJHMLuxtRcghFkehrp8Kc/rC9")
    print("    ⚠️  No se mostrará al escribir")
    secret_key = getpass.getpass("    Pega aquí: ").strip()
    
    # 3. Session Token
    print("\n3️⃣  Token de sesión AWS")
    print("    Es un texto largo (IQoJb3JpZ2luX2VjE...)")
    print("    ⚠️  No se mostrará al escribir")
    session_token = getpass.getpass("    Pega aquí: ").strip()
    
    if not access_key or not secret_key or not session_token:
        print("\n❌ Error: Todas las credenciales son obligatorias para AWS Academy")
        sys.exit(1)
    
    # Validar
    print("\n" + "=" * 70)
    print("🔍 Validando credenciales...")
    print("=" * 70)
    
    identity = None
    credentials_valid = False
    
    try:
        import boto3
        sts = boto3.client('sts',
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          aws_session_token=session_token,
                          region_name='us-east-1')
        identity = sts.get_caller_identity()
        credentials_valid = True
        
        print(f"\n✅ Credenciales válidas!")
        print(f"   Cuenta: {identity['Account']}")
        print(f"   Usuario: {identity['Arn'].split('/')[-1]}")
        
        # Probar Bedrock
        bedrock = boto3.client('bedrock',
                              aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key,
                              aws_session_token=session_token,
                              region_name='us-east-1')
        models = bedrock.list_foundation_models()
        print(f"✅ Acceso a Bedrock confirmado ({len(models['modelSummaries'])} modelos)")
        
    except Exception as e:
        print(f"\n⚠️  Advertencia: {str(e)[:100]}")
        confirm = input("\n¿Guardar de todos modos? [s/N]: ").strip().lower()
        if confirm != 's':
            sys.exit(1)
    
    # Guardar
    print("\n" + "=" * 70)
    print("💾 Guardando configuración...")
    print("=" * 70)
    
    env_file = Path(".env")
    
    # Backup
    if env_file.exists():
        backup = Path(f".env.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        import shutil
        shutil.copy(env_file, backup)
        print(f"✅ Backup: {backup}")
    
    # Leer valores actuales
    env_vars = {}
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    
    # Actualizar credenciales
    env_vars['AWS_REGION'] = 'us-east-1'
    env_vars['AWS_ACCESS_KEY_ID'] = access_key
    env_vars['AWS_SECRET_ACCESS_KEY'] = secret_key
    env_vars['AWS_SESSION_TOKEN'] = session_token
    
    # Defaults si no existen
    account_id = identity['Account'] if identity and credentials_valid else '123456789012'
    defaults = {
        'S3_BUCKET_NAME': f'docsmart-documents-{account_id}',
        'S3_EMBEDDINGS_FOLDER': 'embeddings/',
        'DB_HOST': 'sqlite',
        'DB_PORT': '5432',
        'DB_NAME': 'docsmart.db',
        'DB_USER': '',
        'DB_PASSWORD': '',
        'BEDROCK_EMBEDDING_MODEL': 'amazon.titan-embed-text-v2:0',
        'BEDROCK_LLM_MODEL': 'anthropic.claude-3-5-sonnet-20240620-v1:0',
        'MAX_TOKENS': '4096',
        'TEMPERATURE': '0.7',
        'TOP_P': '0.9',
        'CHUNK_SIZE': '1000',
        'CHUNK_OVERLAP': '200',
        'TOP_K_RESULTS': '5',
        'ENABLE_GUARDRAILS': 'true',
        'MAX_QUERY_LENGTH': '2000',
        'ALLOWED_FILE_TYPES': 'pdf,docx,txt,md'
    }
    
    for key, value in defaults.items():
        if key not in env_vars:
            env_vars[key] = value
    
    # Escribir archivo
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write("# DocSmart RAG System - AWS Academy Configuration\n")
        f.write(f"# Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# ⚠️  NUNCA COMPARTIR - Contiene credenciales sensibles\n\n")
        
        f.write("# AWS Configuration (AWS Academy)\n")
        f.write(f"AWS_REGION={env_vars['AWS_REGION']}\n")
        f.write(f"AWS_ACCESS_KEY_ID={env_vars['AWS_ACCESS_KEY_ID']}\n")
        f.write(f"AWS_SECRET_ACCESS_KEY={env_vars['AWS_SECRET_ACCESS_KEY']}\n")
        f.write(f"AWS_SESSION_TOKEN={env_vars['AWS_SESSION_TOKEN']}\n\n")
        
        f.write("# S3 Configuration\n")
        f.write(f"S3_BUCKET_NAME={env_vars['S3_BUCKET_NAME']}\n")
        f.write(f"S3_EMBEDDINGS_FOLDER={env_vars['S3_EMBEDDINGS_FOLDER']}\n\n")
        
        f.write("# Database Configuration (SQLite local para testing)\n")
        f.write(f"DB_HOST={env_vars['DB_HOST']}\n")
        f.write(f"DB_PORT={env_vars['DB_PORT']}\n")
        f.write(f"DB_NAME={env_vars['DB_NAME']}\n")
        f.write(f"DB_USER={env_vars['DB_USER']}\n")
        f.write(f"DB_PASSWORD={env_vars['DB_PASSWORD']}\n\n")
        
        f.write("# Bedrock Configuration\n")
        f.write(f"BEDROCK_EMBEDDING_MODEL={env_vars['BEDROCK_EMBEDDING_MODEL']}\n")
        f.write(f"BEDROCK_LLM_MODEL={env_vars['BEDROCK_LLM_MODEL']}\n\n")
        
        f.write("# Application Configuration\n")
        f.write(f"MAX_TOKENS={env_vars['MAX_TOKENS']}\n")
        f.write(f"TEMPERATURE={env_vars['TEMPERATURE']}\n")
        f.write(f"TOP_P={env_vars['TOP_P']}\n")
        f.write(f"CHUNK_SIZE={env_vars['CHUNK_SIZE']}\n")
        f.write(f"CHUNK_OVERLAP={env_vars['CHUNK_OVERLAP']}\n")
        f.write(f"TOP_K_RESULTS={env_vars['TOP_K_RESULTS']}\n\n")
        
        f.write("# Security\n")
        f.write(f"ENABLE_GUARDRAILS={env_vars['ENABLE_GUARDRAILS']}\n")
        f.write(f"MAX_QUERY_LENGTH={env_vars['MAX_QUERY_LENGTH']}\n")
        f.write(f"ALLOWED_FILE_TYPES={env_vars['ALLOWED_FILE_TYPES']}\n")
    
    print(f"✅ Configuración guardada: {env_file}")
    
    # Crear bucket S3 si no existe
    if credentials_valid:
        try:
            import boto3
            s3 = boto3.client('s3',
                             aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key,
                             aws_session_token=session_token,
                             region_name='us-east-1')
            bucket_name = env_vars['S3_BUCKET_NAME']
            
            try:
                s3.head_bucket(Bucket=bucket_name)
                print(f"✅ Bucket S3 existe: {bucket_name}")
            except:
                print(f"\nℹ️  Bucket '{bucket_name}' no existe")
                create = input("   ¿Crear bucket ahora? [S/n]: ").strip().lower()
                if create != 'n':
                    s3.create_bucket(Bucket=bucket_name)
                    print(f"✅ Bucket creado: {bucket_name}")
        except Exception as e:
            print(f"⚠️  No se pudo verificar/crear bucket S3: {str(e)[:50]}")
    else:
        print("⚠️  Saltando verificación de S3 (credenciales no validadas)")
    
    # Resumen final
    print("\n" + "=" * 70)
    print("✨ ¡Configuración Completada!")
    print("=" * 70)
    print("\n📋 Próximos pasos:\n")
    print("  1. Verificar AWS:  aws sts get-caller-identity")
    print("  2. Probar Bedrock: python test_bedrock.py")
    print("  3. Inicializar:    python cli.py setup")
    print("  4. Ingestar docs:  python cli.py ingest -f sample_docs/")
    print("  5. Consultar:      python cli.py query '¿Cuántos días de vacaciones?'")
    print("  6. Interfaz web:   streamlit run app.py")
    print("\n🚀 ¡Sistema listo!\n")
    
    print("⚠️  RECORDATORIO:")
    print("   • Las credenciales expiran en ~3-4 horas")
    print("   • Regenera desde AWS Academy cuando expiren")
    print("   • Ejecuta nuevamente: python aws_academy_config.py")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
