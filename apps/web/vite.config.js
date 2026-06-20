import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// React 16 uses the classic JSX runtime (every component does `import React`),
// so we keep jsxRuntime: 'classic'. Static assets live in public/ and are
// served at the site root (/static, /style, /seo).
export default defineConfig({
  plugins: [react({ jsxRuntime: 'classic' })],
  server: {
    host: true,
    port: 3000,
  },
  build: {
    outDir: 'dist',
  },
});
