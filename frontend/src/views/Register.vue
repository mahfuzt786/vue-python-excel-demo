<template>
  <v-app>
    <v-main>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6" lg="4">
            <v-card>
              <v-card-title>Register</v-card-title>
              <v-card-text>
                <v-form ref="registerForm" @submit.prevent="register">
                  <v-text-field
                    v-model="name"
                    label="Name"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="email"
                    label="Email"
                    type="email"
                    :rules="[rules.required, rules.email]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="address"
                    label="Address"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="password"
                    label="Password"
                    type="password"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="contactNumber"
                    label="Contact Number"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-btn type="submit" color="primary" block>Register</v-btn>
                </v-form>
                <v-alert v-if="error" type="error" class="mt-4">
                  {{ error }}
                </v-alert>
                <v-alert v-if="success" type="success" class="mt-4">
                  {{ success }}
                </v-alert>
              </v-card-text>
              <v-card-actions>
                <v-btn text color="primary" @click="$router.push('/login')">
                  Back to Login
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      email: '',
      address: '',
      password: '',
      contactNumber: '',
      error: null,
      success: null,
      rules: {
        required: (value) => !!value || 'This field is required.',
        email: (value) => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return pattern.test(value) || 'Invalid email address.';
        },
      },
    };
  },
  methods: {
    async register() {
      if (this.$refs.registerForm.validate()) {
        try {
          // Implement registration logic here
          const result = await this.$store.dispatch('register', {
            name: this.name,
            email: this.email,
            address: this.address,
            password: this.password,
            contactNumber: this.contactNumber,
          });

          if(result) {
            this.success = result
      
            // Redirect to the login page
            setTimeout(() => this.$router.push('/login'), 500);
          }
          else {
              this.error = this.$store.getters.errors
          }
          
        } catch (error) {
          this.error = error.response.data.msg;
        }
      }
    },
  },
};
</script>