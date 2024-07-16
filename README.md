# kic-vue-python

## Introduction
This project is a web application built with Vue.js (with Vuetify for UI components) as the front end and Python-Flask as the backend. For database I have used SQLAlchemy.


The application allows users to upload an Excel file, display its content in a tabular format, and perform operations such as saving the data to a database and generating PDFs.



## Installation

### Backend
1. Navigate to the backend directory:
    ```
    cd backend
    ```

2. Create a virtual environment:
    ```
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```
        venv\Scripts\activate
        ```

        OR

        ```
        source venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```
        source venv/bin/activate
        ```

4. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

5. Run the Flask server:
    ```
    python app.py
    ```

### Frontend
1. Navigate to the frontend directory:
    ```
    cd frontend
    ```

2. Install vue.js dependencies:
    ```
    npm install
    ```

3. Run the Vue.js development server:
    ```
    npm run serve
    ```

## Usage
1. Access the application:
    - Open your web browser and navigate to http://localhost:8080/dist/#.

2. Login or Register:
    - Use the provided login or registration forms to access the dashboard.

3. Read a Excel File:
    - On the dashboard, read an Excel file using the file input.

4. View Data:
    - The data from the Excel file will be displayed in tabs and tables based on the sheet names.

5. Generate PDF:
    - Use the "Print" button to generate a PDF of the table data with selected columns.
	
6. Users Page

7.  #### Default admin login
    - admin_email = 'admin@kic.com' / password = 'kic_admin12'
    = On registration users will be created with role 'user'.
    - admin can access all users profile.
    - User can edit only own record.



## Additional Notes
- Ensure that you have Python 3.x and Node.js installed on your system.
- For the Flask backend, make sure to set up a virtual environment to manage dependencies.
- Vue.js frontend requires Node.js and npm for package management and development server.

---

This documentation provides a comprehensive guide to setting up and running the project, including detailed steps for both backend and frontend development. If you have any questions or need further assistance, please refer to the official documentation of the respective frameworks or reach out to the project maintainers.

