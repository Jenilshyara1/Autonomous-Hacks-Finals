# Autonomous Hacks Finals - Project Setup

This documentation explains how to set up and run both the Backend and Frontend servers for the Autonomous Hacks Finals project.

## Prerequisites

- **Node.js** (v20.19+ or v22.12+ required)
- **Python** (v3.8+)
- **PostgreSQL** (installed and running)

## Key Features

- **AI-Powered Analysis**: Uses Google Gemini to automatically classify emails and generate privilege logs.
- **User Isolation**: Secure multi-user environment ensures data privacy.
- **Full Stack Architecture**: Interactive React frontend and robust FastAPI backend.
- **Dockerized**: Easy deployment with Docker Compose.

## System Architecture

See the [Flow Diagram](flow_diagram.md) for a visual overview of the processing pipeline.

## 1. Quick Start (Docker Compose)

The easiest way to run the entire application (Frontend + Backend + Database) is using Docker Compose.

1.  **Configure Environment**:
    - Ensure you have a `backend/.env` file with `GOOGLE_API_KEY`.

2.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```

- **Frontend**: `http://localhost:5173`
- **Backend API**: `http://localhost:8000`

---

## 2. Manual Backend Setup

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

## 3. Manual Frontend Setup

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

| Method | Command | Notes |
| :--- | :--- | :--- |
| **Docker** | `docker-compose up --build` | Runs everything |
| **Manual Backend** | `uvicorn app.main:app --reload` | Run in `backend/` dir |
| **Manual Frontend** | `npm run dev` | Run in `frontend/` dir |
