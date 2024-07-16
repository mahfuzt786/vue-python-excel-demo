<template>
  <v-container fluid>
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
                    <!-- <v-btn align="right" color="primary" @click="printPdf()">
                        Print <v-icon right>mdi-printer</v-icon>
                    </v-btn> -->
                    <v-btn @click="showPrintDialog" color="primary">
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
            ref="dataTable"            
        ></v-data-table>
    </v-card>

    <!-- Print PDF Dialog -->
    <v-dialog v-model="printDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Print PDF</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="filter.fromDate"
                  label="From Date"
                  type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="filter.toDate"
                  label="To Date"
                  type="date"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="filter.portfolioNumber"
                  label="Portfolio Number"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="filter.shareSymbol"
                  label="Share Symbol"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="filter.securityCurrency"
                  label="Security Currency"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="printDialog = false">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="generatePdf">Generate PDF</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-overlay
      z-index=99
      :value="showLoading"
    >
      <v-row justify="center" align="center" style="height: 200px;">
        <v-progress-circular
          :size="70"
          :width="7"
          color="purple"
          indeterminate
        ></v-progress-circular>
      </v-row>
    </v-overlay>
  </v-container>
    
</template>
  
<script>
  import axios from 'axios';
  import debounce from 'lodash/debounce';
  import jsPDF from 'jspdf';
  import 'jspdf-autotable';
    // import html2canvas from 'html2canvas';
  
  export default {
    props: ['sheet'],
    data() {
      return {
        headers: [],
        items: [],
        totalItems: 0,
        loading: true,
        search: '',
        showLoading: false,
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
        sheet1Data: [],
        sheet2Data: [],
        sheet3Data: [],
        printDialog: false,
        filter: {
          fromDate: '',
          toDate: '',
          portfolioNumber: '',
          shareSymbol: '',
          securityCurrency: '',
        },
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
      fetchSheetData(sheetName) {
        return axios.get(`http://127.0.0.1:8001/api/data`, {
          params: {
            sheet: sheetName,
            page: 1,
            itemsPerPage: 10000, // Adjust as needed
            sortBy: '',
            sortDesc: false,
            search: '',
          },
        });
      },
      showPrintDialog() {
        this.printDialog = true;
      },
      async generatePdf() {
        this.printDialog = false;
        this.showLoading = true;

        try {
          const sheet1Response = await this.fetchSheetData('SECURITY_TRANSACTIONS');
          const sheet2Response = await this.fetchSheetData('SECURITY_MASTER');
          const sheet3Response = await this.fetchSheetData('SEC_ACC_MASTER');
          
          this.sheet1Data = sheet1Response.data.items;
          this.sheet2Data = sheet2Response.data.items;
          this.sheet3Data = sheet3Response.data.items;

          // Filter data based on input values
          const filteredSheet1Data = this.sheet1Data.filter(item => {
            // Convert all relevant fields to uppercase for comparison
            const itemTradeDate = item.TRADE_DATE ? item.TRADE_DATE.toUpperCase() : '';
            const itemSecurityAccount = item.SECURITY_ACCOUNT ? item.SECURITY_ACCOUNT.toUpperCase() : '';
            const itemSecurityNumber = item.SECURITY_NUMBER ? item.SECURITY_NUMBER.toUpperCase() : '';
            const itemSecurityCurrency = item.SECURITY_CURRENCY ? item.SECURITY_CURRENCY.toUpperCase() : '';

            // Convert filter inputs to uppercase for comparison
            const filterFromDate = this.filter.fromDate ? this.filter.fromDate.toUpperCase() : '';
            const filterToDate = this.filter.toDate ? this.filter.toDate.toUpperCase() : '';
            const filterPortfolioNumber = this.filter.portfolioNumber ? this.filter.portfolioNumber.toUpperCase() : '';
            const filterShareSymbol = this.filter.shareSymbol ? this.filter.shareSymbol.toUpperCase() : '';
            const filterSecurityCurrency = this.filter.securityCurrency ? this.filter.securityCurrency.toUpperCase() : '';

            // Parse TRADE_DATE to ensure correct comparison
            const itemDate = itemTradeDate ? new Date(itemTradeDate.split('-').reverse().join('-')) : null;
            const fromDate = filterFromDate ? new Date(filterFromDate) : null;
            const toDate = filterToDate ? new Date(filterToDate) : null;

            return (
              (!fromDate || (itemDate && itemDate >= fromDate)) &&
              (!toDate || (itemDate && itemDate <= toDate)) &&
              (!filterPortfolioNumber || (itemSecurityAccount && itemSecurityAccount.includes(filterPortfolioNumber))) &&
              (!filterShareSymbol || (itemSecurityNumber && itemSecurityNumber.includes(filterShareSymbol))) &&
              (!filterSecurityCurrency || (itemSecurityCurrency && itemSecurityCurrency.includes(filterSecurityCurrency)))
            );
          });

          console.log(filteredSheet1Data)

          const mappedData = filteredSheet1Data.map(item => {
            const account = this.sheet3Data.find(acc => acc.RECID === item.SECURITY_ACCOUNT);
            const security = this.sheet2Data.find(sec => sec.ID === item.SECURITY_NUMBER);
            return {
              TRADE_DATE: item.TRADE_DATE,
              SECURITY_ACCOUNT: item.SECURITY_ACCOUNT,
              SAM_NAME: account ? account.ACCOUNT_NAME : '',
              SECURITY_NUMBER: item.SECURITY_NUMBER,
              SECURITY_NAME: security ? security.SHORT_NAME : '',
              TRANS_TYPE: item.TRANS_TYPE,
              RECID: item.RECID,
              NO_NOMINAL: item.NO_NOMINAL,
              PRICE: item.PRICE,
              NET_AMT_TRADE: item.NET_AMT_TRADE,
              BROKER_COMMS: item.BROKER_COMMS,
              PROF_LOSS_SEC_CCY: item.PROF_LOSS_SEC_CCY,
            };
          });

          const pdf = new jsPDF('p', 'pt', 'a4');
          const pdfWidth = pdf.internal.pageSize.getWidth();
          let yOffset = 20;

          // Add PDF Header
          pdf.setFontSize(18);
          pdf.text(`Report`, pdfWidth / 2, yOffset, { align: 'center' });
          yOffset += 30;
          pdf.setFontSize(14);
          pdf.text(`FROM DATE: ${this.filter.fromDate}`, 20, yOffset);
          yOffset += 20;
          pdf.text(`TO DATE: ${this.filter.toDate}`, 20, yOffset);
          yOffset += 20;
          pdf.text(`PORTFOLIO NUMBER: ${this.filter.portfolioNumber}`, 20, yOffset);
          yOffset += 20;
          pdf.text(`SHARE SYMBOL: ${this.filter.shareSymbol}`, 20, yOffset);
          yOffset += 20;
          pdf.text(`SECURITY CURRENCY: ${this.filter.securityCurrency}`, 20, yOffset);
          yOffset += 30;

          // Add Table to PDF
          const headers = [
            'TRADE_DATE', 'SECURITY_ACCOUNT', 'SAM_NAME', 'SECURITY_NUMBER',
            'SECURITY_NAME', 'TRANS_TYPE', 'RECID', 'NO_NOMINAL', 'PRICE',
            'NET_AMT_TRADE', 'BROKER_COMMS', 'PROF_LOSS_SEC_CCY'
          ];
          const tableData = mappedData.map(item => headers.map(header => item[header]));

          pdf.autoTable({
            startY: yOffset,
            head: [headers],
            body: tableData,
            margin: { top: 10 },
            styles: {fontSize: 8},
          });

          pdf.save('reports.pdf');
          this.showLoading = false;

        } catch (error) {
          console.error('Error generating PDF:', error);
          this.showLoading = false;
        }
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
  