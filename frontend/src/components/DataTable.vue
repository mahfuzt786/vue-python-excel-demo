<template>
    <v-card>
        <v-card-title>
            <v-row>
                <v-col cols="7">
                    <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                    @input="debouncedSearch"
                    ></v-text-field>
                </v-col>
                <v-col cols="2"></v-col>
                <v-col cols="3">
                    <v-btn align="right" color="primary" @click="printPdf()">
                        Print <v-icon right>mdi-printer</v-icon>
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-title>
        <v-data-table
            :headers="headers"
            :items="items"
            :options.sync="options"
            :server-items-length="totalItems"
            :loading="loading"
            :sort-desc.sync="sortDesc"
            :sort-by.sync="sortBy"
            @update:sortBy="updateSort"
            
        ></v-data-table>
    </v-card>
    
  </template>
  
<script>
  import axios from 'axios';
  import debounce from 'lodash/debounce';
  import jsPDF from 'jspdf';
    import 'jspdf-autotable';
  
  export default {
    props: ['sheet'],
    data() {
      return {
        headers: [],
        items: [],
        totalItems: 0,
        loading: true,
        search: '',
        options: {
          page: 1,
          itemsPerPage: 10,
          sortBy: [], // Initially empty for client-side sorting
          sortDesc: [], // Initially empty for client-side sorting
          filter: '',
        },
        sortBy: [], // Track current sortBy state
        sortDesc: [], // Track current sortDesc state
        debounceSearch: null,
      };
    },
    watch: {
      options: {
        handler() {
          this.fetchData();
        },
        deep: true,
      },
      sheet: {
        handler() {
          this.fetchData();
        },
      },
      search: {
            handler() {
                this.debouncedSearch();
            },
        },
    },
    methods: {
        printPDF() {
      const doc = new jsPDF();
      const table = this.$refs.dataTable.$el; // Reference to v-data-table DOM element

      // Generate PDF content
      doc.setFontSize(16);
      doc.text('Custom PDF Document', 15, 15);
      doc.autoTable({
        html: table,
        startY: 20,
      });

      // Save or open the PDF
      doc.save(`${this.sheet}.pdf`);
    },
      async fetchData() {
        this.loading = true;
        const { page, itemsPerPage, sortBy, sortDesc } = this.options;
        try {
          // Simulating API call for demonstration, but you can remove this if not needed
          const response = await axios.get(`http://127.0.0.1:8001/api/data`, {
            params: {
              sheet: this.sheet,
              page,
              itemsPerPage,
              sortBy: sortBy.length ? sortBy[0] : '',
              sortDesc: sortDesc.length ? sortDesc[0] : false,
              search: this.search,
            },
          });
          const responseData = response.data;
          console.log('Response:', responseData); // Log the response
          this.items = responseData.items || [];
          this.totalItems = responseData.total || 0;
          if (this.items.length > 0) {
            this.headers = Object.keys(this.items[0]).map(key => ({
              text: key,
              value: key,
            }));
          }
        } catch (error) {
          console.error('Error fetching data:', error);
        }
        this.loading = false;
      },
      updateSort(sortBy) {
        if (sortBy.length === 0) {
          this.sortBy = [];
          this.sortDesc = [];
        } else {
          this.sortBy = [sortBy[0]]; // Allow only one column sorting
          this.sortDesc = [this.options.sortDesc[0]]; // Preserve existing sortDesc
        }
      },
      debouncedSearch: debounce(function () {
            this.fetchData();
        }, 300),
    },
    mounted() {
      this.fetchData();
    },
  };
</script>
  