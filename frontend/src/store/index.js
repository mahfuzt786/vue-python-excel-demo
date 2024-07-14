// import Vue from 'vue'
// import Vuex from 'vuex'
// import axios from 'axios'

// Vue.use(Vuex)

// export default new Vuex.Store({
//   state: {
//   },
//   mutations: {
//   },
//   actions: {
//     calculateValuesApi(state, input) {
//       console.log(input)
//       // console.log('values', JSON.stringify(input))
//       const formData = new FormData();
//       formData.append('data', JSON.stringify(input));

//       // imp to load output in different structure for test and Addy
//       // formData.append('ENVIRONMENT', 'TEST');
//       formData.append('ENVIRONMENT', 'PROD');

//       return axios.post('http://localhost/dental-api/', formData)
//       // return axios.post('https://www.alegralabs.com/syed/dental-api/', formData)

//       // return axios.post('http://localhost/dental-api-QA/', formData)
//       // return axios.post('https://www.alegralabs.com/syed/dental-api-QA/', formData)
//     }
//   },
//   modules: {
//   }
// })


import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import * as XLSX from 'xlsx';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: null,
    user: null,
    users: [],
    workbook: null,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    setUser(state, user) {
      state.user = user;
    },
    setUsers(state, users) {
      state.users = users;
    },
    setWorkbook(state, workbook) {
      state.workbook = workbook;
    },
  },
  actions: {
    async login({ commit }, { email, password }) {
      const response = await axios.post('http://127.0.0.1:8001/api/login', { email, password });
      const token = response.data.access_token;
      const user = response.data.user;

      commit('setToken', token);
      commit('setUser', user);
      return token;
    },
    async register(_, { name, email, address, password, contactNumber }) {
      const response = await axios.post('http://127.0.0.1:8001/api/register', { name, email, address, password, contactNumber });
      const message = response.data.message;
      // commit('setToken', token);
      return message;
    },
    async fetchUsers({ commit }) {
      const response = await axios.get('http://127.0.0.1:8001/api/users', {
        headers: {
          Authorization: `Bearer ${this.state.token}`,
        },
      });
      commit('setUsers', response.data);
      return response.data;
    },
    async createUser(_, { name, email, address, password, contactNumber }) {
      const response = await axios.post(`http://127.0.0.1:8001/api/users`, { name, email, address, password, contactNumber }, {
        headers: {
          Authorization: `Bearer ${this.state.token}`,
        },
      });
      return response.data;
    },
    async updateUser(_, user) {
      const response = await axios.put(`http://127.0.0.1:8001/api/users/${user.id}`, user, {
        headers: {
          Authorization: `Bearer ${this.state.token}`,
        },
      });
      return response.data;
    },
    async deleteUser(_, userId) {
      await axios.delete(`http://127.0.0.1:8001/api/users/${userId}`, {
        headers: {
          Authorization: `Bearer ${this.state.token}`,
        },
      });
    },
    async fetchExcelFile({ commit }) {
      try {
        // Fetch the Excel file from the backend
        const response = await axios.get('http://127.0.0.1:8001/api/excel-file', { responseType: 'arraybuffer' });
        const workbook = await XLSX.read(response.data);

        commit('setWorkbook', workbook);
      } catch (error) {
        console.error(error);
        throw error;
      }
    },
    async saveWorksheetToDatabase(_, { tableName, data }) {
      await axios.post('http://127.0.0.1:8001/api/worksheets', { tableName, data }, {
        headers: {
          Authorization: `Bearer ${this.state.token}`,
        },
      });
    },
  },
  getters: {
    isAuthenticated(state) {
      return !!state.token;
    },
    user(state) {
      return state.user;
    }
  }
});
