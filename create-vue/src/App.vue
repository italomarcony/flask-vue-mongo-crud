<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <!-- Botão Home com margem à esquerda para afastar da borda -->
      <v-btn text to="/" class="ml-16">Home</v-btn>

      <!-- Centralizando o título 'Tabel' -->
      <v-spacer></v-spacer>
      <!-- Esto cria o espaço que empurra o título para o centro -->
      <v-toolbar-title>Tabel</v-toolbar-title>
      <v-spacer></v-spacer>
      <!-- Cria o espaço necessário para centralizar -->
    </v-app-bar>

    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<style scoped>
/* Estilos adicionais não são necessários, pois estamos utilizando as classes do Vuetify para layout */
</style>
