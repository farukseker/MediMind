// plugins/highlight.js
import hljs from 'highlight.js';

export default defineNuxtPlugin(nuxtApp => {
  nuxtApp.vueApp.directive('highlight', {
    mounted(el) {
      const blocks = el.querySelectorAll('pre code');
      blocks.forEach(block => {
        hljs.highlightElement(block); // Otomatik vurgulama
      });
    },
  });
});
