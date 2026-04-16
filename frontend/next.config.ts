import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  // Sincronizar trailing slash para evitar errores de MIME types en Render
  trailingSlash: true,
};

export default nextConfig;
