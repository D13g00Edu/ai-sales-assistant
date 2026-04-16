'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { ComposedChart, Line, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Sparkles, RefreshCw } from 'lucide-react';

export default function ForecastPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/forecast/monthly`)
      .then(res => res.json())
      .then(d => {
        if (!d.historical || d.historical.length === 0) {
            setError("No hay suficientes datos históricos para generar un pronóstico.");
            setLoading(false);
            return;
        }
        
        // Unir datos para un solo gráfico
        const historical = d.historical.map((h: any) => ({ ds: h.ds, ventas: h.y }));
        const forecast = d.forecast.map((f: any) => ({ 
            ds: f.ds, 
            prediccion: f.yhat, 
            rango: [f.yhat_lower, f.yhat_upper] 
        }));
        
        setData([...historical, ...forecast]);
        setLoading(false);
      })
      .catch(err => {
          setError("Error al conectar con el servidor de predicciones.");
          setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="landing" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <RefreshCw className="spin" />
        <p style={{ marginLeft: '1rem' }}>Generando modelo de Deep Learning...</p>
    </div>
  );

  return (
    <div className="landing" style={{ padding: '6rem 2rem' }}>
      <nav className="navbar">
        <Link href="/" className="navbar-brand">
          <div className="navbar-logo">SA</div>
          <div className="navbar-title">Sales Assistant</div>
        </Link>
        <Link href="/architecture" className="btn btn-secondary">Arquitectura</Link>
        <Link href="/dashboard" className="btn btn-secondary">Dashboard</Link>
      </nav>

      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <h1 className="section-title">Pronóstico de Ventas</h1>
        <p className="section-subtitle">Predicción basada en estacionalidad histórica con bandas de confianza al 95%.</p>

        {error ? (
            <div className="feature-card" style={{ textAlign: 'center', padding: '4rem' }}>
                <p style={{ color: 'var(--error)' }}>{error}</p>
                <Link href="/upload" className="btn btn-primary" style={{ marginTop: '1rem' }}>Sube un Excel primero</Link>
            </div>
        ) : (
            <div className="feature-card" style={{ height: '550px', padding: '2rem', marginTop: '2rem' }}>
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="ds" stroke="#8b95b0" fontSize={12} tickLine={false} />
                  <YAxis stroke="#8b95b0" fontSize={12} tickLine={false} tickFormatter={(v) => `$${v}`} />
                  <Tooltip 
                    contentStyle={{ background: '#1a2235', border: '1px solid #3b82f6', borderRadius: '8px' }}
                  />
                  <Legend verticalAlign="top" height={40} />
                  
                  {/* Histórico */}
                  <Line 
                    type="monotone" 
                    dataKey="ventas" 
                    stroke="#3b82f6" 
                    strokeWidth={4} 
                    name="Historial Real" 
                    dot={{ r: 4, fill: '#3b82f6' }} 
                  />
                  
                  {/* Predicción */}
                  <Line 
                    type="monotone" 
                    dataKey="prediccion" 
                    stroke="#8b5cf6" 
                    strokeWidth={3} 
                    strokeDasharray="8 5" 
                    name="Pronóstico IA" 
                    dot={{ r: 4, fill: '#8b5cf6' }} 
                  />
                  
                  {/* Bandas de confianza */}
                  <Area 
                    dataKey="rango" 
                    stroke="none" 
                    fill="#8b5cf6" 
                    fillOpacity={0.15} 
                    name="Intervalo de Confianza" 
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
        )}
      </div>
      <style>{`.spin { animation: spin 2s linear infinite; } @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}