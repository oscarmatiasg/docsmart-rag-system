#!/usr/bin/env python3
"""
Script de Configuración Segura para DocSmart RAG System
Permite configurar credenciales AWS y otros parámetros de forma segura
"""

import os
import sys
import getpass
import json
import boto3
from pathlib import Path
from typing import Optional, Dict

class SecureConfigurator:
    """Configurador seguro para DocSmart"""
    
    def __init__(self):
        self.env_file = Path(".env")
        self.env_example = Path(".env.example")
        self.config = {}
        
    def print_header(self, text: str):
        """Imprime un encabezado formateado"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60 + "\n")
    
    def print_info(self, text: str):
        """Imprime información"""
        print(f"ℹ️  {text}")
    
    def print_success(self, text: str):
        """Imprime mensaje de éxito"""
        print(f"✅ {text}")
    
    def print_error(self, text: str):
        """Imprime mensaje de error"""
        print(f"❌ {text}")
    
    def print_warning(self, text: str):
        """Imprime advertencia"""
        print(f"⚠️  {text}")
    
    def read_current_env(self) -> Dict[str, str]:
        """Lee el archivo .env actual si existe"""
        if not self.env_file.exists():
            return {}
        
        env_vars = {}
        with open(self.env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        return env_vars
    
    def get_input(self, prompt: str, default: str = "", secret: bool = False) -> str:
        """Obtiene input del usuario"""
        if default:
            prompt_text = f"{prompt} [{default}]: "
        else:
            prompt_text = f"{prompt}: "
        
        if secret:
            value = getpass.getpass(prompt_text)
            return value if value else default
        else:
            value = input(prompt_text)
            return value if value else default
    
    def get_yes_no(self, prompt: str, default: bool = True) -> bool:
        """Obtiene respuesta sí/no del usuario"""
        default_str = "S/n" if default else "s/N"
        response = input(f"{prompt} [{default_str}]: ").strip().lower()
        
        if not response:
            return default
        return response in ['s', 'si', 'sí', 'y', 'yes']
    
    def validate_aws_credentials(self, access_key: str, secret_key: str, 
                                 session_token: Optional[str], region: str) -> bool:
        """Valida las credenciales AWS"""
        try:
            self.print_info("Validando credenciales AWS...")
            
            # Crear cliente STS para validar
            session_config = {
                'aws_access_key_id': access_key,
                'aws_secret_access_key': secret_key,
                'region_name': region
            }
            
            if session_token:
                session_config['aws_session_token'] = session_token
            
            sts = boto3.client('sts', **session_config)
            identity = sts.get_caller_identity()
            
            self.print_success(f"Credenciales válidas para cuenta: {identity['Account']}")
            self.print_info(f"Usuario/Role: {identity['Arn']}")
            return True
            
        except Exception as e:
            self.print_error(f"Error validando credenciales: {str(e)}")
            return False
    
    def validate_bedrock_access(self, access_key: str, secret_key: str,
                                session_token: Optional[str], region: str) -> bool:
        """Valida acceso a Amazon Bedrock"""
        try:
            self.print_info("Verificando acceso a Amazon Bedrock...")
            
            session_config = {
                'aws_access_key_id': access_key,
                'aws_secret_access_key': secret_key,
                'region_name': region
            }
            
            if session_token:
                session_config['aws_session_token'] = session_token
            
            bedrock = boto3.client('bedrock', **session_config)
            models = bedrock.list_foundation_models()
            
            # Verificar modelos específicos
            required_models = {
                'titan-embed': False,
                'claude': False
            }
            
            for model in models['modelSummaries']:
                model_id = model['modelId'].lower()
                if 'titan-embed' in model_id:
                    required_models['titan-embed'] = True
                if 'claude' in model_id:
                    required_models['claude'] = True
            
            if all(required_models.values()):
                self.print_success("Acceso a Bedrock confirmado (Titan Embeddings + Claude)")
                return True
            else:
                self.print_warning("Acceso parcial a Bedrock")
                return True
                
        except Exception as e:
            self.print_error(f"Error verificando Bedrock: {str(e)}")
            return False
    
    def check_s3_bucket(self, bucket_name: str, access_key: str, secret_key: str,
                       session_token: Optional[str], region: str) -> bool:
        """Verifica si el bucket S3 existe o puede crearse"""
        try:
            session_config = {
                'aws_access_key_id': access_key,
                'aws_secret_access_key': secret_key,
                'region_name': region
            }
            
            if session_token:
                session_config['aws_session_token'] = session_token
            
            s3 = boto3.client('s3', **session_config)
            
            # Intentar listar el bucket
            try:
                s3.head_bucket(Bucket=bucket_name)
                self.print_success(f"Bucket '{bucket_name}' existe y es accesible")
                return True
            except:
                # Bucket no existe, preguntar si crear
                if self.get_yes_no(f"Bucket '{bucket_name}' no existe. ¿Crear ahora?", True):
                    s3.create_bucket(Bucket=bucket_name)
                    self.print_success(f"Bucket '{bucket_name}' creado exitosamente")
                    return True
                else:
                    self.print_warning("Bucket no creado. Configúralo manualmente más tarde.")
                    return True
                    
        except Exception as e:
            self.print_error(f"Error verificando S3: {str(e)}")
            return False
    
    def configure_aws(self):
        """Configura credenciales AWS"""
        self.print_header("Configuración de AWS")
        
        current_env = self.read_current_env()
        
        self.print_info("Ingresa tus credenciales AWS (típicamente desde AWS Academy/Console)")
        
        # AWS Region
        default_region = current_env.get('AWS_REGION', 'us-east-1')
        region = self.get_input("AWS Region", default_region)
        
        # Access Key ID
        default_access = current_env.get('AWS_ACCESS_KEY_ID', '')
        if default_access:
            masked_access = default_access[:4] + "*" * (len(default_access) - 8) + default_access[-4:]
            self.print_info(f"Access Key actual: {masked_access}")
        access_key = self.get_input("ID de clave de acceso AWS (Access Key ID)", default_access, secret=False)
        
        # Secret Access Key
        self.print_warning("La Secret Key no se mostrará al escribir (seguridad)")
        secret_key = self.get_input("Clave de acceso secreta AWS (Secret Access Key)", "", secret=True)
        if not secret_key and current_env.get('AWS_SECRET_ACCESS_KEY'):
            if self.get_yes_no("¿Mantener Secret Key actual?", True):
                secret_key = current_env.get('AWS_SECRET_ACCESS_KEY')
        
        # Session Token (siempre preguntar)
        self.print_info("\nSi usas AWS Academy/voclabs, necesitas el Session Token")
        self.print_info("Si usas credenciales permanentes (IAM User), déjalo vacío")
        self.print_warning("El Session Token no se mostrará al escribir (seguridad)")
        session_token = self.get_input("Token de sesión AWS (Session Token, opcional)", "", secret=True)
        if not session_token and current_env.get('AWS_SESSION_TOKEN'):
            if self.get_yes_no("¿Mantener Session Token actual?", True):
                session_token = current_env.get('AWS_SESSION_TOKEN')
        
        # Validar credenciales
        if secret_key:  # Solo validar si hay secret key
            if not self.validate_aws_credentials(access_key, secret_key, session_token, region):
                if not self.get_yes_no("Credenciales inválidas. ¿Continuar de todos modos?", False):
                    sys.exit(1)
            
            # Validar Bedrock
            self.validate_bedrock_access(access_key, secret_key, session_token, region)
        else:
            self.print_warning("No se proporcionó Secret Key, saltando validación")
        
        # Guardar configuración
        self.config['AWS_REGION'] = region
        self.config['AWS_ACCESS_KEY_ID'] = access_key
        if secret_key:
            self.config['AWS_SECRET_ACCESS_KEY'] = secret_key
        if session_token:
            self.config['AWS_SESSION_TOKEN'] = session_token
        
        return True
    
    def configure_s3(self):
        """Configura S3"""
        self.print_header("Configuración de Amazon S3")
        
        current_env = self.read_current_env()
        
        # Sugerir nombre de bucket
        account_id = ""
        try:
            sts = boto3.client('sts',
                             aws_access_key_id=self.config['AWS_ACCESS_KEY_ID'],
                             aws_secret_access_key=self.config['AWS_SECRET_ACCESS_KEY'],
                             aws_session_token=self.config.get('AWS_SESSION_TOKEN'),
                             region_name=self.config['AWS_REGION'])
            identity = sts.get_caller_identity()
            account_id = identity['Account']
        except:
            pass
        
        default_bucket = current_env.get('S3_BUCKET_NAME', f'docsmart-documents-{account_id}')
        bucket_name = self.get_input("Nombre del bucket S3", default_bucket)
        
        # Verificar bucket
        self.check_s3_bucket(bucket_name, 
                            self.config['AWS_ACCESS_KEY_ID'],
                            self.config['AWS_SECRET_ACCESS_KEY'],
                            self.config.get('AWS_SESSION_TOKEN'),
                            self.config['AWS_REGION'])
        
        self.config['S3_BUCKET_NAME'] = bucket_name
        self.config['S3_EMBEDDINGS_FOLDER'] = 'embeddings/'
        
        return True
    
    def configure_bedrock(self):
        """Configura modelos de Bedrock"""
        self.print_header("Configuración de Amazon Bedrock")
        
        current_env = self.read_current_env()
        
        # Modelo de embeddings
        default_embed = current_env.get('BEDROCK_EMBEDDING_MODEL', 'amazon.titan-embed-text-v2:0')
        self.print_info("Modelos de Embeddings disponibles:")
        print("  1. amazon.titan-embed-text-v2:0 (Recomendado, 1024 dims)")
        print("  2. amazon.titan-embed-text-v1 (Legacy, 1536 dims)")
        
        embed_choice = input(f"Selecciona [1/2] o ingresa modelo [{default_embed}]: ").strip()
        if embed_choice == '1':
            embed_model = 'amazon.titan-embed-text-v2:0'
        elif embed_choice == '2':
            embed_model = 'amazon.titan-embed-text-v1'
        elif embed_choice:
            embed_model = embed_choice
        else:
            embed_model = default_embed
        
        # Modelo LLM
        default_llm = current_env.get('BEDROCK_LLM_MODEL', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
        self.print_info("\nModelos LLM disponibles:")
        print("  1. anthropic.claude-3-5-sonnet-20240620-v1:0 (Recomendado)")
        print("  2. anthropic.claude-3-haiku-20240307-v1:0 (Más rápido, más económico)")
        print("  3. anthropic.claude-3-opus-20240229-v1:0 (Más potente)")
        
        llm_choice = input(f"Selecciona [1/2/3] o ingresa modelo [{default_llm}]: ").strip()
        if llm_choice == '1':
            llm_model = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
        elif llm_choice == '2':
            llm_model = 'anthropic.claude-3-haiku-20240307-v1:0'
        elif llm_choice == '3':
            llm_model = 'anthropic.claude-3-opus-20240229-v1:0'
        elif llm_choice:
            llm_model = llm_choice
        else:
            llm_model = default_llm
        
        self.config['BEDROCK_EMBEDDING_MODEL'] = embed_model
        self.config['BEDROCK_LLM_MODEL'] = llm_model
        
        return True
    
    def configure_database(self):
        """Configura base de datos"""
        self.print_header("Configuración de Base de Datos")
        
        current_env = self.read_current_env()
        
        self.print_info("Opciones de base de datos:")
        print("  1. SQLite local (Recomendado para desarrollo/testing)")
        print("  2. Aurora PostgreSQL (Producción)")
        
        db_choice = input("Selecciona [1/2]: ").strip()
        
        if db_choice == '2':
            # PostgreSQL
            db_host = self.get_input("DB Host (endpoint)", 
                                    current_env.get('DB_HOST', 'localhost'))
            db_port = self.get_input("DB Port", 
                                    current_env.get('DB_PORT', '5432'))
            db_name = self.get_input("DB Name", 
                                    current_env.get('DB_NAME', 'docsmart_db'))
            db_user = self.get_input("DB User", 
                                    current_env.get('DB_USER', 'postgres'))
            db_password = self.get_input("DB Password", "", secret=True)
            
            self.config['DB_HOST'] = db_host
            self.config['DB_PORT'] = db_port
            self.config['DB_NAME'] = db_name
            self.config['DB_USER'] = db_user
            self.config['DB_PASSWORD'] = db_password
        else:
            # SQLite
            self.print_info("Usando SQLite local (./docsmart.db)")
            self.config['DB_HOST'] = 'sqlite'
            self.config['DB_PORT'] = '5432'
            self.config['DB_NAME'] = 'docsmart.db'
            self.config['DB_USER'] = ''
            self.config['DB_PASSWORD'] = ''
        
        return True
    
    def configure_application(self):
        """Configura parámetros de aplicación"""
        self.print_header("Configuración de Aplicación")
        
        current_env = self.read_current_env()
        
        # Parámetros por defecto
        self.config['MAX_TOKENS'] = current_env.get('MAX_TOKENS', '4096')
        self.config['TEMPERATURE'] = current_env.get('TEMPERATURE', '0.7')
        self.config['TOP_P'] = current_env.get('TOP_P', '0.9')
        self.config['CHUNK_SIZE'] = current_env.get('CHUNK_SIZE', '1000')
        self.config['CHUNK_OVERLAP'] = current_env.get('CHUNK_OVERLAP', '200')
        self.config['TOP_K_RESULTS'] = current_env.get('TOP_K_RESULTS', '5')
        
        if self.get_yes_no("¿Configurar parámetros avanzados?", False):
            self.config['MAX_TOKENS'] = self.get_input("Max Tokens", self.config['MAX_TOKENS'])
            self.config['TEMPERATURE'] = self.get_input("Temperature (0-1)", self.config['TEMPERATURE'])
            self.config['TOP_P'] = self.get_input("Top P (0-1)", self.config['TOP_P'])
            self.config['CHUNK_SIZE'] = self.get_input("Chunk Size", self.config['CHUNK_SIZE'])
            self.config['CHUNK_OVERLAP'] = self.get_input("Chunk Overlap", self.config['CHUNK_OVERLAP'])
            self.config['TOP_K_RESULTS'] = self.get_input("Top K Results", self.config['TOP_K_RESULTS'])
        
        # Security
        self.config['ENABLE_GUARDRAILS'] = 'true'
        self.config['MAX_QUERY_LENGTH'] = '2000'
        self.config['ALLOWED_FILE_TYPES'] = 'pdf,docx,txt,md'
        
        return True
    
    def save_env_file(self):
        """Guarda el archivo .env"""
        self.print_header("Guardando Configuración")
        
        # Backup del archivo anterior si existe
        if self.env_file.exists():
            backup_file = Path(".env.backup")
            import shutil
            shutil.copy(self.env_file, backup_file)
            self.print_info(f"Backup guardado en {backup_file}")
        
        # Escribir nuevo .env
        with open(self.env_file, 'w') as f:
            f.write("# DocSmart RAG System - Configuración\n")
            f.write("# Generado automáticamente por configure.py\n")
            f.write(f"# Fecha: {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}\n\n")
            
            # AWS Configuration
            f.write("# AWS Configuration\n")
            f.write(f"AWS_REGION={self.config.get('AWS_REGION', '')}\n")
            f.write(f"AWS_ACCESS_KEY_ID={self.config.get('AWS_ACCESS_KEY_ID', '')}\n")
            f.write(f"AWS_SECRET_ACCESS_KEY={self.config.get('AWS_SECRET_ACCESS_KEY', '')}\n")
            if 'AWS_SESSION_TOKEN' in self.config:
                f.write(f"AWS_SESSION_TOKEN={self.config.get('AWS_SESSION_TOKEN', '')}\n")
            f.write("\n")
            
            # S3 Configuration
            f.write("# S3 Configuration\n")
            f.write(f"S3_BUCKET_NAME={self.config.get('S3_BUCKET_NAME', '')}\n")
            f.write(f"S3_EMBEDDINGS_FOLDER={self.config.get('S3_EMBEDDINGS_FOLDER', 'embeddings/')}\n")
            f.write("\n")
            
            # Database Configuration
            f.write("# Database Configuration\n")
            f.write(f"DB_HOST={self.config.get('DB_HOST', '')}\n")
            f.write(f"DB_PORT={self.config.get('DB_PORT', '5432')}\n")
            f.write(f"DB_NAME={self.config.get('DB_NAME', '')}\n")
            f.write(f"DB_USER={self.config.get('DB_USER', '')}\n")
            f.write(f"DB_PASSWORD={self.config.get('DB_PASSWORD', '')}\n")
            f.write("\n")
            
            # Bedrock Configuration
            f.write("# Bedrock Configuration\n")
            f.write(f"BEDROCK_EMBEDDING_MODEL={self.config.get('BEDROCK_EMBEDDING_MODEL', '')}\n")
            f.write(f"BEDROCK_LLM_MODEL={self.config.get('BEDROCK_LLM_MODEL', '')}\n")
            f.write("\n")
            
            # Application Configuration
            f.write("# Application Configuration\n")
            f.write(f"MAX_TOKENS={self.config.get('MAX_TOKENS', '4096')}\n")
            f.write(f"TEMPERATURE={self.config.get('TEMPERATURE', '0.7')}\n")
            f.write(f"TOP_P={self.config.get('TOP_P', '0.9')}\n")
            f.write(f"CHUNK_SIZE={self.config.get('CHUNK_SIZE', '1000')}\n")
            f.write(f"CHUNK_OVERLAP={self.config.get('CHUNK_OVERLAP', '200')}\n")
            f.write(f"TOP_K_RESULTS={self.config.get('TOP_K_RESULTS', '5')}\n")
            f.write("\n")
            
            # Security
            f.write("# Security\n")
            f.write(f"ENABLE_GUARDRAILS={self.config.get('ENABLE_GUARDRAILS', 'true')}\n")
            f.write(f"MAX_QUERY_LENGTH={self.config.get('MAX_QUERY_LENGTH', '2000')}\n")
            f.write(f"ALLOWED_FILE_TYPES={self.config.get('ALLOWED_FILE_TYPES', 'pdf,docx,txt,md')}\n")
        
        self.print_success(f"Configuración guardada en {self.env_file}")
        self.print_warning("⚠️  NO COMPARTAS este archivo .env con nadie")
        self.print_warning("⚠️  NO SUBAS este archivo a git/GitHub")
        
        return True
    
    def run(self):
        """Ejecuta el configurador completo"""
        try:
            print("\n")
            print("🔒 " + "=" * 58 + " 🔒")
            print("   DocSmart RAG System - Configuración Segura")
            print("🔒 " + "=" * 58 + " 🔒")
            print("\n")
            
            self.print_warning("Este script te ayudará a configurar tus credenciales de forma segura")
            self.print_info("Presiona Ctrl+C en cualquier momento para cancelar\n")
            
            # Paso 1: AWS
            if not self.configure_aws():
                return False
            
            # Paso 2: S3
            if not self.configure_s3():
                return False
            
            # Paso 3: Bedrock
            if not self.configure_bedrock():
                return False
            
            # Paso 4: Database
            if not self.configure_database():
                return False
            
            # Paso 5: Application
            if not self.configure_application():
                return False
            
            # Paso 6: Guardar
            if not self.save_env_file():
                return False
            
            # Resumen final
            self.print_header("¡Configuración Completada!")
            print("Próximos pasos:")
            print("  1. Inicializar base de datos: python cli.py setup")
            print("  2. Ingestar documentos: python cli.py ingest -f sample_docs/")
            print("  3. Realizar consultas: python cli.py query 'tu pregunta'")
            print("  4. Lanzar interfaz web: streamlit run app.py")
            print("\n")
            self.print_success("¡Sistema listo para usar! 🚀\n")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n")
            self.print_warning("Configuración cancelada por el usuario")
            return False
        except Exception as e:
            self.print_error(f"Error durante configuración: {str(e)}")
            return False


def main():
    """Función principal"""
    configurator = SecureConfigurator()
    success = configurator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
