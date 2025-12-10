# 💡 Ejemplos de Uso - DocSmart RAG System

## 📋 Índice
1. [Ejemplos por Industria](#ejemplos-por-industria)
2. [Scripts de Automatización](#scripts-de-automatización)
3. [Casos de Uso Avanzados](#casos-de-uso-avanzados)

---

## 🏢 Ejemplos por Industria

### 1. Recursos Humanos

#### Escenario: Onboarding de Nuevos Empleados

**Documentos a ingestar**:
```bash
python cli.py ingest -d "documentos/rrhh/" --category="RRHH"
```

Estructura de carpeta:
```
documentos/rrhh/
  ├── manual_empleado.pdf
  ├── politica_vacaciones.pdf
  ├── codigo_conducta.docx
  ├── beneficios_2024.pdf
  └── procedimientos_contratacion.pdf
```

**Consultas Típicas**:

```python
# Ejemplo 1: Política de Vacaciones
query = "¿Cuántos días de vacaciones tengo si llevo 3 años en la empresa?"

# Ejemplo 2: Beneficios
query = "¿Qué cobertura de salud incluye el plan médico?"

# Ejemplo 3: Procedimientos
query = "¿Cómo solicito un día de trabajo remoto?"
```

**Código Python**:
```python
from rag_system import RAGSystem
from vector_database import VectorDatabase

# Inicializar
rag = RAGSystem()
db = VectorDatabase()
db.connect()
rag.vector_db = db

# Consultar
response = rag.query(
    user_query="¿Cuántos días de vacaciones tengo si llevo 3 años en la empresa?",
    top_k=3
)

print("Respuesta:", response['answer'])
print("\nFuentes:")
for source in response['sources']:
    print(f"- {source['file_name']} (Similitud: {source['similarity']:.3f})")

db.close()
```

**Respuesta Esperada**:
```
Respuesta: Según la política de vacaciones de la empresa, los empleados 
con 3 años de antigüedad tienen derecho a 15 días hábiles de vacaciones 
anuales, más 3 días personales adicionales.

Fuentes:
- politica_vacaciones.pdf (Similitud: 0.892)
- manual_empleado.pdf (Similitud: 0.745)
```

---

### 2. Ventas y Comercial

#### Escenario: Sales Enablement

**Setup**:
```bash
mkdir -p documentos/ventas
# Agregar fichas técnicas, casos de éxito, FAQ

python cli.py ingest -d "documentos/ventas/" --category="Ventas"
```

**Consultas de Equipo de Ventas**:

```python
# Comparación de productos
queries = [
    "¿Cuáles son las diferencias clave entre el Plan Pro y Enterprise?",
    "¿Qué casos de éxito tenemos en el sector retail?",
    "¿Cuál es el ROI típico que logran nuestros clientes?",
    "¿Qué objeciones comunes mencionan sobre el precio y cómo responder?"
]

# Ejecutar múltiples consultas
for query in queries:
    response = rag.query(query, top_k=5)
    print(f"\nQ: {query}")
    print(f"A: {response['answer'][:200]}...")
```

**Script de Sales Assistant**:
```python
# sales_assistant.py
import streamlit as st
from rag_system import RAGSystem

def sales_assistant():
    st.title("🎯 Sales Assistant")
    
    # Categorías predefinidas
    categoria = st.selectbox(
        "Tipo de Consulta",
        ["Productos", "Casos de Éxito", "Pricing", "Competencia", "Objeciones"]
    )
    
    pregunta = st.text_input("Tu pregunta:")
    
    if st.button("Buscar"):
        # Agregar contexto según categoría
        system_role = f"""Eres un asistente de ventas experto. 
        Enfócate en información de {categoria}. 
        Proporciona respuestas accionables y cita casos específicos."""
        
        response = rag.query(
            user_query=pregunta,
            system_role=system_role,
            top_k=5
        )
        
        st.success(response['answer'])
        
        # Sugerencias de follow-up
        st.subheader("Preguntas Relacionadas")
        st.write("- ¿Necesitas casos de éxito específicos?")
        st.write("- ¿Quieres comparar con competidores?")

if __name__ == "__main__":
    sales_assistant()
```

---

### 3. Legal y Compliance

#### Escenario: Revisión de Contratos

**Documentos**:
```
documentos/legal/
  ├── contratos/
  │   ├── contrato_servicios_tipo_a.pdf
  │   ├── contrato_servicios_tipo_b.pdf
  │   └── nda_standard.pdf
  ├── regulaciones/
  │   ├── gdpr_compliance.pdf
  │   └── politica_privacidad.pdf
  └── precedentes/
      └── casos_disputas_2023.pdf
```

**Consultas Legales**:
```python
legal_queries = {
    "clausulas": "¿Qué cláusulas de indemnización tenemos en contratos tipo A?",
    "compliance": "¿Cumplimos con GDPR en el procesamiento de datos de clientes?",
    "precedentes": "¿Hemos tenido casos similares de disputa contractual?",
    "terminos": "¿Cuál es el periodo de notificación para cancelación en contratos B?"
}

for tipo, query in legal_queries.items():
    response = rag.query(query, top_k=7)  # Más contexto para legal
    
    print(f"\n{'='*80}")
    print(f"TIPO: {tipo.upper()}")
    print(f"{'='*80}")
    print(f"Consulta: {query}")
    print(f"\nRespuesta:\n{response['answer']}")
    print(f"\nDocumentos Citados:")
    for src in response['sources'][:3]:
        print(f"  - {src['file_name']}")
```

**Sistema de Alertas**:
```python
# legal_alerts.py
from datetime import datetime

def check_compliance_updates(rag, db):
    """Verifica actualizaciones en regulaciones."""
    
    queries_compliance = [
        "¿Hay nuevas regulaciones de privacidad de datos?",
        "¿Se han actualizado los términos de GDPR?",
        "¿Existen cambios en regulación financiera?"
    ]
    
    alerts = []
    
    for query in queries_compliance:
        response = rag.query(query)
        
        # Si encuentra documentos recientes
        for source in response['sources']:
            doc_date = source['metadata'].get('processed_at')
            if is_recent(doc_date, days=30):
                alerts.append({
                    'query': query,
                    'document': source['file_name'],
                    'date': doc_date
                })
    
    # Enviar notificación
    if alerts:
        send_compliance_alert(alerts)
    
    return alerts
```

---

### 4. Soporte Técnico

#### Escenario: Troubleshooting Assistant

**Base de Conocimiento**:
```
documentos/soporte/
  ├── manuales/
  │   ├── manual_instalacion.pdf
  │   ├── manual_usuario_avanzado.pdf
  │   └── guia_api.pdf
  ├── troubleshooting/
  │   ├── errores_comunes.md
  │   ├── soluciones_red.md
  │   └── faq_tecnico.md
  └── changelog/
      └── release_notes_2024.md
```

**Chatbot de Soporte**:
```python
# support_bot.py
import streamlit as st
from rag_system import RAGSystem

def technical_support_bot():
    st.title("🔧 Technical Support Assistant")
    
    # Historial de conversación
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Nivel de detalle
    detail_level = st.select_slider(
        "Nivel de Detalle",
        options=['Básico', 'Intermedio', 'Avanzado']
    )
    
    # Input del usuario
    if prompt := st.chat_input("Describe tu problema"):
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt
        })
        
        # Ajustar system role según nivel
        system_roles = {
            'Básico': "Explica en términos simples, paso a paso.",
            'Intermedio': "Proporciona detalles técnicos relevantes.",
            'Avanzado': "Incluye comandos específicos y troubleshooting avanzado."
        }
        
        # Consultar RAG
        response = rag.query(
            user_query=prompt,
            system_role=f"Eres un asistente técnico. {system_roles[detail_level]}",
            top_k=5
        )
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response['answer']
        })
        
        # Mostrar conversación
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Acciones rápidas
        st.subheader("Acciones Sugeridas")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Crear Ticket"):
                create_support_ticket(prompt, response['answer'])
        
        with col2:
            if st.button("📞 Escalar a Humano"):
                escalate_to_human(prompt)
        
        with col3:
            if st.button("✅ Problema Resuelto"):
                mark_resolved(prompt)

if __name__ == "__main__":
    technical_support_bot()
```

---

## 🤖 Scripts de Automatización

### 1. Ingesta Automática Programada

```python
# scheduled_ingestion.py
import schedule
import time
from ingestion_pipeline import IngestionPipeline
from datetime import datetime

def scheduled_ingestion():
    """Ingesta automática de documentos nuevos cada hora."""
    
    pipeline = IngestionPipeline()
    watch_folder = "documentos/incoming/"
    
    print(f"[{datetime.now()}] Iniciando ingesta programada...")
    
    try:
        summaries = pipeline.ingest_directory(
            watch_folder,
            upload_to_s3=True
        )
        
        print(f"✓ Ingested {len(summaries)} documentos")
        
        # Mover archivos procesados
        move_to_processed(watch_folder)
        
    except Exception as e:
        print(f"❌ Error en ingesta: {e}")
        send_alert(f"Ingestion failed: {e}")

# Programar cada hora
schedule.every(1).hours.do(scheduled_ingestion)

# Ejecutar indefinidamente
while True:
    schedule.run_pending()
    time.sleep(60)
```

### 2. Exportar Analytics a CSV

```python
# export_analytics.py
import pandas as pd
from vector_database import VectorDatabase
from datetime import datetime, timedelta

def export_query_analytics(days=30):
    """Exporta analytics de consultas a CSV."""
    
    db = VectorDatabase()
    db.connect()
    
    # Query para últimos N días
    query = f"""
    SELECT 
        DATE(created_at) as date,
        query_text,
        results_count,
        response_time_ms,
        user_id
    FROM query_logs
    WHERE created_at >= NOW() - INTERVAL '{days} days'
    ORDER BY created_at DESC;
    """
    
    db.cursor.execute(query)
    results = db.cursor.fetchall()
    
    # Convertir a DataFrame
    df = pd.DataFrame(results, columns=[
        'date', 'query', 'results', 'response_time', 'user'
    ])
    
    # Exportar
    filename = f"analytics_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"✓ Exported {len(df)} records to {filename}")
    
    # Estadísticas básicas
    print("\nEstadísticas:")
    print(f"- Total consultas: {len(df)}")
    print(f"- Tiempo promedio: {df['response_time'].mean():.2f}ms")
    print(f"- Usuarios únicos: {df['user'].nunique()}")
    
    db.close()
    return filename

if __name__ == "__main__":
    export_query_analytics(days=30)
```

### 3. Batch Query Processor

```python
# batch_query.py
import pandas as pd
from rag_system import RAGSystem
from tqdm import tqdm

def batch_process_queries(queries_file, output_file):
    """Procesa múltiples consultas desde archivo CSV."""
    
    # Leer consultas
    df = pd.read_csv(queries_file)
    
    # Inicializar RAG
    rag = RAGSystem()
    
    results = []
    
    # Procesar cada consulta
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        query = row['query']
        category = row.get('category', 'General')
        
        try:
            response = rag.query(query, top_k=5)
            
            results.append({
                'query': query,
                'category': category,
                'answer': response['answer'],
                'num_sources': len(response['sources']),
                'response_time': response['metadata']['total_time_ms'],
                'status': 'success'
            })
            
        except Exception as e:
            results.append({
                'query': query,
                'category': category,
                'answer': None,
                'num_sources': 0,
                'response_time': 0,
                'status': f'error: {str(e)}'
            })
    
    # Guardar resultados
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    
    print(f"✓ Processed {len(results)} queries")
    print(f"✓ Success rate: {(results_df['status'] == 'success').mean() * 100:.1f}%")
    print(f"✓ Results saved to {output_file}")

# Uso
# queries.csv:
# query,category
# "¿Qué es la política de vacaciones?",RRHH
# "¿Cómo instalar el software?",Soporte
# ...

if __name__ == "__main__":
    batch_process_queries('queries.csv', 'results.csv')
```

---

## 🎯 Casos de Uso Avanzados

### 1. Multi-Query con Agregación

```python
# multi_query_aggregation.py
from rag_system import RAGSystem

def multi_perspective_query(original_query, num_variations=3):
    """
    Genera múltiples variaciones de la consulta y agrega resultados.
    """
    
    rag = RAGSystem()
    
    # Generar variaciones de la consulta
    variations = [
        original_query,
        f"Explica {original_query}",
        f"Detalles sobre {original_query}",
        f"Información completa de {original_query}"
    ]
    
    all_sources = {}
    
    # Ejecutar cada variación
    for var in variations[:num_variations]:
        response = rag.query(var, top_k=5)
        
        # Agregar fuentes únicas
        for source in response['sources']:
            doc_id = source['id']
            if doc_id not in all_sources:
                all_sources[doc_id] = source
            else:
                # Actualizar similitud si es mayor
                if source['similarity'] > all_sources[doc_id]['similarity']:
                    all_sources[doc_id] = source
    
    # Ordenar por similitud
    aggregated_sources = sorted(
        all_sources.values(),
        key=lambda x: x['similarity'],
        reverse=True
    )
    
    # Generar respuesta final con contexto agregado
    final_response = rag.query(
        original_query,
        top_k=len(aggregated_sources[:10])
    )
    
    return final_response, aggregated_sources

# Uso
query = "política de vacaciones"
response, sources = multi_perspective_query(query)
print(response['answer'])
```

### 2. Query con Filtros de Metadata

```python
# filtered_query.py
from rag_system import RAGSystem
from vector_database import VectorDatabase

def query_with_filters(query, category=None, date_from=None):
    """
    Consulta con filtros de metadata.
    """
    
    rag = RAGSystem()
    embedding = rag.embedding_service.generate_embedding(query)
    
    # Construir query SQL con filtros
    sql = """
    SELECT 
        id, file_name, text, metadata,
        1 - (embedding <=> %s::vector) AS similarity
    FROM documents
    WHERE 1 - (embedding <=> %s::vector) > 0.3
    """
    
    params = [embedding, embedding]
    
    if category:
        sql += " AND metadata->>'category' = %s"
        params.append(category)
    
    if date_from:
        sql += " AND metadata->>'processed_at' >= %s"
        params.append(date_from)
    
    sql += " ORDER BY similarity DESC LIMIT 5;"
    
    # Ejecutar
    rag.vector_db.cursor.execute(sql, params)
    results = rag.vector_db.cursor.fetchall()
    
    # Formatear y generar respuesta
    # ...
    
    return results

# Uso
results = query_with_filters(
    "política de vacaciones",
    category="RRHH",
    date_from="2024-01-01"
)
```

### 3. Feedback Loop para Mejorar Resultados

```python
# feedback_system.py
from vector_database import VectorDatabase

def log_feedback(query, answer, helpful=True, user_id=None):
    """
    Registra feedback del usuario para mejorar sistema.
    """
    
    db = VectorDatabase()
    db.connect()
    
    # Crear tabla de feedback si no existe
    db.cursor.execute("""
    CREATE TABLE IF NOT EXISTS query_feedback (
        id SERIAL PRIMARY KEY,
        query_text TEXT,
        answer_text TEXT,
        helpful BOOLEAN,
        user_id VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Insertar feedback
    db.cursor.execute("""
    INSERT INTO query_feedback (query_text, answer_text, helpful, user_id)
    VALUES (%s, %s, %s, %s);
    """, (query, answer, helpful, user_id))
    
    db.connection.commit()
    db.close()

def analyze_feedback():
    """
    Analiza feedback para identificar áreas de mejora.
    """
    
    db = VectorDatabase()
    db.connect()
    
    # Consultas con bajo rating
    db.cursor.execute("""
    SELECT query_text, COUNT(*) as count
    FROM query_feedback
    WHERE helpful = FALSE
    GROUP BY query_text
    HAVING COUNT(*) > 3
    ORDER BY count DESC
    LIMIT 10;
    """)
    
    problematic_queries = db.cursor.fetchall()
    
    print("Consultas con problemas:")
    for query, count in problematic_queries:
        print(f"- {query}: {count} votos negativos")
    
    db.close()
    
    return problematic_queries

# Uso en Streamlit
if st.button("👍 Útil"):
    log_feedback(query, answer, helpful=True, user_id=user_id)
    st.success("¡Gracias por tu feedback!")

if st.button("👎 No útil"):
    log_feedback(query, answer, helpful=False, user_id=user_id)
    st.warning("Lamentamos que no haya sido útil. Mejoraremos.")
```

---

## 📊 Dashboard de Métricas

```python
# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from vector_database import VectorDatabase

def analytics_dashboard():
    st.title("📊 DocSmart Analytics Dashboard")
    
    db = VectorDatabase()
    db.connect()
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    # Total consultas
    db.cursor.execute("SELECT COUNT(*) FROM query_logs;")
    total_queries = db.cursor.fetchone()[0]
    col1.metric("Total Consultas", total_queries)
    
    # Tiempo promedio
    db.cursor.execute("SELECT AVG(response_time_ms) FROM query_logs;")
    avg_time = db.cursor.fetchone()[0]
    col2.metric("Tiempo Promedio", f"{avg_time:.0f}ms")
    
    # Documentos indexados
    db.cursor.execute("SELECT COUNT(*) FROM documents;")
    total_docs = db.cursor.fetchone()[0]
    col3.metric("Documentos", total_docs)
    
    # Usuarios únicos
    db.cursor.execute("SELECT COUNT(DISTINCT user_id) FROM query_logs WHERE user_id IS NOT NULL;")
    unique_users = db.cursor.fetchone()[0]
    col4.metric("Usuarios Únicos", unique_users)
    
    # Gráfico: Consultas por día
    df_queries = pd.read_sql("""
    SELECT DATE(created_at) as date, COUNT(*) as count
    FROM query_logs
    WHERE created_at >= NOW() - INTERVAL '30 days'
    GROUP BY DATE(created_at)
    ORDER BY date;
    """, db.connection)
    
    fig_queries = px.line(df_queries, x='date', y='count', title='Consultas por Día')
    st.plotly_chart(fig_queries)
    
    # Top consultas
    st.subheader("🔥 Consultas Más Frecuentes")
    df_top = pd.read_sql("""
    SELECT query_text, COUNT(*) as frequency
    FROM query_logs
    GROUP BY query_text
    ORDER BY frequency DESC
    LIMIT 10;
    """, db.connection)
    
    st.dataframe(df_top)
    
    db.close()

if __name__ == "__main__":
    analytics_dashboard()
```

---

## 🎓 Mejores Prácticas

### 1. Optimización de Consultas

```python
# Mala práctica ❌
query = "dame info"

# Buena práctica ✅
query = "¿Cuál es la política de vacaciones para empleados con más de 2 años de antigüedad?"

# Mejor práctica ⭐
query = """¿Cuál es la política específica de vacaciones para empleados con 
más de 2 años de antigüedad, incluyendo días adicionales y procedimiento de solicitud?"""
```

### 2. Gestión de Contexto

```python
# Para consultas complejas, dividir en sub-consultas
def complex_query_handler(main_query):
    # 1. Identificar sub-preguntas
    sub_queries = extract_sub_queries(main_query)
    
    # 2. Responder cada una
    sub_answers = []
    for sub_q in sub_queries:
        answer = rag.query(sub_q, top_k=3)
        sub_answers.append(answer)
    
    # 3. Agregar respuestas
    final_answer = aggregate_answers(main_query, sub_answers)
    
    return final_answer
```

### 3. Monitoreo de Calidad

```python
# quality_monitor.py
def monitor_answer_quality(response):
    """Valida calidad de respuestas."""
    
    checks = {
        'has_sources': len(response['sources']) > 0,
        'min_similarity': any(s['similarity'] > 0.7 for s in response['sources']),
        'answer_length': len(response['answer']) > 50,
        'response_time': response['metadata']['total_time_ms'] < 3000
    }
    
    if not all(checks.values()):
        log_quality_issue(response, checks)
    
    return checks
```

---

**Fin de Ejemplos** 🎉

Para más información, consulta:
- [README.md](README.md) - Documentación completa
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detalles técnicos
- [QUICKSTART.md](QUICKSTART.md) - Inicio rápido
