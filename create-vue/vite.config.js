import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  define: {
    "process.env": {},
  },
  optimizeDeps: {
    include: ["vuetify"],
  },
  build: {
    rollupOptions: {
      external: ["vuetify"],
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`, // Ajuste caso tenha um arquivo de variáveis SCSS
      },
    },
  },
  server: {
    hmr: true,
  },
  // Configuração para componentes personalizados, como v-dialog e v-container
  vue: {
    compilerOptions: {
      isCustomElement: (tag) => tag.startsWith("v-"), // Permite resolver qualquer tag que comece com v- (como v-dialog, v-container, etc.)
    },
  },
});
