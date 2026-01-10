# Autonomous Hacks Finals - Project Setup

This documentation explains how to set up and run both the Backend and Frontend servers for the Autonomous Hacks Finals project.

## Prerequisites

- **Node.js** (v20.19+ or v22.12+ required)
- **Python** (v3.8+)
- **PostgreSQL** (installed and running)

## 1. Backend Setup

The backend is built with FastAPI and uses SQLAlchemy/Alembic for database management.

### Installation

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Create and activate a virtual environment:
    - **Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    - **Mac/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure environment variables:
    - Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        # Windows: copy .env.example .env
        ```
    - Open `.env` and fill in your `GOOGLE_API_KEY` and `DATABASE_URL`.

5.  Run database migrations:
    ```bash
    alembic upgrade head
    ```

### Running the Backend Server

Start the API server with hot-reload enabled:

```bash
uvicorn app.main:app --reload
```

- The API will be available at: `http://localhost:8000`
- API Documentation (Swagger UI): `http://localhost:8000/docs`

---

## 2. Frontend Setup

The frontend is a React application built with Vite and Tailwind CSS.

### Installation

1.  Open a new terminal and navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

### Running the Frontend Server

Start the development server:

```bash
npm run dev
```

- The application will be running at (usually): `http://localhost:5173`

## Summary of Commands

| Server | Terminal 1 (Backend) | Terminal 2 (Frontend) |
| :--- | :--- | :--- |
| **Directory** | `cd backend` | `cd frontend` |
| **Start** | `uvicorn app.main:app --reload` | `npm run dev` |
