import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import JsonViewer from 'vue-json-viewer'
// import VueExcelXlsx from "vue-excel-xlsx";
import VueExcelEditor from 'vue-excel-editor'

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(JsonViewer)
Vue.use(VueExcelEditor)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
