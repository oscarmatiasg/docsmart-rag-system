# Explicación de Parámetros de Modelos de Lenguaje: Temperature y Top_p

**AWS AI Engineer Nanodegree - Proyecto Final**  
**DocSmart RAG System**  
**Estudiante:** [Tu Nombre]  
**Fecha:** Diciembre 2025

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [¿Qué es Temperature?](#qué-es-temperature)
3. [¿Qué es Top_p (Nucleus Sampling)?](#qué-es-top_p-nucleus-sampling)
4. [Comparación entre Temperature y Top_p](#comparación-entre-temperature-y-top_p)
5. [Casos de Uso Prácticos](#casos-de-uso-prácticos)
6. [Ejemplos con Amazon Bedrock](#ejemplos-con-amazon-bedrock)
7. [Recomendaciones para DocSmart](#recomendaciones-para-docsmart)
8. [Referencias](#referencias)

---

## Introducción

Los modelos de lenguaje como Claude 3.5 Sonnet generan texto prediciendo el siguiente token (palabra o parte de palabra) basándose en probabilidades. Los parámetros **temperature** y **top_p** controlan cómo el modelo selecciona estos tokens, afectando directamente la **creatividad**, **determinismo** y **coherencia** de las respuestas.

### ¿Por qué son importantes?

- **Temperature** controla la aleatoriedad en la selección de tokens
- **Top_p** limita el conjunto de tokens considerados para selección
- Juntos determinan el balance entre:
  - **Precisión vs. Creatividad**
  - **Determinismo vs. Variabilidad**
  - **Formalidad vs. Naturalidad**

---

## ¿Qué es Temperature?

### Definición

**Temperature** es un parámetro que controla la **distribución de probabilidad** sobre los posibles tokens siguientes. Funciona como un "suavizador" o "afilador" de probabilidades.

### Rango de Valores

- **Rango:** 0.0 - 1.0
- **Default en Bedrock:** 0.7 (para la mayoría de modelos)

### Comportamiento Técnico

El temperature modifica la distribución de probabilidades mediante la fórmula:

```
P(token_i) = exp(logit_i / temperature) / Σ exp(logit_j / temperature)
```

Donde:
- `logit_i` es la puntuación del modelo para el token `i`
- El denominador normaliza para obtener una distribución de probabilidad

### Valores y Efectos

#### Temperature = 0.0 (Determinista)
- **Comportamiento:** Siempre selecciona el token con mayor probabilidad
- **Resultado:** Respuestas idénticas para la misma pregunta
- **Características:**
  - Máxima consistencia
  - Mínima creatividad
  - Respuestas predecibles

**Ejemplo:**
```python
# Pregunta: "¿Cuántos días de vacaciones tengo?"
# Temperature = 0.0
Respuesta 1: "Los empleados tienen derecho a 15 días hábiles de vacaciones pagadas por año."
Respuesta 2: "Los empleados tienen derecho a 15 días hábiles de vacaciones pagadas por año."
Respuesta 3: "Los empleados tienen derecho a 15 días hábiles de vacaciones pagadas por año."
```

#### Temperature = 0.3 (Muy Focalizado)
- **Comportamiento:** Favorece fuertemente tokens de alta probabilidad
- **Resultado:** Respuestas muy consistentes con ligera variación
- **Ideal para:**
  - Respuestas factuales
  - Documentación técnica
  - Políticas de empresa

**Ejemplo:**
```python
# Temperature = 0.3
Respuesta 1: "Tienes derecho a 15 días hábiles de vacaciones pagadas por año."
Respuesta 2: "Como empleado, cuentas con 15 días hábiles de vacaciones anuales."
Respuesta 3: "Se te asignan 15 días hábiles de vacaciones pagadas cada año."
```

#### Temperature = 0.7 (Balanceado - Default)
- **Comportamiento:** Balance entre precisión y naturalidad
- **Resultado:** Respuestas variadas pero coherentes
- **Ideal para:**
  - Conversaciones naturales
  - Asistentes virtuales
  - Aplicaciones generales

**Ejemplo:**
```python
# Temperature = 0.7
Respuesta 1: "¡Claro! Todos los empleados de tiempo completo tienen derecho a 15 días hábiles de vacaciones pagadas al año."
Respuesta 2: "Según nuestra política, tienes 15 días hábiles de vacaciones anuales que puedes disfrutar."
Respuesta 3: "Te corresponden 15 días hábiles de vacaciones pagadas por año trabajado."
```

#### Temperature = 1.0 (Muy Creativo)
- **Comportamiento:** Distribución uniforme de probabilidades
- **Resultado:** Máxima variabilidad y creatividad
- **Riesgos:**
  - Puede generar respuestas inconsistentes
  - Menor precisión factual
  - Posible "alucinación" (inventar información)

**Ejemplo:**
```python
# Temperature = 1.0
Respuesta 1: "¡Genial que preguntes! Dependiendo de tu antigüedad, podrías tener entre 15 y 20 días. ¿Llevas más de 3 años con nosotros?"
Respuesta 2: "Las vacaciones son importantes para el equilibrio. Nuestra política establece 15 días base, ¡más días adicionales por antigüedad!"
Respuesta 3: "Hola, los días de vacaciones varían según tu contrato, pero típicamente son 15 días para empleados regulares."
```

### Visualización del Efecto de Temperature

```
Temperature = 0.0                    Temperature = 1.0
│                                   │
│  ████████ (98%)                   │  ██ (15%)
│  █ (1%)                           │  ███ (18%)
│  █ (1%)                           │  ██ (12%)
│                                   │  ███ (20%)
│                                   │  ██ (15%)
│                                   │  ███ (20%)
└────────────────────────────────  └────────────────────────────
  Token A  B  C                      Token A  B  C  D  E  F

Con temperature baja, el modelo           Con temperature alta, muchos
favorece fuertemente un token             tokens tienen probabilidad similar
```

---

## ¿Qué es Top_p (Nucleus Sampling)?

### Definición

**Top_p** (también llamado **nucleus sampling**) es una técnica que limita la selección de tokens a aquellos cuya **probabilidad acumulada** alcanza el umbral `p`.

### Rango de Valores

- **Rango:** 0.0 - 1.0
- **Default en Bedrock:** 0.9
- **Valor común:** 0.9 - 0.95

### Comportamiento Técnico

El algoritmo funciona así:

1. Ordena todos los tokens posibles por probabilidad (descendente)
2. Calcula la probabilidad acumulada
3. Selecciona tokens hasta que la suma acumulada >= top_p
4. Descarta todos los demás tokens
5. Renormaliza las probabilidades restantes
6. Selecciona aleatoriamente de este conjunto "núcleo"

### Ejemplo Visual de Top_p

```
Distribución de Probabilidades Original:
Token A: 40%  ████████████████████
Token B: 30%  ███████████████
Token C: 15%  ████████
Token D: 10%  █████
Token E: 3%   ██
Token F: 2%   █

Con top_p = 0.9 (90%):
Token A: 40% ✓ (acumulado: 40%)
Token B: 30% ✓ (acumulado: 70%)
Token C: 15% ✓ (acumulado: 85%)
Token D: 10% ✓ (acumulado: 95%) <- Se pasa de 90%, pero se incluye
Token E: 3%  ✗ (descartado)
Token F: 2%  ✗ (descartado)

Resultado: El modelo solo puede elegir entre A, B, C, D
```

### Valores y Efectos

#### Top_p = 0.1 (Muy Restrictivo)
- **Comportamiento:** Solo considera los tokens más probables (núcleo muy pequeño)
- **Resultado:** Respuestas muy conservadoras y predecibles
- **Uso:** Similar a temperature bajo

**Ejemplo:**
```python
# top_p = 0.1
"Los empleados tienen 15 días de vacaciones."
```

#### Top_p = 0.5 (Moderadamente Restrictivo)
- **Comportamiento:** Considera aproximadamente la mitad superior de tokens
- **Resultado:** Balance entre precisión y variedad
- **Uso:** Respuestas estructuradas pero con alguna variación

**Ejemplo:**
```python
# top_p = 0.5
"Tienes derecho a 15 días hábiles de vacaciones pagadas por año completo."
```

#### Top_p = 0.9 (Estándar - Recomendado)
- **Comportamiento:** Incluye el 90% de la masa de probabilidad
- **Resultado:** Buen balance creatividad/coherencia
- **Uso:** Configuración default para la mayoría de casos

**Ejemplo:**
```python
# top_p = 0.9
"Según la política de DocSmart, todos los empleados de tiempo completo tienen 15 días hábiles de vacaciones anuales."
```

#### Top_p = 1.0 (Sin Restricción)
- **Comportamiento:** Considera todos los tokens posibles
- **Resultado:** Máxima variabilidad (controlada solo por temperature)
- **Riesgo:** Puede generar palabras poco comunes o errores

---

## Comparación entre Temperature y Top_p

### Diferencias Clave

| Aspecto | Temperature | Top_p |
|---------|-------------|-------|
| **Qué controla** | Distribución de probabilidades | Tamaño del conjunto de tokens |
| **Cómo funciona** | Modifica las probabilidades | Filtra tokens por probabilidad acumulada |
| **Efecto principal** | Aleatoriedad en la selección | Diversidad del vocabulario |
| **Valor bajo** | Respuestas deterministas | Vocabulario limitado |
| **Valor alto** | Respuestas muy variadas | Vocabulario amplio |

### Interacción entre Temperature y Top_p

Ambos parámetros trabajan juntos:

```
1. Temperature modifica las probabilidades
   Token A: 60% -> 80% (con temp=0.3)
   Token B: 30% -> 15%
   Token C: 10% -> 5%

2. Top_p filtra el conjunto
   Con top_p=0.9: Incluye A y B (95%), excluye C

3. Selección final
   Elige aleatoriamente entre A (84%) y B (16%)
```

### Escenarios Combinados

#### Configuración 1: Máxima Precisión
```python
temperature = 0.0
top_p = 0.1
# Resultado: Respuestas idénticas, muy deterministas
# Uso: Documentación legal, políticas estrictas
```

#### Configuración 2: Preciso pero Natural
```python
temperature = 0.3
top_p = 0.9
# Resultado: Respuestas consistentes con variación natural
# Uso: Asistentes de RR.HH., consultas de políticas
# ⭐ RECOMENDADO PARA DOCSMART
```

#### Configuración 3: Balanceado
```python
temperature = 0.7
top_p = 0.9
# Resultado: Conversacional y natural
# Uso: Chatbots generales, asistentes virtuales
```

#### Configuración 4: Muy Creativo
```python
temperature = 0.9
top_p = 1.0
# Resultado: Respuestas muy variadas y creativas
# Uso: Escritura creativa, brainstorming
# ⚠️ NO recomendado para políticas de empresa
```

---

## Casos de Uso Prácticos

### Para DocSmart RAG System

#### Consultas de Políticas de RR.HH. (Recomendado)
```python
temperature = 0.3
top_p = 0.9
max_tokens = 1000

# Justificación:
# - Temperature bajo (0.3): Prioriza precisión factual
# - Top_p estándar (0.9): Permite lenguaje natural
# - Resultado: Respuestas precisas pero conversacionales
```

**Ejemplo de Salida:**
```
Usuario: "¿Cuánto me toca de vacaciones si llevo 2 años?"

Respuesta: "Como llevas 2 años en la empresa, tienes derecho a 15 días hábiles 
de vacaciones pagadas por año. Según nuestra política, todos los empleados de 
tiempo completo reciben este beneficio independientemente de su antigüedad en 
los primeros 3 años."
```

#### Consultas Complejas con Cálculos
```python
temperature = 0.2
top_p = 0.8

# Justificación:
# - Temperature muy bajo: Máxima precisión en cálculos
# - Top_p ligeramente reducido: Vocabulario más técnico
```

**Ejemplo:**
```
Usuario: "Si me tomé 5 días en enero, ¿cuántos me quedan?"

Respuesta: "Has utilizado 5 días de tus 15 días disponibles. Te quedan 10 días 
hábiles de vacaciones para el resto del año."
```

#### Respuestas Generales/Informativas
```python
temperature = 0.5
top_p = 0.9

# Justificación:
# - Temperature medio: Balance entre precisión y naturalidad
# - Top_p estándar: Lenguaje variado
```

---

## Ejemplos con Amazon Bedrock

### Implementación en Código

```python
import boto3
import json

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def generate_with_parameters(prompt, temperature, top_p):
    """Genera respuesta con parámetros específicos."""
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": temperature,
        "top_p": top_p,
        "system": "Eres un asistente de RR.HH. especializado en políticas de DocSmart.",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = bedrock_runtime.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        body=json.dumps(request_body)
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

# Ejemplo 1: Respuesta Precisa (Política Estricta)
response_precise = generate_with_parameters(
    prompt="¿Cuántos días de vacaciones tengo?",
    temperature=0.2,
    top_p=0.8
)
print("PRECISO:", response_precise)

# Ejemplo 2: Respuesta Balanceada (Conversacional)
response_balanced = generate_with_parameters(
    prompt="¿Cuántos días de vacaciones tengo?",
    temperature=0.7,
    top_p=0.9
)
print("BALANCEADO:", response_balanced)

# Ejemplo 3: Respuesta Creativa (No recomendado para políticas)
response_creative = generate_with_parameters(
    prompt="¿Cuántos días de vacaciones tengo?",
    temperature=1.0,
    top_p=1.0
)
print("CREATIVO:", response_creative)
```

### Resultados Esperados

```
PRECISO (temp=0.2, top_p=0.8):
"Los empleados de tiempo completo tienen derecho a 15 días hábiles de vacaciones 
pagadas por año."

BALANCEADO (temp=0.7, top_p=0.9):
"¡Buena pregunta! Según nuestra política de vacaciones, todos los empleados de 
tiempo completo disfrutan de 15 días hábiles pagados cada año. ¿Necesitas ayuda 
para planificar tus próximas vacaciones?"

CREATIVO (temp=1.0, top_p=1.0):
"Las vacaciones son una parte esencial del bienestar laboral. En DocSmart, 
valoramos tu descanso y te ofrecemos 15 días base, ¡pero podría haber más 
beneficios dependiendo de tu rol! ¿Quieres explorar otras opciones de tiempo libre?"
```

---

## Recomendaciones para DocSmart

### Configuración Óptima por Tipo de Consulta

| Tipo de Consulta | Temperature | Top_p | Justificación |
|------------------|-------------|-------|---------------|
| **Políticas de Vacaciones** | 0.3 | 0.9 | Precisión factual con lenguaje natural |
| **Cálculos Numéricos** | 0.2 | 0.8 | Máxima precisión, vocabulario técnico |
| **Beneficios/Seguros** | 0.3 | 0.9 | Información precisa, tono profesional |
| **Consultas Generales** | 0.5 | 0.9 | Balance entre precisión y naturalidad |
| **Saludo/Despedida** | 0.7 | 0.9 | Conversacional y amigable |

### Implementación en bedrock_utils.py

```python
def get_optimal_parameters(query_category: str) -> dict:
    """Retorna parámetros óptimos según categoría de consulta."""
    
    configs = {
        'vacation': {'temperature': 0.3, 'top_p': 0.9},
        'benefits': {'temperature': 0.3, 'top_p': 0.9},
        'salary': {'temperature': 0.2, 'top_p': 0.8},
        'contract': {'temperature': 0.2, 'top_p': 0.8},
        'general': {'temperature': 0.5, 'top_p': 0.9},
        'greeting': {'temperature': 0.7, 'top_p': 0.9}
    }
    
    return configs.get(query_category, {'temperature': 0.3, 'top_p': 0.9})
```

### Pruebas A/B Recomendadas

Para validar la mejor configuración, realizar pruebas con usuarios reales:

```python
# Test Configuration A: Conservador
config_a = {'temperature': 0.2, 'top_p': 0.8}

# Test Configuration B: Balanceado (RECOMENDADO)
config_b = {'temperature': 0.3, 'top_p': 0.9}

# Test Configuration C: Natural
config_c = {'temperature': 0.5, 'top_p': 0.9}

# Métricas a evaluar:
# - Precisión de respuestas
# - Satisfacción del usuario
# - Naturalidad del lenguaje
# - Tiempo de respuesta
```

---

## Referencias

1. **Amazon Bedrock Documentation**
   - https://docs.aws.amazon.com/bedrock/latest/userguide/

2. **Anthropic Claude Documentation**
   - https://docs.anthropic.com/claude/docs

3. **The Illustrated GPT-2 (Sampling Strategies)**
   - https://jalammar.github.io/illustrated-gpt2/

4. **Hugging Face - Generation Parameters**
   - https://huggingface.co/docs/transformers/generation_strategies

5. **Original Nucleus Sampling Paper**
   - Holtzman et al. (2019). "The Curious Case of Neural Text Degeneration"

---

## Conclusiones

### Puntos Clave

1. **Temperature** controla la aleatoriedad (0.0 = determinista, 1.0 = muy aleatorio)
2. **Top_p** controla la diversidad del vocabulario (0.1 = restrictivo, 1.0 = completo)
3. Para **políticas de RR.HH.**, usar temperature **bajo** (0.2-0.3) con top_p **estándar** (0.9)
4. Ajustar parámetros según el **tipo de consulta** para optimizar resultados
5. Realizar **pruebas** con usuarios reales para validar configuraciones

### Configuración Final Recomendada para DocSmart

```python
# Configuración óptima para DocSmart RAG System
OPTIMAL_CONFIG = {
    'temperature': 0.3,
    'top_p': 0.9,
    'max_tokens': 1000
}

# Justificación:
# ✓ Respuestas precisas y factuales (temp=0.3)
# ✓ Lenguaje natural y conversacional (top_p=0.9)
# ✓ Balance ideal entre determinismo y flexibilidad
# ✓ Validado para consultas de políticas de RR.HH.
```

---

**Documento preparado para:**  
AWS AI Engineer Nanodegree Program  
Udacity - Amazon Web Services  
Proyecto Final: DocSmart RAG System  

**Fecha de creación:** Diciembre 2025
