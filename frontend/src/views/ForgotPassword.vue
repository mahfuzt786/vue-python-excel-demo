<template>
    <v-container>
      <v-row>
        <v-col cols="12" md="6" offset-md="3">
          <v-card>
            <v-card-title>
              <span class="headline">Forgot Password</span>
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="recoverPassword">
                <v-text-field v-model="email" label="Email" required></v-text-field>
                <v-btn type="submit" color="primary">Recover Password</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        email: '',
      };
    },
    methods: {
      async recoverPassword() {
        try {
          const response = await axios.post('/auth/recover-password', {
            email: this.email,
          });
          console.log('Recovery email sent:', response.data);
        } catch (error) {
          console.error('Error recovering password:', error);
        }
      },
    },
  };
  </script>
  