import os
fp = r'c:/Users/diego/Desktop/proyectos/Mlops/frontend/app/architecture/page.tsx'
os.makedirs(os.path.dirname(fp), exist_ok=True)
with open(fp, 'w', encoding='utf8') as f:
    f.write('''"use client";
import Link from "next/link";
import { Database, FileSpreadsheet, Server, FileText, UploadCloud, CheckCircle, ShieldAlert, Cpu, BarChart3, MessageSquare, LineChart, LayoutDashboard, Activity, ArrowRight, Table, Fingerprint } from "lucide-react";

export default function ArchitecturePage() {
  return (
    <div className="landing" style={{ padding: "6rem 2rem 4rem", minHeight: "100vh", background: "var(--bg-main)" }}>
      <nav className="navbar">
        <Link href="/" className="navbar-brand"><div className="navbar-logo">SA</div><div className="navbar-title">Sales Assistant</div></Link>
        <div className="navbar-actions"><Link href="/dashboard" className="btn btn-secondary">Dashboard</Link></div>
      </nav>
      <header style={{ textAlign: "center", marginBottom: "4rem" }}>
        <h1 className="section-title">System Architecture</h1>
        <p style={{ color: "var(--text-secondary)", maxWidth: "800px", margin: "0 auto", fontSize: "1.1rem" }}>
          Layered Data Pipeline architecture with ingestion, validation, analytics, AI query engine and forecasting.
        </p>
      </header>
      <div style={{ display: "flex", gap: "1.5rem", overflowX: "auto", paddingBottom: "2rem", alignItems: "stretch", minWidth: "max-content", margin: "0 auto", maxWidth: "1600px" }}>
        
        <ArchColumn title="DATA SOURCES" icon={<Database size={18} />} color="#0ea5e9">
          <ArchCard icon={<FileSpreadsheet size={20} />} title="Excel Files" subtitle=".xlsx" />
          <ArchCard icon={<FileText size={20} />} title="CSV Files" subtitle=".csv" />
          <ArchCard icon={<UploadCloud size={20} />} title="Sales Data Upload" subtitle="Drag & Drop" />
        </ArchColumn><Arrow />

        <ArchColumn title="Ingestion Layer" icon={<Database size={18} />} color="#3b82f6">
          <ArchCard icon={<UploadCloud size={16} />} title="Upload API" />
          <ArchCard icon={<Server size={16} />} title="File Receiver" />
          <ArchCard icon={<Database size={16} />} title="Dataset Registration" />
          <ArchCard icon={<Fingerprint size={16} />} title="Version Control" />
        </ArchColumn><Arrow />

        <ArchColumn title="Validation & Quality" icon={<ShieldAlert size={18} />} color="#06b6d4">
          <ArchCard icon={<CheckCircle size={16} />} title="Schema Validation" />
          <ArchCard icon={<CheckCircle size={16} />} title="Required Columns Check" />
          <ArchCard icon={<ShieldAlert size={16} />} title="Null Detection" />
          <ArchCard icon={<ShieldAlert size={16} />} title="Duplicate Detection" />
          <ArchCard icon={<Activity size={16} />} title="Business Rules Engine" />
          <ArchCard icon={<FileText size={16} />} title="Quality Report" />
        </ArchColumn><Arrow />

        <ArchColumn title="ETL Processing" icon={<Cpu size={18} />} color="#8b5cf6">
          <ArchCard icon={<Activity size={16} />} title="Pandas Engine" />
          <ArchCard icon={<Table size={16} />} title="Column Standardization" />
          <ArchCard icon={<Table size={16} />} title="Date Parsing" />
          <ArchCard icon={<Table size={16} />} title="Currency Cleanup" />
          <ArchCard icon={<Database size={16} />} title="Dataset Normalization" />
          <ArchCard icon={<Database size={16} />} title="Curated Dataset Output" />
        </ArchColumn><Arrow />

        <ArchColumn title="Analytical Storage" icon={<Database size={18} />} color="#0ea5e9">
          <ArchCard icon={<Database size={16} />} title="/raw" />
          <ArchCard icon={<Database size={16} />} title="/validated" />
          <ArchCard icon={<Database size={16} />} title="/processed" />
          <div style={{ marginTop: "1rem", borderTop: "1px solid rgba(255,255,255,0.1)", paddingTop: "1rem" }}>
            <ArchCard icon={<Database size={20} color="#facc15" />} title="DuckDB Warehouse" subtitle="Parquet Files" />
          </div>
        </ArchColumn><Arrow />

        <div style={{ display: "flex", flexDirection: "column", gap: "1rem", flex: 1 }}>
          <ArchColumn title="Metrics & BI" icon={<BarChart3 size={18} />} color="#10b981" fullHeight={false}>
            <ul style={{ fontSize: "0.85rem", color: "var(--text-secondary)", paddingLeft: "1.5rem", margin: 0, lineHeight: "1.8" }}>
              <li>KPI Engine</li><li>Sales by Month</li><li>Top Products</li><li>Revenue Aggregations</li><li>Dashboard Queries</li>
            </ul>
          </ArchColumn>
          <ArchColumn title="NL Query Engine" icon={<MessageSquare size={18} />} color="#d946ef" fullHeight={false}>
             <ul style={{ fontSize: "0.85rem", color: "var(--text-secondary)", paddingLeft: "1.5rem", margin: 0, lineHeight: "1.8" }}>
              <li>LLM API</li><li>Prompt Builder</li><li>Text-to-SQL</li><li>SQL Guardrails</li><li>Query Executor</li><li>Natural Language Responses</li>
            </ul>
          </ArchColumn>
          <ArchColumn title="Forecasting Engine" icon={<LineChart size={18} />} color="#f59e0b" fullHeight={false}>
             <ul style={{ fontSize: "0.85rem", color: "var(--text-secondary)", paddingLeft: "1.5rem", margin: 0, lineHeight: "1.8" }}>
              <li>Prophet Model</li><li>Time Series Builder</li><li>Monthly Forecast</li><li>Confidence Intervals</li>
            </ul>
          </ArchColumn>
        </div><Arrow />

        <ArchColumn title="FastAPI Service Layer" icon={<Server size={18} />} color="#14b8a6">
          <ArchCard icon={<Server size={16} />} title="/datasets/upload" />
          <ArchCard icon={<Server size={16} />} title="/datasets/{id}/metrics" />
          <ArchCard icon={<Server size={16} />} title="/datasets/{id}/query" />
          <ArchCard icon={<Server size={16} />} title="/datasets/{id}/forecast" />
        </ArchColumn><Arrow />

        <ArchColumn title="Next.js Frontend" icon={<LayoutDashboard size={18} />} color="#f8fafc">
          <ArchCard icon={<UploadCloud size={16} />} title="Upload UI" />
          <ArchCard icon={<BarChart3 size={16} />} title="Dashboard" />
          <ArchCard icon={<MessageSquare size={16} />} title="AI Chat" />
          <ArchCard icon={<LineChart size={16} />} title="Forecast Charts" />
          <ArchCard icon={<Database size={16} />} title="Dataset History" />
        </ArchColumn>
      </div>
    </div>
  );
}

function ArchColumn({ title, icon, color, children, fullHeight = true }: any) {
  return (
    <div style={{ background: "rgba(15, 23, 42, 0.6)", border: "1px solid rgba(255,255,255,0.05)", borderRadius: "16px", padding: "1.5rem", minWidth: "220px", display: "flex", flexDirection: "column", boxShadow: "0 0 20px " + color + "10", height: fullHeight ? "100%" : "auto" }}>
      <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "1.5rem", color: color, fontWeight: 600, fontSize: "0.9rem", letterSpacing: "0.5px" }}>{icon}{title.toUpperCase()}</div>
      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem", flex: 1 }}>{children}</div>
    </div>
  );
}

function ArchCard({ icon, title, subtitle }: any) {
  return (
    <div style={{ background: "rgba(255, 255, 255, 0.03)", border: "1px solid rgba(255, 255, 255, 0.05)", borderRadius: "8px", padding: "0.75rem 1rem", display: "flex", alignItems: "center", gap: "12px" }}>
      <div style={{ color: "var(--text-secondary)" }}>{icon}</div>
      <div><div style={{ fontSize: "0.85rem", color: "#e2e8f0", fontWeight: 500 }}>{title}</div>{subtitle && <div style={{ fontSize: "0.7rem", color: "#94a3b8", marginTop: "2px" }}>{subtitle}</div>}</div>
    </div>
  );
}

function Arrow() {
  return <div style={{ display: "flex", alignItems: "center", color: "#3b82f6", opacity: 0.5, padding: "0 0.5rem" }}><ArrowRight size={24} /></div>;
}
''')
