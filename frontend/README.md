# Privilege Log Portal - Frontend

## Overview
This is the frontend application for the Privilege Log Portal, built with **React**, **Vite**, and **TailwindCSS**. It provides an interface for uploading emails (`.eml`, `.txt`), viewing the AI-generated privilege analysis, and exporting the results as a CSV.

## Prerequisites
- Node.js (v18 or higher recommended)
- npm

## Setup & Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Development

To start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

> **Note**: This frontend expects the backend API to be running on `http://localhost:8000`. The Vite proxy is configured to forward requests from `/api` to the backend.

## Production Build

To build the application for production:

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.
