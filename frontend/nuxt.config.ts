// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: true,
  modules: ['@nuxt/eslint', '@nuxt/icon',
            '@nuxt/image'],
  css: ['~/assets/css/main.css',],  
  devtools: { enabled: false},
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  routeRules: {
    '/admin/**': { ssr: false, redirect: '/login' },
  },
  compatibilityDate: '2025-01-07',

  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL,
      NODE_ENV: process.env.ENVIRONMENT
    }
  }
  
})