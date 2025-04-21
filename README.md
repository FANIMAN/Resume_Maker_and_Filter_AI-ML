# Resume Ranker

**Brief Description of Your Project**  
Resume Ranker is a web application designed to rank resumes based on their content. It processes resumes and evaluates them based on specific criteria to provide a ranking score. This project leverages on analysis and ranking, with an intuitive FastAPI backend and PostgreSQL for data storage.

---

## 1. **Clone the Repository**

1. Navigate to the project folder.
2. To zip the project folder, use the following command:
    ```bash
    zip -r project_name.zip .
    ```

---

## 2. **Set up a Virtual Environment** *(Optional but recommended for Python projects)*

1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```
2. Activate the virtual environment:
    ```bash
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

---

## 3. **Install Dependencies**

Install the necessary Python dependencies:
```bash
pip install -r requirements.txt
```

---

## 4. **Set up Docker** *(Optional)*

If you are using Docker, follow these steps to build and start the web application and the database:

```bash
docker-compose up --build
```

This will build the Docker images and start both the web application and the database.

---

## 5. **Set up Environment Variables**

Create a `.env` file in the root directory with the following variables:

```env
postgres_user=your_db_user
postgres_password=your_db_password
postgres_db=your_db_name
DATABASE_URL=db_url
```

---

## 6. **Access the App**

Once everything is set up, you can access the app:

- **For local development**: [http://localhost:8000](http://localhost:8000)
- **For Docker**: [http://localhost:8000](http://localhost:8000)

---

## How to Run the App

### Method 1: **With Uvicorn** *(using a virtual environment)*

1. Activate the virtual environment (if using one).
2. Run the FastAPI app with Uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```
    Or to bind to `0.0.0.0` on port `8000`:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
    This will start the app at [http://localhost:8000](http://localhost:8000).

---

### Method 2: **With Docker**

To run the app with Docker, use the following command:
```bash
docker-compose up
```
This will start the application along with the PostgreSQL container. The app will be accessible at [http://localhost:8000](http://localhost:8000).

---

## How to Run the Tests

To run the tests, follow these steps:

1. Install the test dependencies (if any):
    ```bash
    pip install -r requirements.txt
    ```

2. Run the tests with `pytest`:
    ```bash
    pytest
    ```

Or, for a custom environment:
```bash
PYTHONPATH=.:$PYTHONPATH pytest tests
```

This will execute the tests and show the results in the terminal.

---

## Notes on What Works, What Doesn’t, and What You’d Improve with More Time

### What Works:
- The FastAPI app is running and serving endpoints.
- PostgreSQL integration is set up using Docker.
- API documentation is accessible via Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs).

### What Doesn’t Work:
- AI models require a subscription and key access to function properly. Currently, these keys are not integrated, so the models are not operational.
  
### What You’d Improve with More Time:
- **AI Model Integration**: With more time, I would integrate the AI models with proper subscription keys and ensure that the AI evaluation can rank resumes more accurately. I would also work on implementing caching and performance improvements for the AI model calls.

- **User Authentication and Roles**: Implement a more robust authentication and role management system, allowing only authorized users (e.g., admins) to access certain features.

- **UI Improvements**: If given more time, I would work on enhancing the frontend user experience by adding more features, improving the design, and ensuring it is mobile-responsive.

---

## Additional Notes

- **Docker**: Ensure Docker and Docker Compose are installed on your machine before attempting to use the Docker setup.

