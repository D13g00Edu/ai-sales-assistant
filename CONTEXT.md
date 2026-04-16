# 🧠 AI Sales Assistant - Contexto del Proyecto

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
