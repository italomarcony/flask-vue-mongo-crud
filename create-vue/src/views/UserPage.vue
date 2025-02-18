<template>
  <v-container>
    <v-card v-if="user.username">
      <v-card-title>User Details</v-card-title>
      <v-card-subtitle>{{ user.username }}</v-card-subtitle>
      <v-card-text>
        <p>Roles: {{ user.roles.join(", ") }}</p>
        <p>Timezone: {{ user.preferences.timezone }}</p>
        <p>Active: {{ user.active }}</p>
        <p>
          Created At: {{ new Date(user.created_ts * 1000).toLocaleString() }}
        </p>
        <p>
          Last Updated At:
          {{ new Date(user.updated_ts * 1000).toLocaleString() }}
        </p>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="deleteUser">Delete</v-btn>
        <v-btn @click="editUser">Edit</v-btn>
      </v-card-actions>
    </v-card>

    <v-alert v-else type="error" dismissible> User not found. </v-alert>

    <!-- Modal de Edição -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>Edit User</v-card-title>
        <v-card-text>
          <v-text-field v-model="userForm.username" label="Username" />
          <v-text-field
            v-model="userForm.password"
            label="Password"
            type="password"
          />
          <v-text-field
            v-model="userForm.roles"
            label="Roles (comma separated)"
          />
          <v-text-field v-model="userForm.timezone" label="Timezone" />
          <v-switch
            v-model="userForm.active"
            label="Is Active?"
            :false-value="false"
            :true-value="true"
          />
          <v-text-field
            v-model="userForm.lastUpdatedAt"
            label="Last Updated At"
            disabled
          />
          <v-text-field
            v-model="userForm.createdAt"
            label="Created At"
            disabled
          />
        </v-card-text>
        <v-card-actions>
          <v-btn @click="dialog = false">Cancel</v-btn>
          <v-btn @click="saveUser">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  props: ["username"],
  data() {
    return {
      user: {},
      dialog: false,
      userForm: {
        username: "",
        password: "",
        roles: "",
        timezone: "",
        active: true,
        lastUpdatedAt: "",
        createdAt: "",
      },
      currentUsername: "", // Armazena o nome de usuário atual para verificar se mudou
    };
  },
  methods: {
    fetchUser() {
      axios
        .get(`http://127.0.0.1:5000/users/${this.username}`)
        .then((response) => {
          this.user = response.data;
          this.userForm = { ...this.user, roles: this.user.roles.join(", ") }; // Preenche o formulário com os dados do usuário
          this.currentUsername = this.user.username; // Armazena o nome de usuário atual
        })
        .catch((error) => {
          this.user = {}; // Limpa os dados se não encontrar o usuário
          console.error("User not found", error);
        });
    },
    deleteUser() {
      if (confirm(`Are you sure you want to delete ${this.user.username}?`)) {
        axios
          .delete(`http://127.0.0.1:5000/users/${this.user.username}`)
          .then(() => this.$router.push("/"));
      }
    },
    editUser() {
      this.dialog = true; // Abre o modal de edição
    },
    saveUser() {
      const data = {
        ...this.userForm,
        roles: this.userForm.roles.split(", ").map((role) => role.trim()),
      };

      // Verifica se o nome de usuário foi alterado
      if (this.currentUsername !== this.userForm.username) {
        // Caso o nome de usuário tenha sido alterado, cria um novo e deleta o antigo
        if (confirm("Are you sure you want to change the username?")) {
          // Deleta o usuário antigo
          axios
            .delete(`http://127.0.0.1:5000/users/${this.currentUsername}`)
            .then(() => {
              // Cria o novo usuário
              axios
                .post("http://127.0.0.1:5000/users", data)
                .then(() => {
                  this.dialog = false;
                  this.fetchUser(); // Recarrega os dados atualizados do usuário
                  alert("User updated successfully.");
                })
                .catch((error) => {
                  alert("Error creating new user.");
                  console.log("Error creating new user:", error);
                });
            })
            .catch((error) => {
              alert("Error deleting old user.");
              console.log("Error deleting old user:", error);
            });
        }
      } else {
        // Caso o nome de usuário não tenha mudado, faz a atualização normalmente
        axios
          .put(`http://127.0.0.1:5000/users/${this.userForm.username}`, data)
          .then(() => {
            this.dialog = false; // Fecha o modal após salvar
            this.fetchUser(); // Recarrega os dados atualizados do usuário
            alert("User updated successfully.");
          })
          .catch((error) => {
            alert("Error updating user.");
            console.log("Error updating user:", error);
          });
      }
    },
  },
  mounted() {
    this.fetchUser();
  },
};
</script>
