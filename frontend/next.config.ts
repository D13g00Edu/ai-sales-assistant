import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Configuración para que funcione en Render
  // Deshabilitamos trailingSlash que suele dar problemas de MIME
  trailingSlash: false,
};

export default nextConfig;
