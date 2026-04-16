'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Bot, User, Send, Database, Terminal, Table as TableIcon } from 'lucide-react';

export default function AskPage() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    const userQuestion = question;
    setQuestion('');
    setLoading(true);
    setError(null);

    // Agregar mensaje del usuario al historial
    const newHistory = [...history, { role: 'user', content: userQuestion }];
    setHistory(newHistory);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userQuestion }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Error en la consulta');

      setHistory([...newHistory, { role: 'ai', ...data }]);
    } catch (err: any) {
      setError(err.message);
      setHistory([...newHistory, { role: 'error', content: err.message }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="landing" style={{ padding: '6rem 2rem 2rem', minHeight: '100vh' }}>
      <nav className="navbar">
        <Link href="/" className="navbar-brand">
          <div className="navbar-logo">SA</div>
          <div className="navbar-title">Sales Assistant</div>
        </Link>
        <div className="navbar-actions">
           <Link href="/architecture" className="btn btn-secondary">Arquitectura</Link>
           <Link href="/dashboard" className="btn btn-secondary">Panel de Gráficos</Link>
        </div>
      </nav>

      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <header style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <h1 className="section-title">Pregunta a tus Datos</h1>
          <p style={{ color: 'var(--text-secondary)' }}>La IA generará SQL en tiempo real para consultar tu base DuckDB.</p>
        </header>

        {/* Chat Area */}
        <div className="feature-card" style={{ height: '500px', overflowY: 'auto', marginBottom: '1.5rem', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {history.length === 0 && (
            <div style={{ margin: 'auto', textAlign: 'center', color: 'var(--text-muted)' }}>
              <Bot size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
              <p>Prueba con: "¿Cuál fue el mes con más ventas?" o "¿Qué producto es el más popular en Surco?"</p>
            </div>
          )}
          
          {history.map((msg, i) => (
            <div key={i} style={{ alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', maxWidth: '85%' }}>
              <div style={{ 
                display: 'flex', 
                gap: '0.75rem', 
                flexDirection: msg.role === 'user' ? 'row-reverse' : 'row'
              }}>
                <div style={{ 
                  width: '32px', height: '32px', borderRadius: '50%', background: msg.role === 'user' ? 'var(--accent-primary)' : 'var(--bg-input)', 
                  display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0
                }}>
                  {msg.role === 'user' ? <User size={16} color="white" /> : <Bot size={16} color="var(--accent-primary)" />}
                </div>
                
                <div style={{ 
                  background: msg.role === 'user' ? 'var(--accent-gradient)' : 'var(--bg-input)',
                  padding: '1rem', borderRadius: '12px', color: 'white',
                  border: msg.role === 'ai' ? '1px solid var(--border-color)' : 'none'
                }}>
                  {msg.role === 'user' ? msg.content : (
                    <div>
                      <p style={{ fontWeight: 500, lineHeight: '1.5' }}>{msg.summary}</p>
                      
                      {msg.sql && (
                        <details style={{ marginTop: '1rem', fontSize: '0.8rem' }}>
                          <summary style={{ cursor: 'pointer', color: 'var(--accent-primary)', opacity: 0.8 }}>Ver SQL Generado</summary>
                          <pre style={{ background: '#000', padding: '0.75rem', borderRadius: '4px', marginTop: '0.5rem', overflowX: 'auto', color: '#10b981' }}>
                            {msg.sql}
                          </pre>
                        </details>
                      )}

                      {msg.result && msg.result.length > 0 && (
                        <details style={{ marginTop: '0.5rem', fontSize: '0.8rem' }}>
                          <summary style={{ cursor: 'pointer', color: 'var(--accent-primary)', opacity: 0.8 }}>Ver Datos Brutos</summary>
                          <div style={{ marginTop: '0.5rem', maxHeight: '200px', overflowY: 'auto' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', color: 'var(--text-secondary)' }}>
                              <thead>
                                <tr>{Object.keys(msg.result[0]).map(k => <th key={k} style={{ textAlign: 'left', borderBottom: '1px solid var(--border-color)', padding: '4px' }}>{k}</th>)}</tr>
                              </thead>
                              <tbody>
                                {msg.result.slice(0, 5).map((r: any, ri: number) => (
                                  <tr key={ri}>{Object.values(r).map((v: any, vi) => <td key={vi} style={{ padding: '4px', borderBottom: '1px solid rgba(255,255,255,0.02)' }}>{String(v)}</td>)}</tr>
                                ))}
                              </tbody>
                            </table>
                            {msg.result.length > 5 && <p style={{ fontSize: '0.7rem', marginTop: '0.5rem' }}>+ {msg.result.length - 5} filas más...</p>}
                          </div>
                        </details>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
          {loading && <div style={{ alignSelf: 'flex-start', color: 'var(--text-muted)', fontSize: '0.9rem' }}>La IA está consultando DuckDB...</div>}
        </div>

        {/* Input Area */}
        <form onSubmit={handleAsk} style={{ display: 'flex', gap: '0.75rem' }}>
          <input 
            type="text" 
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={loading}
            placeholder="Escribe tu pregunta aquí..." 
            style={{ 
              flex: 1, background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '12px', 
              padding: '1rem 1.5rem', color: 'white', outline: 'none'
            }}
          />
          <button type="submit" disabled={!question.trim() || loading} className="btn btn-primary" style={{ padding: '0 1.5rem', borderRadius: '12px' }}>
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}
