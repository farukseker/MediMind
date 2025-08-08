// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  build: {
    analyze: true,
  },
  devServer: {
    // https: {
    //   key: './.ssl/192.168.123.97-key.pem',
    //   cert: './.ssl/192.168.123.97.pem',
    // },
    // host: '192.168.123.97',
    // port: 6020,
  },
  devtools: {
    enabled: true,

    timeline: {
      enabled: true,
    },
  },
  // plugins: [{ src: '~/plugins/registerServiceWorker.js', mode: 'client' }],
  ssr: false,
    routeRules: {
    '/': {
      headers: {
        'x-nuxt-override': 'true'
      }
    }
  },
  app: {
    head: {
      link: [
        {
          rel: 'manifest',
          href: '/manifest.webmanifest',
        },
      ],
    },
  },
  modules: [
    '@nuxt/ui',
    '@nuxtjs/tailwindcss',
    '@vesp/nuxt-fontawesome',
    '@nuxt/content',
    '@nuxtjs/mdc',
    '@nuxtjs/google-fonts',
    '@pinia/nuxt',
    '@nuxt/image',
    'vue3-carousel-nuxt',
    '@vueuse/motion/nuxt',
    '@vite-pwa/nuxt',
    '@nuxtjs/color-mode',
    '@nuxtjs/i18n',
  ],
i18n: {
  bundle: {
    optimizeTranslationDirective: false
  },
  locales: [
    { code: 'us', name: "English", language: 'en-US', file: 'en.json'},
    { code: 'tr', name: "Türkçe", language: 'tr-TR', file: 'tr.json'},
    { code: 'fr', name: "Français", language: 'fr-FR', file: 'fr.json'},
  ],
  lazy: true,
  langDir: './locales/',
  defaultLocale: 'us',
  // strategy: 'prefix',
  strategy: 'prefix_and_default',
  detectBrowserLanguage: {
    useCookie: true,
    cookieKey: 'i18n_redirected',
    fallbackLocale: 'us',
    alwaysRedirect: false,
  },
},
  // colorMode: {
  //   classSuffix: '',
  //   preference: 'light',
  //   fallback: 'light',
  // },
  colorMode: {
    preference: 'system',
    dataValue: 'theme', // <html data-theme="">
    classSuffix: '',
  },
  tailwindcss: { exposeConfig: true },
  pwa: {
    workbox: {
      globPatterns: [
        '**/*',  // ya da sadece ihtiyacın olanları yaz
        // "**/_payload.json", // bunu kaldır
      ],
      globIgnores: [
        '**/node_modules/**/*',
        'sw.js',
        'workbox-*.js',
      ],
    },
    registerType: 'autoUpdate',
    manifest: {
      name: 'Medicine Tracker',
      short_name: 'Pars Meds',
      description: 'Tracker',
      theme_color: '#ffffff',
      "icons": [
        {
          "src": "/icons/launchericon-192-192.png",
          "sizes": "192x192",
          "type": "image/png"
        },
        {
          "src": "/icons/launchericon-512-512.png",
          "sizes": "512x512",
          "type": "image/png"
        }
      ],
      "screenshots": [
        {
          "src": "/screenshots/mobile-home.png",
          "sizes": "500x778",
          "type": "image/png",
          "form_factor": "narrow"
        },
        {
          "src": "/screenshots/desktop-dashboard.png",
          "sizes": "1280x720",
          "type": "image/png",
          "form_factor": "wide"
        }
      ]
    },
  },
  image: {
    domains: ['public.blob.vercel-storage.com'],
  },
  css: [
    '@/assets/css/tailwind.css',
    'flag-icons/css/flag-icons.min.css'
  ],
  fontawesome: {
    icons: {
      solid: ['coffee', 'child',],
      regular: ['comment',],
      brands: ['twitter', 'Instagram',],
    }
  },
  vite: {
    optimizeDeps: {
      include: ['debug', 'daisyui']
    }
  },
  googleFonts: {
    families: {
      'Nunito': [400, 500, 600, 700],
      'Roboto': [400, 500, 700],
      'Ubuntu': [400, 500, 700],
      'Noto Sans Old Turkic': [400],
    },
  },
  runtimeConfig: {
    API_HOST: process.env.NUXT_API_PATH,
    public: {
      API_HOST: process.env.NUXT_API_PATH,
    }
  },

})