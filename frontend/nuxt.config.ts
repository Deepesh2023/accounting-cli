export default defineNuxtConfig({
  compatibilityDate: '2026-06-30',
  devtools: { enabled: true },
  modules: ['@nuxt/ui', '@nuxt/icon', '@pinia/nuxt'],
  css: ['~/assets/css/main.css'],

  ui: {
    colors: {
      primary: 'blue',
      neutral: 'slate',
    },
  },
})
