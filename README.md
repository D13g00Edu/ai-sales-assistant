# 🚀 AI Sales Assistant - Enterprise Data Platform

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
