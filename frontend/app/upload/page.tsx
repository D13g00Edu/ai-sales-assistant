'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ message: string; rows_loaded: number } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
      setError(null);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Error al subir el archivo');
      }

      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="landing" style={{ padding: '8rem 2rem' }}>
      <nav className="navbar">
        <Link href="/" className="navbar-brand">
          <div className="navbar-logo">SA</div>
          <div className="navbar-title">Sales Assistant</div>
        </Link>
        <Link href="/architecture" className="btn btn-secondary">Arquitectura</Link>
        <Link href="/" className="btn btn-secondary">Volver al Inicio</Link>
      </nav>

      <div style={{ maxWidth: '600px', margin: '0 auto', width: '100%' }}>
        <h1 className="section-title">Cargar Datos de Ventas</h1>
        <p className="section-subtitle" style={{ marginBottom: '2rem' }}>
          Sube tu archivo .xlsx para procesar las ventas y generar el dashboard.
        </p>

        <div className="feature-card" style={{ padding: '3rem', textAlign: 'center' }}>
          <div className="feature-icon" style={{ margin: '0 auto 1.5rem', background: 'rgba(59, 130, 246, 0.1)' }}>
            {loading ? '⏳' : '📁'}
          </div>

          <input
            type="file"
            id="file-upload"
            accept=".xlsx, .xls"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          
          <label 
            htmlFor="file-upload" 
            className="btn btn-secondary" 
            style={{ marginBottom: '1rem', cursor: 'pointer', display: 'inline-flex' }}
          >
            {file ? 'Archivo Seleccionado' : 'Seleccionar Excel'}
          </label>

          {file && (
            <div style={{ marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>
              <strong>{file.name}</strong> ({(file.size / 1024).toFixed(2)} KB)
            </div>
          )}

          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="btn btn-primary"
              style={{ opacity: !file || loading ? 0.5 : 1 }}
            >
              {loading ? 'Procesando...' : '🚀 Iniciar Procesamiento'}
            </button>
          </div>

          {error && (
            <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--error)', borderRadius: 'var(--radius-md)', color: 'var(--error)' }}>
              Error: {error}
            </div>
          )}

          {result && (
            <div style={{ marginTop: '1.5rem', padding: '1.5rem', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid var(--success)', borderRadius: 'var(--radius-md)' }}>
              <div style={{ color: 'var(--success)', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                ✅ {result.message}
              </div>
              <div style={{ color: 'var(--text-primary)' }}>
                Se cargaron <strong>{result.rows_loaded}</strong> registros correctamente.
              </div>
              <Link href="/dashboard" className="btn btn-primary" style={{ marginTop: '1rem' }}>
                Ver Dashboard 📈
              </Link>
            </div>
          )}
        </div>

        <div style={{ marginTop: '2rem', padding: '1.5rem', background: 'var(--bg-card)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
          <h4 style={{ marginBottom: '1rem' }}>Estructura Sugerida:</h4>
          <ul style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', paddingLeft: '1.2rem', lineHeight: '1.8' }}>
            <li>fecha (YYYY-MM-DD)</li>
            <li>producto, categoria</li>
            <li>cliente, distrito</li>
            <li>cantidad (numérico)</li>
            <li>precio_unitario, total_venta (numérico)</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
