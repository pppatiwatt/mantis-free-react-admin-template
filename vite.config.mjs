import react from '@vitejs/plugin-react';
import path from 'path';
import { defineConfig } from 'vite';
import jsconfigPaths from 'vite-jsconfig-paths';

export default defineConfig({
  plugins: [react(), jsconfigPaths()],
  base: '/free',
  define: {
    global: 'window'
  },
  resolve: {
    alias: [
      {
        find: /^~(.+)/,
        replacement: path.join(process.cwd(), 'node_modules/$1')
      },
      {
        find: /^src(.+)/,
        replacement: path.join(process.cwd(), 'src/$1')
      },
      {
        find: 'pages',
        replacement: path.join(process.cwd(), 'src/pages')
      },
      {
        find: 'analyze',
        replacement: path.join(process.cwd(), 'src/pages/analyze')
      }
    ]
  },
  server: {
    open: true,
    port: 3000
  },
  preview: {
    open: true,
    port: 3000
  }
});