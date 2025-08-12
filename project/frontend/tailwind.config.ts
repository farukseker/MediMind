import type { Config } from "tailwindcss";
import daisyui from "daisyui";

const config: Config = {
    content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.js',
    './nuxt.config.{js,ts}',
  ],
  theme: {
    extend: {
      fontFamily: {
        rosemary: ['Rosemary', 'sans-serif'],
      },
    },
  },
  plugins: [daisyui({themes:'all'})],
  
}

export default config;
