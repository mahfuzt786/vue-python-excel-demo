<template>
  <v-app>
    <v-main>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6" lg="4">
            <v-card>
              <v-card-title>Login</v-card-title>
              <v-card-text>
                <v-form ref="loginForm" @submit.prevent="login">
                  <v-text-field
                    v-model="email"
                    label="Email"
                    type="email"
                    :rules="[rules.required, rules.email]"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="password"
                    label="Password"
                    type="password"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                  <v-checkbox
                    v-model="rememberMe"
                    label="Remember me"
                  ></v-checkbox>
                  <v-btn type="submit" color="primary" block>Login</v-btn>
                </v-form>
                <v-alert v-if="error" type="error" class="mt-4">
                  {{ error }}
                </v-alert>
              </v-card-text>
              <v-card-actions>
                <v-btn text color="primary" @click="showRegistration()">
                  Register
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="showForgotPassword()">
                  Forgot Password
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
      email: '',
      password: '',
      rememberMe: false,
      // showRegistration: false,
      // showForgotPassword: false,
      error: null,
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
    async login() {
      if (this.$refs.loginForm.validate()) {
        try {
          // Implement JWT authentication logic here
          const token = await this.$store.dispatch('login', {
            email: this.email,
            password: this.password,
          });
          // Save the token and redirect to the dashboard
          localStorage.setItem('token', token);
          this.$router.push('/dashboard');
        } catch (error) {        
          // Display an error message to the user
          this.error = error.response.data.msg;
        }
      }
    },
    showRegistration() {
      this.$router.push('/register');
    },
    showForgotPassword() {

    },

  },
};
</script>