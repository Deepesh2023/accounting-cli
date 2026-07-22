export default defineNuxtConfig({
  compatibilityDate: '2026-07-22',
  modules: ['@nuxt/ui', '@nuxt/icon', '@pinia/nuxt'],
  css: ['~/assets/main.css'],
  runtimeConfig: {
    apiBase: 'http://127.0.0.1:8000',
  },
})
