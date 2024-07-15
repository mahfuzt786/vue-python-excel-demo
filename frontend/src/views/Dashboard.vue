<template>
  <v-app>
    <v-container>
      <v-tabs v-model="currentTab">
        <v-tab v-for="(sheet, index) in sheets" :key="index">{{ sheet }}</v-tab>
      </v-tabs>
      <v-tabs-items v-model="currentTab">
        <v-tab-item v-for="(sheet, index) in sheets" :key="index">
          <data-table :sheet="sheet"></data-table>
        </v-tab-item>
      </v-tabs-items>
    </v-container>
  </v-app>
</template>

<script>
import DataTable from '../components/DataTable.vue';

export default {
  components: { DataTable },
  data() {
    return {
      currentTab: 0,
      sheets: ['SECURITY_TRANSACTIONS', 'SECURITY_MASTER', 'SEC_ACC_MASTER'],
    };
  },
};
</script>

