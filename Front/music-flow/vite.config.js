import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'



export default defineConfig({
  // server: {
  // https: true},
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
