import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Sales Assistant | Análisis Inteligente de Ventas",
  description:
    "Sube tu Excel de ventas y obtén dashboards automáticos, preguntas en lenguaje natural y forecasting con IA. Potenciado por OpenAI y Prophet.",
  keywords: ["ventas", "IA", "dashboard", "forecast", "análisis", "excel"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
