# Flask + Vue.js + MongoDB CRUD Application

This project is a full-stack CRUD application using Flask (backend), Vue.js (frontend), and MongoDB as the database. It allows users to manage a collection of users with functionalities to create, read, update, and delete (CRUD) users.

## Prerequisites

Before running the project, ensure you have the following installed:

- [Python](https://www.python.org/downloads/) (version 3.8 or higher)
- [Node.js](https://nodejs.org/) (version 16 or higher)
- [MongoDB](https://www.mongodb.com/try/download/community) (ensure MongoDB service is running)

## 1. Setup and Run the Backend (Flask API)

1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. Create and activate a virtual environment:
   - On Windows (PowerShell):
     ```sh
     python -m venv venv
     venv\Scripts\Activate
     ```
   - On macOS/Linux:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Flask API:
   ```sh
   python app.py
   ```
   The API should now be running at `http://127.0.0.1:5000/`

## 2. Setup and Run the Frontend (Vue.js Client)

1. Navigate to the frontend directory:
   ```sh
   cd create-vue
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Run the development server:
   ```sh
   npm run dev
   ```
   The frontend should now be running at `http://localhost:5173/`

## 3. Import JSON Data into MongoDB

1. Ensure the MongoDB service is running:
   - On Windows (PowerShell):
     ```sh
     mongod
     ```
   - On macOS/Linux:
     ```sh
     sudo systemctl start mongod
     ```
2. Run the parser script to import the JSON data:
   ```sh
   python parser.py
   ```

## 4. Running the Project

Once both the backend and frontend are running, open `http://localhost:5173/` in your browser to use the application.

## 5. API Endpoints

The Flask backend provides the following API endpoints:

- `GET /users` - Retrieve all users
- `POST /users` - Create a new user
- `GET /users/<username>` - Retrieve a specific user
- `PUT /users/<username>` - Update an existing user
- `DELETE /users/<username>` - Delete a user

## 6. Notes

- Ensure MongoDB is running before starting the backend.
- The frontend communicates with the backend at `http://127.0.0.1:5000/`.
- If any dependency issues occur, verify the installed versions of Python, Node.js, and MongoDB.
