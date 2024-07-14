<template>
    <nav>
        <v-navigation-drawer v-model="drawer" app>
            <v-list-item>
                <v-list-item-content>
                <v-list-item-title class="text-h6">
                    My Demo App
                </v-list-item-title>
                </v-list-item-content>
            </v-list-item>

            <v-divider></v-divider>

            <v-list dense nav>
                <v-list-item v-for="item in menuItems" :key="item.title" :to="item.route">
                <v-list-item-icon>
                    <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar app>
            <v-app-bar-nav-icon v-if="isAuthenticated" @click="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title>Demo KIC</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn v-if="isAuthenticated" text @click="logout">
                <v-icon>mdi-logout</v-icon>
                Logout
            </v-btn>
        </v-app-bar>
    </nav>
</template>

<script>
    import { mapGetters} from 'vuex';


    export default {
        computed: {
        ...mapGetters(['isAuthenticated'])
        },
        data() {
            return {
            drawer: true,
            menuItems: [
                { title: 'Home', icon: 'mdi-home', route: '/dashboard' },
                { title: 'Users', icon: 'mdi-account-multiple', route: '/users' },
            ],
            };
        },
        methods: {
            logout() {
            // Implement logout logic here
            localStorage.removeItem('token');
            this.$router.push('/login');
            },
        },
    };
</script>