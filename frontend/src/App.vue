<template>
  <v-app>
    

    <v-main>
      <v-container>
        <Navbar></Navbar>

        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
  import Navbar from './components/Navbar.vue';

  export default {
    name: 'App',

    components: {
      Navbar,
    },

    data: () => ({
      //
    }),
  };

</script>