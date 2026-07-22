export default defineNuxtConfig({
  compatibilityDate: '2026-07-22',
  modules: ['@pinia/nuxt'],
  app: {
    head: {
      link: [
        { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' }
      ],
      script: [
        { src: 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js', tagPosition: 'bodyClose' }
      ]
    }
  },
  runtimeConfig: {
    public: {
      apiBase: 'http://127.0.0.1:8000',
    },
  },
})
