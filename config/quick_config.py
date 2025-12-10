#!/usr/bin/env python3
"""
Configuración Rápida de Credenciales AWS
Script simplificado para cambiar credenciales rápidamente
"""

import os
import sys
import getpass
from pathlib import Path
from datetime import datetime

def print_header(text):
    """Imprime encabezado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_success(text):
    print(f"✅ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def quick_configure():
    """Configuración rápida de credenciales AWS"""
    
    print_header("⚡ Configuración Rápida de Credenciales AWS")
    
    print_info("Este script actualiza SOLO las credenciales AWS")
    print_info("Para configuración completa, usa: python configure.py\n")
    
    # Leer .env actual
    env_file = Path(".env")
    env_vars = {}
    
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        print_success(f"Archivo .env encontrado ({len(env_vars)} variables)\n")
    else:
        print_warning("Archivo .env no existe. Se creará uno nuevo.\n")
    
    # Solicitar credenciales
    print("📝 Ingresa tus credenciales AWS:")
    print("-" * 70)
    
    # Región
    current_region = env_vars.get('AWS_REGION', 'us-east-1')
    region = input(f"AWS Region [{current_region}]: ").strip() or current_region
    
    # Access Key ID
    print("\n1️⃣ ID de clave de acceso AWS (Access Key ID)")
    print("   Ejemplo: AKIAIOSFODNN7EXAMPLE o ASIAVVIKEY3FMCTKCQA2")
    current_access = env_vars.get('AWS_ACCESS_KEY_ID', '')
    if current_access:
        masked = current_access[:4] + "*" * (len(current_access) - 8) + current_access[-4:]
        print(f"   Actual: {masked}")
    access_key = input(f"   Ingresa: ").strip()
    if not access_key and current_access:
        access_key = current_access
        print_info(f"   Manteniendo Access Key actual")
    
    # Secret Access Key
    print("\n2️⃣ Clave de acceso secreta AWS (Secret Access Key)")
    print("   Ejemplo: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
    print("   ⚠️  No se mostrará al escribir (seguridad)")
    secret_key = getpass.getpass("   Ingresa: ").strip()
    if not secret_key and env_vars.get('AWS_SECRET_ACCESS_KEY'):
        keep = input("   ¿Mantener Secret Key actual? [S/n]: ").strip().lower()
        if keep != 'n':
            secret_key = env_vars.get('AWS_SECRET_ACCESS_KEY')
            print_info("   Manteniendo Secret Key actual")
    
    # Session Token
    print("\n3️⃣ Token de sesión AWS (Session Token)")
    print("   Solo si usas AWS Academy/voclabs (credenciales temporales)")
    print("   Déjalo vacío si usas credenciales permanentes (IAM User)")
    print("   ⚠️  No se mostrará al escribir (seguridad)")
    session_token = getpass.getpass("   Ingresa (opcional): ").strip()
    if not session_token and env_vars.get('AWS_SESSION_TOKEN'):
        keep = input("   ¿Mantener Session Token actual? [S/n]: ").strip().lower()
        if keep != 'n':
            session_token = env_vars.get('AWS_SESSION_TOKEN')
            print_info("   Manteniendo Session Token actual")
    
    # Validación básica
    print("\n" + "=" * 70)
    print("🔍 Validación de credenciales...")
    print("=" * 70)
    
    if not access_key or not secret_key:
        print_warning("⚠️  Credenciales incompletas (se guardarán de todos modos)")
    else:
        # Validar con boto3
        try:
            import boto3
            session_config = {
                'aws_access_key_id': access_key,
                'aws_secret_access_key': secret_key,
                'region_name': region
            }
            if session_token:
                session_config['aws_session_token'] = session_token
            
            sts = boto3.client('sts', **session_config)
            identity = sts.get_caller_identity()
            
            print_success(f"Credenciales válidas")
            print_info(f"Cuenta AWS: {identity['Account']}")
            print_info(f"Usuario/Role: {identity['Arn'].split('/')[-1]}")
            
            # Verificar Bedrock
            try:
                bedrock = boto3.client('bedrock', **session_config)
                models = bedrock.list_foundation_models()
                print_success(f"Acceso a Bedrock confirmado ({len(models['modelSummaries'])} modelos)")
            except Exception as e:
                print_warning(f"No se pudo verificar Bedrock: {str(e)[:50]}...")
                
        except Exception as e:
            print_warning(f"No se pudieron validar credenciales: {str(e)[:80]}...")
            confirm = input("\n¿Continuar de todos modos? [s/N]: ").strip().lower()
            if confirm != 's':
                print("\n❌ Configuración cancelada")
                sys.exit(1)
    
    # Actualizar .env
    print("\n" + "=" * 70)
    print("💾 Guardando configuración...")
    print("=" * 70)
    
    # Backup
    if env_file.exists():
        backup_file = Path(f".env.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        import shutil
        shutil.copy(env_file, backup_file)
        print_success(f"Backup creado: {backup_file}")
    
    # Actualizar variables
    env_vars['AWS_REGION'] = region
    env_vars['AWS_ACCESS_KEY_ID'] = access_key
    if secret_key:
        env_vars['AWS_SECRET_ACCESS_KEY'] = secret_key
    if session_token:
        env_vars['AWS_SESSION_TOKEN'] = session_token
    elif 'AWS_SESSION_TOKEN' in env_vars and not session_token:
        # Eliminar session token si se dejó vacío
        pass  # Lo mantendremos para no romper nada
    
    # Escribir .env
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write("# DocSmart RAG System - Configuración\n")
        f.write(f"# Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# ⚠️  NO COMPARTIR este archivo - Contiene credenciales sensibles\n\n")
        
        # AWS Configuration
        f.write("# AWS Configuration\n")
        f.write(f"AWS_REGION={env_vars.get('AWS_REGION', 'us-east-1')}\n")
        f.write(f"AWS_ACCESS_KEY_ID={env_vars.get('AWS_ACCESS_KEY_ID', '')}\n")
        f.write(f"AWS_SECRET_ACCESS_KEY={env_vars.get('AWS_SECRET_ACCESS_KEY', '')}\n")
        if env_vars.get('AWS_SESSION_TOKEN'):
            f.write(f"AWS_SESSION_TOKEN={env_vars.get('AWS_SESSION_TOKEN', '')}\n")
        f.write("\n")
        
        # Mantener otras secciones si existen
        for key in ['S3_BUCKET_NAME', 'S3_EMBEDDINGS_FOLDER', 'DB_HOST', 'DB_PORT', 
                   'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'BEDROCK_EMBEDDING_MODEL',
                   'BEDROCK_LLM_MODEL', 'MAX_TOKENS', 'TEMPERATURE', 'TOP_P',
                   'CHUNK_SIZE', 'CHUNK_OVERLAP', 'TOP_K_RESULTS', 'ENABLE_GUARDRAILS',
                   'MAX_QUERY_LENGTH', 'ALLOWED_FILE_TYPES']:
            if key in env_vars:
                # Agrupar por sección
                if key == 'S3_BUCKET_NAME':
                    f.write("# S3 Configuration\n")
                elif key == 'DB_HOST':
                    f.write("# Database Configuration\n")
                elif key == 'BEDROCK_EMBEDDING_MODEL':
                    f.write("# Bedrock Configuration\n")
                elif key == 'MAX_TOKENS':
                    f.write("# Application Configuration\n")
                elif key == 'ENABLE_GUARDRAILS':
                    f.write("# Security\n")
                
                f.write(f"{key}={env_vars[key]}\n")
                
                # Saltos de línea entre secciones
                if key in ['S3_EMBEDDINGS_FOLDER', 'DB_PASSWORD', 'BEDROCK_LLM_MODEL', 
                          'TOP_K_RESULTS', 'ALLOWED_FILE_TYPES']:
                    f.write("\n")
    
    print_success(f"Configuración guardada en {env_file}")
    
    # Resumen
    print("\n" + "=" * 70)
    print("✨ ¡Configuración Completada!")
    print("=" * 70)
    print("\n📋 Próximos pasos:")
    print("  1. Verificar: aws sts get-caller-identity")
    print("  2. Probar Bedrock: python test_bedrock.py")
    print("  3. Inicializar DB: python cli.py setup")
    print("  4. Ingestar docs: python cli.py ingest -f sample_docs/")
    print("  5. Consultar: python cli.py query 'tu pregunta'")
    print("\n🚀 Sistema listo para usar!\n")
    
    print_warning("⚠️  IMPORTANTE:")
    print("   - NO compartas el archivo .env")
    print("   - NO lo subas a git/GitHub")
    print("   - Credenciales temporales expiran (típicamente 3-4 horas)")
    print("   - Regenera desde AWS Academy cuando expiren\n")

if __name__ == "__main__":
    try:
        quick_configure()
    except KeyboardInterrupt:
        print("\n\n❌ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        sys.exit(1)
