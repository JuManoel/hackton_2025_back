# 📊 API de Métricas - Documentación

Esta API analiza la calidad de conversaciones usando IA para generar métricas de satisfacción y precisión de cada mensaje en tiempo real.

## 📋 Endpoint Disponible

### 📊 Generar Análisis de Métricas
**GET** `/api/metricas/{chat_id}`

Analiza todos los mensajes de un chat y genera métricas de calidad usando Mistral AI.

#### Parámetros
- `chat_id` (string): ID único del chat a analizar

#### Response
```json
{
  "satisfacion": [85.0, 90.0, 78.5],
  "precision": [92.0, 88.0, 85.5, 90.0, 95.0, 87.0],
  "satisfacion_promedio": 84.5,
  "precision_promedio": 89.6
}
```

#### Ejemplo cURL
```bash
curl -X GET "http://localhost:8000/api/metricas/67a1b2c3d4e5f6789012345"
```

---

## 🧠 Proceso de Análisis

### 1. Extracción de Mensajes
El sistema:
- 📥 **Recupera** todos los mensajes del chat especificado
- 🔍 **Valida** que el chat existe en la base de datos
- 📝 **Organiza** los mensajes por orden cronológico

### 2. Análisis con IA
Para cada mensaje:
- 🤖 **Envía** el contenido a **Mistral AI**
- 📊 **Solicita** análisis de satisfacción y precisión
- 🔄 **Procesa** la respuesta usando expresiones regulares
- 💾 **Extrae** valores numéricos de calidad

### 3. Cálculo de Métricas
- 📈 **Satisfacción por mensaje**: Qué tan satisfactoria es cada respuesta
- 🎯 **Precisión por mensaje**: Qué tan precisa y correcta es la información
- 📊 **Promedios generales**: Valores promedio de toda la conversación
- 🔢 **Estadísticas**: Máximos, mínimos y distribución

---

## 📈 Tipos de Métricas

### Satisfacción (0-100%)
Mide qué tan satisfactoria es la respuesta para el usuario:
- **90-100%**: Excelente - Respuesta muy satisfactoria
- **80-89%**: Buena - Respuesta satisfactoria
- **70-79%**: Regular - Respuesta aceptable
- **60-69%**: Deficiente - Respuesta poco satisfactoria
- **0-59%**: Mala - Respuesta insatisfactoria

### Precisión (0-100%)
Mide qué tan precisa y correcta es la información:
- **90-100%**: Excelente - Información muy precisa
- **80-89%**: Buena - Información precisa
- **70-79%**: Regular - Información mayormente correcta
- **60-69%**: Deficiente - Información parcialmente correcta
- **0-59%**: Mala - Información imprecisa

---

## 🎨 Dashboard Visual

### Interfaz Web Integrada
La interfaz web (`mix.html`) incluye un dashboard completo:

#### 📊 Métricas Principales
- **Satisfacción Promedio**: Con emoji 😊 y color azul
- **Precisión Promedio**: Con emoji 🎯 y color verde

#### 📈 Gráficos de Barras
- **Satisfacción por Mensaje**: Barras azules con gradiente
- **Precisión por Mensaje**: Barras verdes con gradiente
- **Valores dentro de las barras**: Porcentajes visibles
- **Animaciones suaves**: Transiciones de 500ms

#### 📋 Estadísticas Detalladas
- **Total de Mensajes**: Conteo completo
- **Máxima Satisfacción**: Mejor valor encontrado
- **Máxima Precisión**: Mejor valor encontrado
- **ID del Chat**: Identificador de la conversación

---

## 🔧 Implementación Técnica

### Procesamiento de Respuestas IA
```python
# Extracción con expresiones regulares
pattern = r'\{[^{}]*\}'
matches = re.findall(pattern, response)

for match in matches:
    try:
        dict_data = json.loads(match)
        if "satisfacion" in dict_data:
            satisfacion_list.append(dict_data["satisfacion"])
        if "precision" in dict_data:
            precision_list.append(dict_data["precision"])
    except json.JSONDecodeError:
        # Fallback con eval para casos edge
        dict_data = eval(match)
```

### Cálculo de Promedios
```python
satisfacion_promedio = sum(satisfacion_list) / len(satisfacion_list) if satisfacion_list else 0
precision_promedio = sum(precision_list) / len(precision_list) if precision_list else 0
```

### Frontend Integration
```javascript
// Llamada a la API
const response = await fetch(`/api/metricas/${currentChatId}`);
const data = await response.json();

// Mostrar en dashboard
displayMetrics(data);
```

---

## 🚨 Manejo de Errores

### Chat No Encontrado
```json
{
  "success": false,
  "error": "Chat no encontrado",
  "message": "El chat especificado no existe"
}
```

### Error de Procesamiento
```json
{
  "success": false,
  "error": "Error al obtener mensajes: Database connection failed",
  "message": "No se pudieron obtener los mensajes"
}
```

### Chat Vacío
```json
{
  "satisfacion": [],
  "precision": [],
  "satisfacion_promedio": 0,
  "precision_promedio": 0
}
```

---

## 💡 Casos de Uso

### 1. Análisis de Calidad en Tiempo Real
```javascript
// Después de una conversación
const metrics = await fetch(`/api/metricas/${chatId}`);
const data = await metrics.json();

console.log(`Satisfacción promedio: ${data.satisfacion_promedio}%`);
console.log(`Precisión promedio: ${data.precision_promedio}%`);
```

### 2. Monitoreo de Performance
```bash
# Análisis de múltiples chats
for chat_id in chat_ids; do
  curl -X GET "http://localhost:8000/api/metricas/$chat_id"
done
```

### 3. Mejora Continua
- 📊 **Identificar** conversaciones con baja satisfacción
- 🔍 **Analizar** patrones en mensajes con baja precisión
- 📈 **Optimizar** prompts del sistema basado en métricas
- 🎯 **Mejorar** respuestas futuras

---

## 🎮 Uso desde la Interfaz Web

### Acceso al Dashboard
1. 🌐 **Abrir** `http://localhost:8000/html/mix.html`
2. 💬 **Mantener** conversación con el asistente
3. 📊 **Hacer clic** en "Generar Métricas"
4. 👀 **Ver** dashboard completo con gráficos

### Características del Dashboard
- ⚡ **Carga en tiempo real** con indicador de progreso
- 🎨 **Diseño moderno** con TailwindCSS
- 📱 **Responsive** para móvil y desktop
- 🔄 **Actualización dinámica** sin recargar página
- ❌ **Manejo de errores** con mensajes claros

---

## 📊 Ejemplos de Datos

### Conversación de Alta Calidad
```json
{
  "satisfacion": [95.0, 92.0, 88.0, 90.0],
  "precision": [98.0, 95.0, 92.0, 94.0, 89.0, 91.0],
  "satisfacion_promedio": 91.25,
  "precision_promedio": 93.17
}
```

### Conversación a Mejorar
```json
{
  "satisfacion": [65.0, 70.0, 58.0],
  "precision": [72.0, 68.0, 75.0, 63.0],
  "satisfacion_promedio": 64.33,
  "precision_promedio": 69.5
}
```

---

## 🔗 Enlaces Relacionados

- [💬 API de Chats](CHAT.md) - Para gestionar conversaciones
- [📨 API de Mensajes](MESSAGE.md) - Para enviar y recibir mensajes
- [🏠 README Principal](../README.md) - Guía de instalación y configuración