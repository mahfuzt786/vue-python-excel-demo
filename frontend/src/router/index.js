// import Vue from 'vue'
// import VueRouter from 'vue-router'
// import Home from '../views/Login.vue'

// Vue.use(VueRouter)

// const routes = [
//   {
//     path: '/',
//     name: 'Home',
//     component: Home
//   },
//   {
//     path: '/login',
//     name: 'Login',
//     // route level code-splitting
//     // this generates a separate chunk (about.[hash].js) for this route
//     // which is lazy-loaded when the route is visited.
//     component: () => import('../views/Login.vue')
//   },
//   {
//     path: '/register',
//     name: 'Register',
//     component: () => import('../views/Register.vue')
//   },
//   {
//     path: '/dashboard',
//     name: 'Dashboard',
//     component: () => import('../views/Dashboard.vue')
//   },
//   {
//     path: '/users',
//     name: 'Users',
//     component: () => import('../views/Users.vue')
//   }
// ]

// const router = new VueRouter({
//   mode: 'hash',
//   // mode: 'history',
//   base: process.env.BASE_URL,
//   routes
// })

// export default router


import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '../store';

Vue.use(VueRouter);

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    // meta: { requiresAuth: true },
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/Users.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '*',
    redirect: '/login'
  }
];

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  console.log(from)
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.state.token) {
      next('/login');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;