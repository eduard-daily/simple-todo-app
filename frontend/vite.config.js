import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // Default port Vite uses
    host: true, // Allows access from network (needed for Docker)
    // Optional: Proxy API requests to backend during development
    // to avoid CORS issues if frontend and backend are on different origins
    // proxy: {
    //   '/api': {
    //     target: 'http://localhost:8000', // Your backend address
    //     changeOrigin: true,
    //     // rewrite: (path) => path.replace(/^\/api/, '') // if backend doesn't have /api prefix
    //   }
    // }
  }
})
