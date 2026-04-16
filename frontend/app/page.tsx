import Link from 'next/link';
export default function Home() {
  return (
    <div className="landing">
      {/* Navbar */}
      <nav className="navbar" id="navbar">
        <div className="navbar-brand">
          <div className="navbar-logo">SA</div>
          <div>
            <div className="navbar-title">Sales Assistant</div>
            <div className="navbar-subtitle">Powered by AI</div>
          </div>
        </div>
        <div className="navbar-actions">
           <Link href="/architecture" className="btn btn-secondary">Arquitectura</Link>
          <a href="/dashboard" className="btn btn-secondary" id="nav-dashboard">
            Dashboard
          </a>
          <a href="/upload" className="btn btn-primary" id="nav-upload">
            Subir Excel
          </a>
        </div>
      </nav>

      {/* Hero */}
      <section className="hero" id="hero">
        <div className="hero-badge">
          <span className="hero-badge-dot"></span>
          Plataforma de Análisis Inteligente
        </div>
        <h1>
          Transforma tus ventas
          <br />
          con <span className="gradient-text">Inteligencia Artificial</span>
        </h1>
        <p className="hero-description">
          Sube tu archivo Excel y obtén dashboards automáticos, haz preguntas en
          lenguaje natural y genera pronósticos de ventas. Todo potenciado por
          Gemini 1.5 Flash y Prophet.
        </p>
        <div className="hero-actions">
          <a href="/upload" className="btn btn-primary btn-lg" id="cta-upload">
            📊 Comenzar Análisis
          </a>
          <a href="#features" className="btn btn-secondary btn-lg" id="cta-features">
            Explorar Funciones
          </a>
        </div>
      </section>

      {/* Features */}
      <section className="features-section" id="features">
        <p className="section-label">Funcionalidades</p>
        <h2 className="section-title">Todo lo que necesitas</h2>
        <p className="section-subtitle">
          Un ecosistema completo para analizar, consultar y predecir tus ventas.
        </p>

        <div className="features-grid">
          <div className="feature-card" id="feature-upload">
            <div className="feature-icon">📁</div>
            <h3>Carga Inteligente</h3>
            <p>
              Sube tu Excel y el sistema limpia, normaliza y almacena tus datos
              automáticamente en DuckDB para consultas ultrarrápidas.
            </p>
          </div>

          <div className="feature-card" id="feature-dashboard">
            <div className="feature-icon">📈</div>
            <h3>Dashboard Automático</h3>
            <p>
              Visualiza ventas totales, ticket promedio, tendencias mensuales,
              top productos y clientes con gráficos interactivos.
            </p>
          </div>

          <div className="feature-card" id="feature-ai">
            <div className="feature-icon">🤖</div>
            <h3>Preguntas con IA</h3>
            <p>
              Pregunta en español sobre tus datos. Gemini 1.5 Flash genera SQL seguro,
              ejecuta la consulta y te responde en lenguaje natural.
            </p>
          </div>

          <div className="feature-card" id="feature-forecast">
            <div className="feature-icon">🔮</div>
            <h3>Forecast con Prophet</h3>
            <p>
              Genera pronósticos de ventas para los próximos 6 meses con bandas
              de confianza usando Facebook Prophet.
            </p>
          </div>

          <div className="feature-card" id="feature-docker">
            <div className="feature-icon">🐳</div>
            <h3>Dockerizado</h3>
            <p>
              Frontend y backend completamente dockerizados con CI/CD en GitHub
              Actions. Listo para deploy en AWS.
            </p>
          </div>

          <div className="feature-card" id="feature-security">
            <div className="feature-icon">🛡️</div>
            <h3>Seguridad Integrada</h3>
            <p>
              Validación de SQL inyectado, solo consultas SELECT permitidas.
              Sanitización de datos y control de archivos.
            </p>
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="stack-section" id="stack">
        <p className="section-label">Tech Stack</p>
        <h2 className="section-title">Construido con lo Mejor</h2>
        <p className="section-subtitle">
          Stack moderno de producción, listo para escalar.
        </p>

        <div className="stack-grid">
          <span className="stack-chip">⚡ Next.js</span>
          <span className="stack-chip">🐍 FastAPI</span>
          <span className="stack-chip">🐼 Pandas</span>
          <span className="stack-chip">🦆 DuckDB</span>
          <span className="stack-chip">🧠 Gemini 1.5 Flash</span>
          <span className="stack-chip">📊 Prophet</span>
          <span className="stack-chip">🐳 Docker</span>
          <span className="stack-chip">⚙️ GitHub Actions</span>
          <span className="stack-chip">☁️ AWS Ready</span>
          <span className="stack-chip">📘 TypeScript</span>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer" id="footer">
        <p>
          AI Sales Assistant &copy; {new Date().getFullYear()} &mdash; Portfolio
          Project &mdash; Built with Next.js + FastAPI + Gemini 1.5 Flash
        </p>
      </footer>
    </div>
  );
}
