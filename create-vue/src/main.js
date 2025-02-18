import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify"; // Ou a configuração que você estiver usando para Vuetify

import {
  VApp,
  VAppBar,
  VSpacer,
  VToolbarTitle,
  VMain,
  VBtn,
  VDataTable,
  VCard,
  VCardTitle,
  VCardText,
  VCardActions,
  VTextField,
  VDialog,
  VContainer,
  VSwitch, // Importando o VSwitch
  VIcon, // Importando o VIcon
} from "vuetify/components";

// Criação da instância do Vue
const app = createApp(App);

// Registrando os componentes do Vuetify, incluindo VSwitch e VIcon
app.component("VApp", VApp);
app.component("VAppBar", VAppBar);
app.component("VSpacer", VSpacer);
app.component("VToolbarTitle", VToolbarTitle);
app.component("VMain", VMain);
app.component("VBtn", VBtn);
app.component("VDataTable", VDataTable);
app.component("VCard", VCard);
app.component("VCardTitle", VCardTitle);
app.component("VCardText", VCardText);
app.component("VCardActions", VCardActions);
app.component("VTextField", VTextField);
app.component("VDialog", VDialog);
app.component("VContainer", VContainer);
app.component("VSwitch", VSwitch); // Registrando o VSwitch
app.component("VIcon", VIcon); // Registrando o VIcon

// Configuração do router e Vuetify
app.use(router);
app.use(vuetify);

app.mount("#app");
