<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>
            User Management
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="showCreateDialog = true" v-if="isAdmin">
              Create User
            </v-btn>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="users"
            :search="search"
            :loading="loading"
            :page.sync="page"
            :items-per-page="itemsPerPage"
            @page-count="pageCount = $event"
            class="elevation-1"
          >
            <template v-slot:item.actions="{ item }">
              <v-btn
                color="primary"
                small
                class="mr-2"
                @click="editUser(item)"
              >
                Edit
              </v-btn>
              <!-- <v-btn
                color="error"
                small
                v-if="isAdmin"
                @click="deleteUser(item)"
              >
                Delete
              </v-btn> -->
              <v-btn
                color="error"
                small
                v-if="isAdmin"
                @click="showDeleteConfirmation(item)"
              >
                Delete
              </v-btn>
            </template>
          </v-data-table>
          <v-pagination
            v-model="page"
            :length="pageCount"
            :total-visible="7"
          ></v-pagination>
          <v-dialog v-model="showEditDialog" max-width="600px">
            <v-card>
              <v-card-title>Edit User</v-card-title>
              <v-card-text>
                <v-form ref="editForm" @submit.prevent="saveUser">
                  <v-text-field
                    v-model="editedUser.name"
                    label="Name"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="editedUser.email"
                    label="Email"
                    type="email"
                    :rules="[rules.required, rules.email]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="editedUser.address"
                    label="Address"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="editedUser.contactNumber"
                    label="Contact Number"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-btn type="submit" color="primary" block>Save</v-btn>
                </v-form>
                <v-alert v-if="error" type="error" class="mt-4">
                  {{ error }}
                </v-alert>
              </v-card-text>
              <v-card-actions>
                <v-btn text color="primary" @click="showEditDialog = false">
                  Cancel
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="showCreateDialog" max-width="600px">
            <v-card>
              <v-card-title>Create User</v-card-title>
              <v-card-text>
                <v-form ref="createForm" @submit.prevent="createUser">
                  <v-text-field
                    v-model="newUser.name"
                    label="Name"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="newUser.email"
                    label="Email"
                    type="email"
                    :rules="[rules.required, rules.email]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="newUser.password"
                    label="Password"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>

                  <v-text-field
                    v-model="newUser.address"
                    label="Address"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="newUser.contactNumber"
                    label="Contact Number"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-btn type="submit" color="primary" block>Create</v-btn>
                </v-form>
                <v-alert v-if="error" type="error" class="mt-4">
                  {{ error }}
                </v-alert>
              </v-card-text>
              <v-card-actions>
                <v-btn text color="primary" @click="showCreateDialog = false">
                  Cancel
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="showDeleteDialog" max-width="400px">
            <v-card>
              <v-card-title>Confirm Delete</v-card-title>
              <v-card-text>
                Are you sure you want to delete user: 
                {{ userToDelete.name }}?
              </v-card-text>
              <v-card-actions>
                <v-btn text color="primary" @click="showDeleteDialog = false">
                  Cancel
                </v-btn>
                <v-btn text color="error" @click="deleteUser">
                  Delete
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        { text: 'Name', value: 'name' },
        { text: 'Email', value: 'email' },
        { text: 'Address', value: 'address' },
        { text: 'Contact Number', value: 'contactNumber' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      users: [],
      search: '',
      loading: true,
      page: 1,
      itemsPerPage: 10,
      pageCount: 0,
      showEditDialog: false,
      showCreateDialog: false,
      editedUser: {
        id: null,
        name: '',
        email: '',
        address: '',
        contactNumber: '',
      },
      newUser: {
        name: '',
        email: '',
        password: '',
        address: '',
        contactNumber: '',
      },
      error: null,
      rules: {
        required: (value) => !!value || 'This field is required.',
        email: (value) => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return pattern.test(value) || 'Invalid email address.';
        },
      },
      showDeleteDialog: false,
      // userToDelete: null,
      userToDelete: {
        id: null,
        name: '',
        email: '',
        address: '',
        contactNumber: '',
      },
    };
  },
  created() {
    this.fetchUsers();
  },
  computed: {
    isAdmin() {
      return this.$store.state.user && this.$store.state.user.role === 'admin';
    },
  },
  methods: {
    async fetchUsers() {
      try {
        this.loading = true;
        // Fetch users from the backend
        this.users = await this.$store.dispatch('fetchUsers');
      } catch (error) {
        this.error = error.response.data.msg;
      } finally {
        this.loading = false;
      }
    },
    async editUser(user) {
      this.editedUser = { ...user };
      this.showEditDialog = true;
    },
    async saveUser() {
      if (this.$refs.editForm.validate()) {
        try {
          // Implement edit user logic here
          await this.$store.dispatch('updateUser', this.editedUser);
          this.showEditDialog = false;
          this.fetchUsers();
        } catch (error) {
          this.error = error.response.data.msg;
        }
      }
    },
    showDeleteConfirmation(user) {
      this.userToDelete = user;
      this.showDeleteDialog = true;
    },
    async deleteUser() {
      try {
        // Implement delete user logic here
        await this.$store.dispatch('deleteUser', this.userToDelete.id);
        this.fetchUsers();
        this.showDeleteDialog = false;
      } catch (error) {
        this.error = error.response.data.msg;
      }
    },
    async createUser() {
      if (this.$refs.createForm.validate()) {
        try {
          // Implement create user logic here
          await this.$store.dispatch('createUser', this.newUser);
          this.showCreateDialog = false;
          this.fetchUsers();
        } catch (error) {
          this.error = error.response.data.msg;
        }
      }
    },
  },
};
</script>