<template>
  <v-container>
    <v-tabs v-model="activeTab">
      <v-tab v-for="(worksheet, index) in worksheets" :key="index">
        {{ worksheet.name }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="activeTab">
      <v-tab-item v-for="(worksheet, index) in worksheets" :key="index">
        <v-data-table
          :headers="worksheet.headers"
          :items="filteredData(worksheet)"
          :loading="worksheet.loading"
          :page.sync="worksheet.page"
          :items-per-page="worksheet.itemsPerPage"
          @page-count="worksheet.pageCount = $event"
          :sort-by.sync="worksheet.sortBy"
          :sort-desc.sync="worksheet.sortDesc"
          :search="worksheet.search"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>{{ worksheet.name }}</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-text-field
                v-model="worksheet.search"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
              ></v-text-field>              
              <v-btn color="primary" @click="printPdf()">
                Print
              </v-btn>
            </v-toolbar>
          </template>
          <template>
            <v-checkbox
              v-for="header in worksheet.headers"
              :key="header.value"
              v-model="header.selected"
              :label="header.text"
            ></v-checkbox>
          </template>
        </v-data-table>
      </v-tab-item>
    </v-tabs-items>
    <v-alert v-if="error" type="error" class="mt-4">
      {{ error }}
    </v-alert>
  </v-container>
</template>

<script>
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

export default {
  data() {
    return {
      activeTab: 0,
      worksheets: [],
      error: null,
    };
  },
  created() {
    this.loadDataFromExcel();
  },
  methods: {
    async loadDataFromExcel() {
      try {
        // Fetch the Excel file from the backend
        await this.$store.dispatch('fetchExcelFile');
        const workbook = this.$store.state.workbook;

        // Process each worksheet
        this.worksheets = workbook.SheetNames.map((name, index) => {
          console.log(index)
          const worksheet = workbook.Sheets[name];
          const data = XLSX.utils.sheet_to_json(worksheet);
          const headers = Object.keys(data[0]).map((key) => ({
            text: key,
            value: key,
            selected: true,
            filterable: true,
            sortable: true,
          }));

          return {
            name,
            data,
            headers,
            loading: false,
            page: 1,
            itemsPerPage: 10,
            pageCount: 0,
            sortBy: null,
            sortDesc: false,
            search: '',
          };
        });
      } catch (error) {
        this.error = 'Error loading Excel file from the backend.';
        console.error(error);
      }
    },
    printPdf() {
      try {
        // Get the workbook from the Vuex store
        // const workbook = this.$store.state.workbook;

        // Get the selected worksheet
        const selectedWorksheet = this.worksheets[this.activeTab];

        // Get the selected columns
        const selectedColumns = selectedWorksheet.headers.filter((header) => header.selected);

        // Rename the column names
        const columnNames = {
          'Dates': 'Trade Date',
          'Full name': 'Name',
        };

        // Extract the data for the selected columns
        const data = selectedWorksheet.data.map((row) => {
          return selectedColumns.map((column) => row[column.value]);
        });

        // Create a new PDF document
        const doc = new jsPDF();

        // Add the data to the PDF
        doc.autoTable({
          head: [selectedColumns.map((column) => columnNames[column.text] || column.text)],
          body: data,
          columnStyles: selectedColumns.reduce((styles, column) => {
            styles[column.value] = { columnWidth: 'auto' };
            return styles;
          }, {}),
        });

        // Download the PDF
        doc.save(`${selectedWorksheet.name}.pdf`);
      } catch (error) {
        this.error = 'Error generating PDF. Please try again.';
        console.error(error);
      }
    },
    filteredData(worksheet) {
      return worksheet.data.filter((row) => {
        return Object.values(row).some((value) =>
          value.toString().toLowerCase().includes(worksheet.search.toLowerCase())
        );
      }).sort((a, b) => {
        if (worksheet.sortBy === null) return 0;
        const modifier = worksheet.sortDesc ? -1 : 1;
        if (a[worksheet.sortBy] < b[worksheet.sortBy]) return -1 * modifier;
        if (a[worksheet.sortBy] > b[worksheet.sortBy]) return 1 * modifier;
        return 0;
      }).slice((worksheet.page - 1) * worksheet.itemsPerPage, worksheet.page * worksheet.itemsPerPage);
    },
  },
};
</script>