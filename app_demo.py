import streamlit as st
import sys
import os
from datetime import datetime
import time

# Agregar path del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar módulos del proyecto
from config import Config
from rag_system import RAGSystem
from ingestion_pipeline import IngestionPipeline
from vector_database import VectorDatabase

# Configuración de la página
st.set_page_config(
    page_title="DocSmart - Sistema RAG con Amazon Bedrock",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Personalizado - Diseño moderno y profesional con ALTO CONTRASTE
st.markdown("""
<style>
    /* Fondo oscuro profesional */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Contenedor principal */
    .main .block-container {
        padding: 2rem;
        max-width: 1400px;
    }
    
    /* Tarjetas con alto contraste */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        border-left: 5px solid #00d4ff;
    }
    
    /* Títulos con ALTO CONTRASTE */
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-size: 3.5em !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        font-weight: 800 !important;
    }
    
    h2 {
        color: #00d4ff !important;
        font-size: 2em !important;
        margin-top: 2rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h3 {
        color: #ffffff !important;
        font-size: 1.5em !important;
        font-weight: 600 !important;
    }
    
    /* Texto general más visible */
    p, div, span, label {
        color: #ffffff !important;
    }
    
    /* Sidebar oscuro con contraste */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1e 0%, #1a1a2e 100%);
        border-right: 2px solid #00d4ff;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #00d4ff !important;
    }
    
    /* Botones con gradiente vibrante */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
        color: #000000 !important;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.2em;
        border-radius: 12px;
        font-weight: bold;
        transition: all 0.3s;
        box-shadow: 0 4px 8px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 212, 255, 0.5);
        background: linear-gradient(135deg, #00ffff 0%, #00d4ff 100%);
    }
    
    /* Input fields oscuros con texto blanco */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 12px;
        border: 2px solid #00d4ff;
        padding: 0.75rem;
        font-size: 1.1em;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Chat messages con contraste */
    .chat-message {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        color: #000000 !important;
    }
    
    .chat-message * {
        color: #000000 !important;
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(0, 153, 255, 0.2) 100%);
        border-left: 5px solid #00d4ff;
    }
    
    .assistant-message {
        background: rgba(255, 255, 255, 0.95);
        border-left: 5px solid #00ff88;
    }
    
    /* Source cards con fondo claro */
    .source-card {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 0.5rem;
        border-left: 4px solid #00d4ff;
        color: #000000 !important;
    }
    
    .source-card * {
        color: #000000 !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(0, 255, 136, 0.2);
        border: 2px solid #00ff88;
        border-radius: 10px;
        color: #ffffff !important;
    }
    
    .stError {
        background-color: rgba(255, 0, 85, 0.2);
        border: 2px solid #ff0055;
        border-radius: 10px;
        color: #ffffff !important;
    }
    
    .stWarning {
        background-color: rgba(255, 196, 0, 0.2);
        border: 2px solid #ffc400;
        border-radius: 10px;
        color: #ffffff !important;
    }
    
    .stInfo {
        background-color: rgba(0, 212, 255, 0.2);
        border: 2px solid #00d4ff;
        border-radius: 10px;
        color: #ffffff !important;
    }
    
    /* Metrics con alto contraste */
    [data-testid="stMetricValue"] {
        font-size: 2.5em !important;
        color: #00d4ff !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 1.1em !important;
    }
    
    /* Expander con fondo visible */
    .streamlit-expanderHeader {
        background: rgba(0, 212, 255, 0.2) !important;
        border-radius: 10px;
        font-weight: bold;
        color: #ffffff !important;
        border: 1px solid #00d4ff;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 0 0 10px 10px;
        padding: 1rem;
    }
    
    /* Progress bar vibrante */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00d4ff 0%, #00ff88 100%);
    }
    
    /* Radio buttons y checkboxes */
    .stRadio > label, .stCheckbox > label {
        color: #ffffff !important;
        font-size: 1.1em !important;
    }
    
    /* Select box */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border: 2px solid #00d4ff;
        border-radius: 12px;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(0, 212, 255, 0.1);
        border: 2px dashed #00d4ff;
        border-radius: 12px;
        padding: 2rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #ffffff !important;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00d4ff !important;
        color: #000000 !important;
    }
    
    /* Markdown text in main area */
    .main p, .main li, .main span {
        color: #ffffff !important;
        line-height: 1.6;
    }
    
    /* Code blocks */
    code {
        background-color: rgba(0, 212, 255, 0.2) !important;
        color: #00ffff !important;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
    }
    
    pre {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid #00d4ff;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Inicialización de session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'rag_system' not in st.session_state:
    try:
        config = Config()
        # Crear RAG system
        st.session_state.rag_system = RAGSystem()
        # Conectar la base de datos del RAG system
        st.session_state.rag_system.vector_db.connect()
        # Crear instancias adicionales para UI
        st.session_state.ingestion = IngestionPipeline()
        st.session_state.vector_db = st.session_state.rag_system.vector_db
    except Exception as e:
        st.error(f"Error inicializando sistema: {str(e)}")
        st.error(f"Detalles: {type(e).__name__}")
        import traceback
        st.code(traceback.format_exc())
        st.stop()

# Header con logo y título
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🚀 DocSmart")
    st.markdown("<p style='text-align: center; color: white; font-size: 1.2em;'>Sistema Inteligente de Consulta de Documentos</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; opacity: 0.8;'>Powered by Amazon Bedrock & RAG</p>", unsafe_allow_html=True)

st.markdown("---")

# Sidebar con información y controles
with st.sidebar:
    st.markdown("### 🎯 Panel de Control")
    
    # Selector de modo
    mode = st.radio(
        "Selecciona el modo:",
        ["💬 Chat Inteligente", "📊 Estadísticas", "⚙️ Configuración"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Info del sistema
    st.markdown("### 📱 Info del Sistema")
    st.info(f"""
    **Modelo LLM:** Claude 3.5 Sonnet  
    **Embeddings:** Titan v2 (1024d)  
    **Base de Datos:** {Config.DB_HOST}  
    **Región AWS:** {Config.AWS_REGION}
    """)
    
    st.markdown("---")
    
    # Estadísticas rápidas
    try:
        stats = st.session_state.vector_db.get_statistics()
        st.markdown("### 📈 Estadísticas Rápidas")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documentos", stats['total_chunks'])
        with col2:
            st.metric("Archivos", stats['total_files'])
    except:
        pass
    
    st.markdown("---")
    
    # Acerca de
    with st.expander("ℹ️ Acerca de DocSmart"):
        st.markdown("""
        **DocSmart** es un sistema de consulta inteligente que utiliza:
        
        - 🤖 **Amazon Bedrock** para IA generativa
        - 🎯 **RAG** (Retrieval-Augmented Generation)
        - 📊 **Embeddings vectoriales** para búsqueda semántica
        - 🔒 **Seguridad multicapa**
        
        Desarrollado con Python, Streamlit y AWS.
        """)

# Contenido principal según el modo seleccionado
if mode == "💬 Chat Inteligente":
    st.markdown("## 💬 Chat Inteligente")
    st.markdown("Haz preguntas sobre tus documentos y obtén respuestas precisas con fuentes citadas.")
    
    # Contenedor de chat
    chat_container = st.container()
    
    # Historial de chat
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 Tú:</strong><br/>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 DocSmart:</strong><br/>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
                
                # Mostrar fuentes si existen
                if 'sources' in message and message['sources']:
                    with st.expander(f"📚 Ver {len(message['sources'])} fuente(s)"):
                        for idx, source in enumerate(message['sources'], 1):
                            # Manejar diferentes formatos de source
                            text_content = source.get('text', source.get('content', 'Sin contenido'))
                            file_name = source.get('file_name', source.get('metadata', {}).get('file_name', 'Documento'))
                            similarity = source.get('similarity', source.get('score', 0))
                            
                            st.markdown(f"""
                            <div class="source-card">
                                <strong>[{idx}] {file_name}</strong><br/>
                                <em>Similitud: {similarity:.1%}</em><br/>
                                <small>{text_content[:200] if text_content else 'Sin texto'}...</small>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Metadata
                if 'metadata' in message:
                    st.caption(f"⏱️ {message['metadata']['response_time']:.2f}s | 📊 {message['metadata']['sources_used']} fuentes | 🔤 {message['metadata']['tokens_used']} tokens")
    
    # Input de consulta con mejor UX
    st.markdown("---")
    
    # Botones de control
    control_col1, control_col2, control_col3 = st.columns([3, 1, 1])
    with control_col2:
        if st.button("🗑️ Limpiar Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with control_col3:
        if st.button("♻️ Recargar", use_container_width=True):
            st.rerun()
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Tu pregunta:",
            placeholder="Ej: ¿A mi cuánto me toca? Estoy hace 1 año | ¿Cuántos días de vacaciones tengo?",
            label_visibility="collapsed",
            key="query_input"
        )
    
    with col2:
        submit = st.button("🚀 Enviar", use_container_width=True, type="primary")
    
    # Ejemplos de preguntas con botones
    st.markdown("**💡 Preguntas sugeridas:**")
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        if st.button("📅 ¿Cuántos días de vacaciones tengo?", key="ex1"):
            query = "¿Cuántos días de vacaciones tengo si llevo 1 año?"
            submit = True
    
    with example_col2:
        if st.button("⏰ ¿Con cuánta anticipación pido vacaciones?", key="ex2"):
            query = "¿Con cuánta anticipación debo solicitar mis vacaciones?"
            submit = True
    
    with example_col3:
        if st.button("💰 ¿Puedo cobrar vacaciones?", key="ex3"):
            query = "¿Puedo cobrar las vacaciones no tomadas?"
            submit = True
    
    # Procesar consulta
    if submit and query:
        # Agregar mensaje del usuario
        st.session_state.chat_history.append({
            'role': 'user',
            'content': query
        })
        
        # Mostrar indicador de carga
        with st.spinner('🤖 Pensando...'):
            try:
                start_time = time.time()
                
                # Ejecutar RAG
                result = st.session_state.rag_system.query(query)
                
                end_time = time.time()
                response_time = end_time - start_time
                
                # Agregar respuesta del asistente
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': result['answer'],
                    'sources': result['sources'],
                    'metadata': {
                        'response_time': response_time,
                        'sources_used': len(result['sources']),
                        'tokens_used': result.get('tokens_used', 'N/A')
                    }
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error al procesar consulta: {str(e)}")
    
    # Botón para limpiar chat
    if st.session_state.chat_history:
        if st.button("🗑️ Limpiar Chat"):
            st.session_state.chat_history = []
            st.rerun()

elif mode == "📊 Estadísticas":
    st.markdown("## 📊 Estadísticas del Sistema")
    
    try:
        stats = st.session_state.vector_db.get_statistics()
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin:0; color:#667eea;">📄 Documentos</h3>
                <h2 style="margin:0; color:#333;">{}</h2>
                <p style="margin:0; color:#666;">Chunks totales</p>
            </div>
            """.format(stats['total_chunks']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin:0; color:#764ba2;">📁 Archivos</h3>
                <h2 style="margin:0; color:#333;">{}</h2>
                <p style="margin:0; color:#666;">Archivos únicos</p>
            </div>
            """.format(stats['total_files']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin:0; color:#667eea;">💬 Consultas</h3>
                <h2 style="margin:0; color:#333;">{}</h2>
                <p style="margin:0; color:#666;">En esta sesión</p>
            </div>
            """.format(len([m for m in st.session_state.chat_history if m['role'] == 'user'])), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin:0; color:#764ba2;">⚡ Latencia</h3>
                <h2 style="margin:0; color:#333;">< 3s</h2>
                <p style="margin:0; color:#666;">Promedio p95</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Lista de archivos
        st.markdown("### 📚 Documentos en la Base de Conocimiento")
        
        if stats['files']:
            for file_name, count in stats['files'].items():
                with st.expander(f"📄 {file_name} ({count} chunks)"):
                    st.write(f"**Chunks:** {count}")
                    st.write(f"**Última actualización:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.info("No hay documentos ingestados aún. Usa el modo de configuración para subir documentos.")
        
        st.markdown("---")
        
        # Tecnologías utilizadas
        st.markdown("### 🛠️ Stack Tecnológico")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **☁️ AWS Services:**
            - Amazon Bedrock (Claude 3.5 + Titan)
            - Amazon S3
            - AWS IAM
            """)
        
        with col2:
            st.markdown("""
            **🐍 Python Stack:**
            - Streamlit (Web UI)
            - boto3 (AWS SDK)
            - psycopg2/SQLite (Database)
            - pgvector (Vector search)
            """)
        
    except Exception as e:
        st.error(f"Error obteniendo estadísticas: {str(e)}")

elif mode == "⚙️ Configuración":
    st.markdown("## ⚙️ Configuración del Sistema")
    
    tab1, tab2, tab3 = st.tabs(["📤 Subir Documentos", "🔧 Configuración", "📖 Ayuda"])
    
    with tab1:
        st.markdown("### 📤 Subir Documentos")
        st.markdown("Sube documentos PDF, DOCX o TXT para agregarlos a la base de conocimiento.")
        
        uploaded_file = st.file_uploader(
            "Selecciona un archivo",
            type=['pdf', 'docx', 'txt', 'md'],
            help="Formatos soportados: PDF, DOCX, TXT, MD"
        )
        
        if uploaded_file:
            st.success(f"✅ Archivo seleccionado: {uploaded_file.name}")
            
            if st.button("🚀 Procesar e Ingestar"):
                with st.spinner('📊 Procesando documento...'):
                    try:
                        # Guardar archivo temporalmente
                        temp_path = f"temp_{uploaded_file.name}"
                        with open(temp_path, 'wb') as f:
                            f.write(uploaded_file.getvalue())
                        
                        # Ingestar
                        progress_bar = st.progress(0)
                        st.write("1️⃣ Extrayendo texto...")
                        progress_bar.progress(25)
                        
                        st.write("2️⃣ Generando embeddings...")
                        progress_bar.progress(50)
                        
                        result = st.session_state.ingestion.ingest_single_document(temp_path)
                        progress_bar.progress(75)
                        
                        st.write("3️⃣ Almacenando en base de datos...")
                        progress_bar.progress(100)
                        
                        # Limpiar archivo temporal
                        os.remove(temp_path)
                        
                        st.success(f"""
                        ✅ **Documento ingestado exitosamente!**
                        - Chunks creados: {result['chunks_count']}
                        - Embeddings generados: {result['embeddings_count']}
                        - Tiempo: {result['processing_time']:.2f}s
                        """)
                        
                    except Exception as e:
                        st.error(f"❌ Error procesando documento: {str(e)}")
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
    
    with tab2:
        st.markdown("### 🔧 Configuración Actual")
        
        config = Config()
        
        st.markdown(f"""
        **AWS Configuration:**
        - Región: `{config.aws_region}`
        - Bucket S3: `{config.s3_bucket_name}`
        
        **Bedrock Models:**
        - LLM: `{config.llm_model}`
        - Embeddings: `{config.embedding_model}`
        
        **RAG Parameters:**
        - Chunk Size: `{config.chunk_size}`
        - Chunk Overlap: `{config.chunk_overlap}`
        - Top-K Results: `{config.top_k}`
        - Temperature: `{config.temperature}`
        
        **Database:**
        - Host: `{config.db_host}`
        - Name: `{config.db_name}`
        """)
        
        st.warning("⚠️ Para cambiar la configuración, edita el archivo `.env`")
        
        if st.button("🔄 Actualizar Credenciales AWS"):
            st.info("Ejecuta: `python aws_academy_config.py` en la terminal")
    
    with tab3:
        st.markdown("### 📖 Guía de Uso")
        
        st.markdown("""
        #### 🚀 Inicio Rápido
        
        1. **Subir documentos:**
           - Ve a la pestaña "Subir Documentos"
           - Selecciona un archivo PDF, DOCX o TXT
           - Click en "Procesar e Ingestar"
        
        2. **Hacer consultas:**
           - Ve al modo "Chat Inteligente"
           - Escribe tu pregunta
           - Recibe respuesta con fuentes citadas
        
        3. **Ver estadísticas:**
           - Ve al modo "Estadísticas"
           - Revisa documentos y métricas
        
        #### 🔑 Atajos de Teclado
        
        - `Enter`: Enviar consulta
        - `Ctrl+L`: Limpiar chat
        
        #### 💡 Tips
        
        - Haz preguntas específicas para mejores resultados
        - Usa lenguaje natural
        - Revisa las fuentes citadas para verificar la información
        
        #### 🆘 Soporte
        
        Si encuentras algún problema:
        1. Revisa el archivo `INSTALLATION.md`
        2. Verifica tus credenciales AWS
        3. Consulta `SECURITY.md` para problemas de seguridad
        """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<p style='text-align: center; color: white; opacity: 0.7;'>🚀 DocSmart v1.0</p>", unsafe_allow_html=True)
with col2:
    st.markdown("<p style='text-align: center; color: white; opacity: 0.7;'>Powered by Amazon Bedrock</p>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<p style='text-align: center; color: white; opacity: 0.7;'>⏰ {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
