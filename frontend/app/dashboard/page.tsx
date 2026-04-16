'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, AreaChart, Area 
} from 'recharts';
import { 
  TrendingUp, Users, Package, ShoppingCart, DollarSign, ArrowLeft, RefreshCw 
} from 'lucide-react';

export default function DashboardPage() {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState<any>(null);
  const [salesTrend, setSalesTrend] = useState<any[]>([]);
  const [topProducts, setTopProducts] = useState<any[]>([]);
  const [topClients, setTopClients] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      const [sumRes, trendRes, prodRes, cliRes] = await Promise.all([
        fetch(`${baseUrl}/dashboard/summary`),
        fetch(`${baseUrl}/dashboard/sales-by-month`),
        fetch(`${baseUrl}/dashboard/top-products`),
        fetch(`${baseUrl}/dashboard/top-clients`)
      ]);

      if (!sumRes.ok) throw new Error("Asegúrate de haber subido un archivo Excel en la fase anterior.");

      setSummary(await sumRes.json());
      setSalesTrend(await trendRes.json());
      setTopProducts(await prodRes.json());
      setTopClients(await cliRes.json());
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return (
    <div className="landing" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
      <div style={{ textAlign: 'center' }}>
        <RefreshCw size={48} color="var(--accent-primary)" style={{ animation: 'spin 2s linear infinite' }} />
        <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>Analizando datos con DuckDB...</p>
      </div>
      <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
    </div>
  );

  if (error) return (
    <div className="landing" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', padding: '2rem' }}>
      <div className="feature-card" style={{ textAlign: 'center', padding: '3rem', maxWidth: '500px' }}>
        <div className="feature-icon" style={{ margin: '0 auto 1.5rem', background: 'rgba(239, 68, 68, 0.1)' }}>⚠️</div>
        <h2 style={{ color: 'var(--error)', marginBottom: '1rem' }}>Sin Datos Disponibles</h2>
        <p style={{ marginBottom: '2rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
          No hemos podido encontrar datos de ventas. Para ver el dashboard, primero debes subir un archivo Excel válido.
        </p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <button onClick={fetchData} className="btn btn-secondary">Reintentar</button>
          <Link href="/upload" className="btn btn-primary">Subir Excel 📊</Link>
        </div>
      </div>
    </div>
  );

  return (
    <div className="landing" style={{ padding: '6rem 2rem 4rem' }}>
      <nav className="navbar">
        <Link href="/" className="navbar-brand">
          <div className="navbar-logo">SA</div>
          <div className="navbar-title">Sales Assistant</div>
        </Link>
        <div className="navbar-actions">
           <Link href="/architecture" className="btn btn-secondary">Arquitectura</Link>
          <Link href="/upload" className="btn btn-secondary">Subir Excel</Link>
          <Link href="/ask" className="btn btn-primary">Preguntar a la IA 🤖</Link>
        </div>
      </nav>

      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        <header style={{ marginBottom: '3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h1 className="section-title" style={{ textAlign: 'left', margin: 0, fontSize: '2.5rem' }}>Dashboard Ejecutivo</h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem' }}>Análisis granular impulsado por DuckDB.</p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Última Actualización</p>
            <p style={{ fontWeight: 600 }}>{new Date().toLocaleDateString()} {new Date().toLocaleTimeString()}</p>
          </div>
        </header>

        {/* KPI Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
          <KPICard title="Ventas Totales" value={`$${summary.total_ventas.toLocaleString()}`} icon={<DollarSign color="#10b981" />} />
          <KPICard title="Ticket Promedio" value={`$${summary.ticket_promedio.toLocaleString()}`} icon={<TrendingUp color="#3b82f6" />} />
          <KPICard title="Transacciones" value={summary.total_transacciones.toLocaleString()} icon={<ShoppingCart color="#6366f1" />} />
          <KPICard title="Clientes Únicos" value={summary.clientes_unicos.toLocaleString()} icon={<Users color="#8b5cf6" />} />
        </div>

        {/* Charts Section */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(600px, 1fr))', gap: '2rem', marginBottom: '2rem' }}>
          {/* Trend Chart */}
          <div className="feature-card" style={{ padding: '2rem' }}>
            <h3 style={{ marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
               <TrendingUp size={20} color="var(--accent-primary)" /> Tendencia de Ventas
            </h3>
            <div style={{ height: '350px', width: '100%' }}>
              <ResponsiveContainer>
                <AreaChart data={salesTrend}>
                  <defs>
                    <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="mes" stroke="var(--text-muted)" fontSize={11} axisLine={false} tickLine={false} />
                  <YAxis stroke="var(--text-muted)" fontSize={11} axisLine={false} tickLine={false} tickFormatter={(v) => `$${v}`} />
                  <Tooltip 
                    contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '12px', boxShadow: 'var(--shadow-lg)' }}
                  />
                  <Area type="monotone" dataKey="total" stroke="var(--accent-primary)" strokeWidth={3} fill="url(#chartGradient)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Products Chart */}
          <div className="feature-card" style={{ padding: '2rem' }}>
            <h3 style={{ marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Package size={20} color="var(--accent-secondary)" /> Top 10 Productos
            </h3>
            <div style={{ height: '350px', width: '100%' }}>
              <ResponsiveContainer>
                <BarChart data={topProducts} layout="vertical">
                  <XAxis type="number" hide />
                  <YAxis dataKey="nombre" type="category" stroke="var(--text-secondary)" fontSize={10} width={120} axisLine={false} tickLine={false} />
                  <Tooltip cursor={{ fill: 'rgba(255,255,255,0.02)' }} contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '12px' }} />
                  <Bar dataKey="total" fill="var(--accent-secondary)" radius={[0, 4, 4, 0]} barSize={15} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Clients & Next Steps */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(600px, 1fr))', gap: '2rem' }}>
          <div className="feature-card" style={{ padding: '2rem' }}>
            <h3 style={{ marginBottom: '2rem' }}>Distribución por Clientes</h3>
            <div style={{ height: '300px', width: '100%' }}>
              <ResponsiveContainer>
                <BarChart data={topClients}>
                  <XAxis dataKey="nombre" stroke="var(--text-muted)" fontSize={9} interval={0} angle={-30} textAnchor="end" height={60} />
                  <YAxis hide />
                  <Tooltip contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '12px' }} />
                  <Bar dataKey="total" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="feature-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', padding: '3rem', textAlign: 'center', background: 'linear-gradient(135deg, var(--bg-card) 0%, rgba(59, 130, 246, 0.05) 100%)' }}>
            <div style={{ background: 'var(--accent-gradient)', padding: '1rem', borderRadius: '50%', marginBottom: '1.5rem', boxShadow: 'var(--shadow-glow)' }}>
              <RefreshCw size={32} color="white" />
            </div>
            <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Potencia tu Análisis</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem', maxWidth: '400px' }}>
              ¿Quieres saber por qué bajaron las ventas? Pregúntale a nuestra IA o genera un pronóstico para adelantarte al mercado.
            </p>
            <div style={{ display: 'flex', gap: '1rem' }}>
              <Link href="/ask" className="btn btn-primary btn-lg">Preguntar 🦾</Link>
              <Link href="/forecast" className="btn btn-secondary btn-lg">Forecast 🔮</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function KPICard({ title, value, icon }: { title: string, value: string, icon: React.ReactNode }) {
  return (
    <div className="feature-card" style={{ padding: '2rem', position: 'relative', overflow: 'hidden' }}>
      <div style={{ position: 'absolute', top: '1rem', right: '1rem', opacity: 0.1 }}>{icon}</div>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.5rem' }}>{title}</p>
      <h2 style={{ fontSize: '2.2rem', fontWeight: 800, letterSpacing: '-0.02em' }}>{value}</h2>
    </div>
  );
}
