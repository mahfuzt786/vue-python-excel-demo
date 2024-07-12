# kic-vue-python

## Introduction
This project is a web application built with Vue.js (with Vuetify for UI components) as the front end and Flask as the backend. 
The application allows users to upload an Excel file, display its content in a tabular format, and perform operations such as saving the data to a database and generating PDFs.

## Directory Structure

my-vue-flask-app/ 
├── backend/ 
│ ├── app.py 
│ ├── models.py 
│ ├── init.py 
│ └── venv/ 
├── frontend/
│ ├── node_modules/ 
│ ├── public/ 
│ ├── src/ 
│ │ ├── assets/ 
│ │ ├── components/ 
│ │ │ ├── AppMenu.vue 
│ │ │ ├── Login.vue 
│ │ │ └── Register.vue 
│ │ ├── router/ 
│ │ │ └── index.js 
│ │ ├── store/ 
│ │ │ └── index.js 
│ │ ├── views/ 
│ │ │ ├── Dashboard.vue 
│ │ │ └── Users.vue 
│ │ ├── App.vue 
│ │ ├── main.js 
│ │ └── vuetify.js 
│ ├── .gitignore 
│ ├── babel.config.js 
│ ├── package.json 
│ ├── README.md 
│ └── vue.config.js 
├── .gitignore 
└── README.md


## Installation

### Backend

1. **Navigate to the backend directory:**
    ```sh
    cd backend
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Create `requirements.txt` file with the following content:**
    ```txt
    Flask
    Flask-JWT-Extended
    Flask-SQLAlchemy
    pandas
    openpyxl
    fpdf
    ```

6. **Run the Flask server:**
    ```sh
    python app.py
    ```

### Frontend

1. **Navigate to the frontend directory:**
    ```sh
    cd frontend
    ```

2. **Install Node.js dependencies:**
    ```sh
    npm install
    ```

3. **Run the Vue.js development server:**
    ```sh
    npm run serve
    ```

## Usage

1. **Access the application:**
    - Open your web browser and navigate to `http://localhost:8080`.

2. **Login or Register:**
    - Use the provided login or registration forms to access the dashboard.

3. **Upload Excel File:**
    - On the dashboard, upload an Excel file using the file input.

4. **View Data:**
    - The Excel file's data will be displayed in a tabular format with sorting, pagination, filtering, and search capabilities.

5. **Save to Database:**
    - Click the "Save to Database" button to save the data to the database. The table name will be the same as the sheet name.

6. **Generate PDF:**
    - Click the "Print" button to generate a PDF. Check or uncheck the columns you want to include in the PDF.

## Notes

- Ensure your Flask server is running on `http://localhost:5000`.
- Ensure your Vue.js development server is running on `http://localhost:8080`.
- Adjust the URLs in the Axios requests if your servers are running on different ports or domains.

## Deployment

### Backend

1. **Install a production server (e.g., Gunicorn):**
    ```sh
    pip install gunicorn
    ```

2. **Run the server:**
    ```sh
    gunicorn -w 4 app:app
    ```

### Frontend

1. **Build the production files:**
    ```sh
    npm run build
    ```

2. **Serve the built files using a static file server or integrate with a backend server.**

## License
This project is licensed under the MIT License.

## Acknowledgements
- Flask
- Vue.js
- Vuetify
- Pandas
- FPDF


