<template>
  <v-container>
    <!-- Botão Create User com margem para afastá-lo da tabela -->
    <v-btn color="primary" @click="openCreateModal" class="mb-4"
      >Create User</v-btn
    >

    <!-- Tabela de Usuários -->
    <v-data-table
      :headers="headers"
      :items="users"
      item-key="username"
      class="elevation-1"
      :items-per-page="5"
    >
      <template v-slot:top>
        <div class="d-flex justify-space-between align-center">
          <div class="headline" style="flex: 1; min-width: 120px">Username</div>
          <div class="headline" style="flex: 1; min-width: 120px">Roles</div>
          <div class="headline" style="flex: 1; min-width: 120px">Timezone</div>
          <div class="headline" style="flex: 1; min-width: 120px">
            Is Active?
          </div>
          <div class="headline" style="flex: 1; min-width: 120px">
            Last Updated At
          </div>
          <div class="headline" style="flex: 1; min-width: 120px">
            Created At
          </div>
          <div class="headline" style="flex: 1; min-width: 120px">Actions</div>
        </div>
      </template>

      <!-- Nome de usuário com link -->
      <template v-slot:[`item.username`]="{ item }">
        <v-btn text @click="goToUserPage(item.username)">
          {{ item.username }}
        </v-btn>
      </template>

      <!-- Roles com formato de string -->
      <template v-slot:[`item.roles`]="{ item }">
        <span>{{ item.roles ? item.roles.join(", ") : "N/A" }}</span>
      </template>

      <!-- Timezone -->
      <template v-slot:[`item.timezone`]="{ item }">
        <span>{{ item.preferences ? item.preferences.timezone : "N/A" }}</span>
      </template>

      <!-- Formatação de data -->
      <template v-slot:[`item.createdAt`]="{ item }">
        <span>{{ formatDate(item.createdAt) }}</span>
      </template>

      <!-- Última atualização -->
      <template v-slot:[`item.lastUpdatedAt`]="{ item }">
        <span>{{ formatDate(item.lastUpdatedAt) }}</span>
      </template>

      <!-- Ações (Editar/Deletar) -->
      <template v-slot:item.actions="{ item }">
        <v-btn @click="editUser(item)">Edit</v-btn>
        <v-btn @click="deleteUser(item)">Delete</v-btn>
      </template>
    </v-data-table>

    <!-- Modal de criação/edição -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ isEdit ? "Edit User" : "Create User" }}</v-card-title>
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
          <v-btn @click="saveUser">{{ isEdit ? "Save" : "Create" }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      headers: [
        { text: "Username", align: "start", value: "username" },
        { text: "Roles", value: "roles" },
        { text: "Timezone", value: "timezone" },
        { text: "Is Active?", value: "active" },
        { text: "Last Updated At", value: "lastUpdatedAt" },
        { text: "Created At", value: "createdAt" },
        { text: "Actions", value: "actions", sortable: false },
      ],
      dialog: false,
      isEdit: false,
      userForm: {
        username: "",
        password: "",
        roles: "",
        timezone: "",
        active: true,
        lastUpdatedAt: "",
        createdAt: "",
      },
      currentUsername: "",
    };
  },
  methods: {
    fetchUsers() {
      console.log("Fetching users...");
      axios
        .get("http://127.0.0.1:5000/users")
        .then((response) => {
          console.log("Users fetched:", response.data);
          this.users = response.data;
        })
        .catch((error) => {
          console.log("Error fetching users:", error);
        });
    },
    openCreateModal() {
      this.isEdit = false;
      this.userForm = {
        username: "",
        password: "",
        roles: "",
        timezone: "",
        active: true,
        lastUpdatedAt: "",
        createdAt: "",
      };
      this.dialog = true;
    },
    editUser(user) {
      this.isEdit = true;
      this.userForm = { ...user, roles: user.roles.join(", ") };
      this.currentUsername = user.username;
      this.dialog = true;
    },
    deleteUser(user) {
      if (confirm(`Are you sure you want to delete ${user.username}?`)) {
        axios
          .delete(`http://127.0.0.1:5000/users/${user.username}`)
          .then(() => {
            this.fetchUsers();
            alert("User deleted successfully.");
          })
          .catch((error) => {
            alert("Error deleting user.");
            console.log("Error deleting user:", error);
          });
      }
    },
    saveUser() {
      const data = {
        ...this.userForm,
        roles: this.userForm.roles.split(", ").map((role) => role.trim()),
      };

      // Verifica se o nome de usuário foi alterado
      if (this.currentUsername !== this.userForm.username) {
        if (confirm("Are you sure you want to change the username?")) {
          axios
            .delete(`http://127.0.0.1:5000/users/${this.currentUsername}`)
            .then(() => {
              axios
                .post("http://127.0.0.1:5000/users", data)
                .then(() => {
                  this.dialog = false;
                  this.fetchUsers();
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
        axios
          .put(`http://127.0.0.1:5000/users/${this.userForm.username}`, data)
          .then(() => {
            this.dialog = false;
            this.fetchUsers();
            alert("User updated successfully.");
          })
          .catch((error) => {
            alert("Error updating user.");
            console.log("Error updating user:", error);
          });
      }
    },
    formatDate(date) {
      if (!date) return "N/A";
      const d = new Date(date);
      return d.toLocaleString();
    },
    goToUserPage(username) {
      this.$router.push({ name: "userPage", params: { username } });
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>
