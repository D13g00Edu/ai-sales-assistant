import os

context = '''# 🧠 AI Sales Assistant - Contexto del Proyecto

## ✅ Estado Actual: Arquitectura Modular (Finalizada)
El proyecto ha evolucionado de un prototipo lineal a un **Data Pipeline** completo implementando un *Monolito Modular* con Clean Architecture.

## 🏗️ Technical Stack
- **Frontend**: Next.js 16 (App Router), TailwindCSS, Recharts, Lucide Icons.
- **Backend API**: FastAPI, Pydantic, Python 3.12+.
- **Pipeline de Datos**: Pandas (Transformadores/Validadores), DuckDB (Almacenaje Analítico/OLAP), PyArrow (Codificación Parquet).
- **Inteligencia y ML**: Gemini 1.5 Flash (Generación NL a SQL), Prophet (Pronóstico Estadístico de Series Temporales).

## 🗃️ Arquitectura de Carpetas y Responsabilidades
El backend está segmentado explícitamente sin acoplamiento:
1. app/api/v1/: Rutas HTTP que manejan los contratos definidos en app/schemas/.
2. app/modules/pipelines/: Orquestador de ingesta de datos. Guarda el crudo, valida esquemas, normaliza con Pandas y lo convierte a capa procesada (Parquet).
3. app/modules/analytics/: Generación de queries estáticas a DuckDB (KPIs globales, rankings).
4. app/modules/ai_query/: El core del chat de IA con *Prompt Engineering* a Gemini y utilidades de seguridad (*Guardrails* para SQL).
5. app/modules/forecast/: Carga el agregado mensual en memoria, extrae estacionalidad y proyecta a Prophet.
6. app/infrastructure/: Interfaces externas agnósticas (Storage Físico, Cliente Gemini, Repositorio de DuckDB).

## 🚀 Puntos Focales para Futuro
- **Multi-tenant**: Actualmente la tabla ventas es compartida u operada globalmente. El esqueleto soporta pasar un dataset_id explícito para operar B2B multicuentas.
- **Nube**: Reemplazar LocalFileStorage de la capa de infraestructura por un manejador de S3 (AWS). La base no tendrá que ser re-escrita gracias a los patrones de diseño aplicados.
'''

readme = '''# 🚀 AI Sales Assistant - Enterprise Data Platform

**AI Sales Assistant** es una plataforma interactiva B2B diseñada para empresas que requieren procesar, visualizar e interrogar bases de datos comerciales sin requerir de un analista técnico de planta. 

Convierte archivos masivos .xlsx o .csv en un *Pipeline Analytics* instantáneo soportado por Machine Learning y Modelos Generativos.

---

## 🏗️ Arquitectura de la Plataforma (Modular Monolith)

A diferencia de aplicaciones típicas CRUD, esta aplicación funciona como un **Data Pipeline Analítico Multicapa**, separando de manera estricta la manipulación HTTP, la lógica de negocios del dominio de datos y la persistencia OLAP.

### El Flujo de Datos (Data Medallion Concept)
1. **[Capa Ingesta - Raw]**: Los archivos entran por el orquestador (/upload). Se les asigna un UUID y se almacenan íntegramente en su formato original antes de ser alterados, permitiendo auditoría o *replay* del pipeline.
2. **[Capa Validadora]**: Se comprueba dinámicamente la obligatoriedad de esquemas, tipo de campos numéricos (cantidades) e integridad de datos nulos para asegurar calidad.
3. **[Capa de Transformación (Pandas)]**: Estandariza estructuras de datos, limpia registros atípicos o *strings* mal formateados y mapea tipos de datos robustos, exportando un binario a disco en formato **Parquet** vía *Pyarrow*.
4. **[Capa Analítica (DuckDB)]**: Se elimina la penalidad de I/O montando una _view_ inmensamente eficiente sobre el Parquet local hacia el motor columnar integrado de DuckDB, capaz de consolidar agregaciones pesadas al instante.

### Capas Cognitivas (AI & ML Layers)
- **Natural Language Query Engine (Gemini 1.5):** Un servicio aislado dentro de la aplicación traduce peticiones de los usuarios en lenguaje natural (ej: "¿Cuál cliente nos hizo ganar más este trimestre?") a código puro DuckDB SQL. Tras pasar *Guardrails* de seguridad de comandos destructivos, el motor se autoarranca, extrae el extracto y provee un resumen contextual humano de los resultados al vuelo.
- **Time Series Forecasting (Prophet):** Un módulo autónomo que extrae en tiempo real la línea temporal de ventas agregadas para entrenar estadísticamente un modelo predictivo, devolviendo tendencia histórica y prediciendo visualmente seis meses a futuro con intervalos de confianza del 95%.

---

## 🛠️ Stack Tecnológico

*   **Frontend**: Next.js 16 (App Router) + Tailwind CSS + Lucide + Recharts. 
*   **Backend REST**: FastAPI + Pydantic (Validación tipada estricta).
*   **Database (OLAP)**: DuckDB.
*   **Data Processing**: Python 3.12, Pandas, Pyarrow.
*   **AI / Machine Learning**: Google Generative AI (Gemini Flash), Facebook Prophet.

---

## 📦 Inicialización en Local

**1. Clonar e Instalar Frontend**
`ash
cd frontend
npm install
npm run dev
`

**2. Configurar e Instalar Backend**
`ash
cd backend
python -m venv venv
.\venv\Scripts\activate  # O source venv/bin/activate en Linux/Mac
pip install -r requirements.txt
pip install pyarrow prophet google-generativeai

# Configura tu .env (En /backend)
GEMINI_API_KEY=tu_clave_aqui_de_google_ai_studio
`

**3. Lanzar API REST**
`ash
uvicorn app.main:app --port 8000 --reload
`
*(Luego, accede a http://localhost:3000)*
'''

with open('c:/Users/diego/Desktop/proyectos/Mlops/CONTEXT.md', 'w', encoding='utf8') as f: f.write(context.strip() + chr(10))
with open('c:/Users/diego/Desktop/proyectos/Mlops/README.md', 'w', encoding='utf8') as f: f.write(readme.strip() + chr(10))
print("Archivos escritos por Pyscript")
