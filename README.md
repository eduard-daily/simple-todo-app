# Full-Stack To-Do List Application

A simple yet complete full-stack web application for managing a list of tasks. This project serves as a learning exercise covering frontend (React), backend (Python/FastAPI), database (PostgreSQL), and containerization (Docker).

## Features

* **View Tasks:** Display the current list of tasks.
* **Add Task:** Input field and button to add new tasks to the list.
* **Mark as Complete:** Toggle the completion status of a task using a checkbox.
* **Delete Task:** Remove tasks permanently from the list.
* **Persistence:** Tasks are stored in a PostgreSQL database. 

*(Potential Future Features: Edit task descriptions, due dates, filtering/sorting, user accounts, drag-and-drop reordering)* 

## Tech Stack

* **Frontend:** React (with Vite), JavaScript, CSS
* **Backend:** Python, FastAPI, SQLAlchemy (ORM)
* **Database:** PostgreSQL
* **API Communication:** RESTful API, JSON
* **Containerization:** Docker, Docker Compose

## Project Structure


todo-app/
├── backend/
│   ├── app/
│   │   ├── init.py
│   │   ├── main.py         # FastAPI app, endpoints, CORS, table creation
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   └── database.py     # Database connection setup
│   ├── Dockerfile          # Backend Docker image instructions
│   ├── requirements.txt    # Python dependencies
│   └── .env_backend_example # Example backend environment variables
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components (TaskList, TaskItem, AddTaskForm)
│   │   ├── App.jsx         # Main React app component (state, API calls)
│   │   └── main.jsx        # React entry point
│   ├── Dockerfile          # Frontend Docker image instructions (dev server)
│   ├── index.html          # Vite entry HTML
│   ├── package.json        # Node.js dependencies
│   ├── vite.config.js      # Vite configuration
│   └── .env.development    # Frontend environment variables (e.g., API URL)
│
├── docker-compose.yml      # Docker Compose configuration for all services
├── .gitignore              # Git ignore rules (node_modules, .env, etc.)
└── README.md               # This file


## Setup and Installation

Follow these steps to get the application running locally using Docker.

### Prerequisites

* **Docker:** Ensure Docker Desktop or Docker Engine is installed and running. ([Install Docker](https://docs.docker.com/get-docker/))
* **Docker Compose:** Usually included with Docker Desktop. If not, install it separately. ([Install Docker Compose](https://docs.docker.com/compose/install/))
* **Git:** For cloning the repository.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd todo-app
    ```

2.  **Configure Environment Variables:**

    * **Backend:** Navigate to the `backend/` directory. Copy the example `.env` file:
        ```bash
        # Make sure you are in the backend/ directory for this command
        cp .env_backend_example .env
        ```
        Edit the `backend/.env` file and set your desired PostgreSQL credentials. **Important:** Keep the database host as `db` as this is the service name within the Docker network.
        ```dotenv
        # backend/.env
        DATABASE_URL=postgresql://your_user:your_password@db:5432/your_db_name
        POSTGRES_USER=your_user
        POSTGRES_PASSWORD=your_password
        POSTGRES_DB=your_db_name
        ```

    * **Frontend:** Navigate to the `frontend/` directory. Create a `.env.development` file (or `.env`). Add the following line, ensuring it points to the *host* address where the backend is exposed by Docker:
        ```dotenv
        # frontend/.env.development
        VITE_API_BASE_URL=http://localhost:8000/api
        ```
        *(Note: The `.gitignore` file should prevent `.env` files from being committed.)*

3.  **Build and Run with Docker Compose:**
    Navigate back to the project root directory (`todo-app/`) where the `docker-compose.yml` file is located. Run:
    ```bash
    docker-compose up --build
    ```
    * `--build` forces Docker to build the images based on the Dockerfiles. You can omit it for subsequent runs if only code changes have been made.
    * This command will start the backend, frontend, and database containers. The first time it runs, it might take a while to download images and install dependencies.

4.  **Access the Application:**
    * **Frontend:** Open your web browser and navigate to `http://localhost:5173`
    * **Backend API Docs:** Access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`

5.  **Stopping the Application:**
    Press `Ctrl + C` in the terminal where `docker-compose up` is running. To remove the containers, run:
    ```bash
    docker-compose down
    ```
    To remove the containers *and* the database volume (deleting all task data), run:
    ```bash
    docker-compose down -v
    ```

## API Endpoints

The backend provides the following RESTful API endpoints under the `/api` prefix:

* `GET /tasks`: Retrieve all tasks.
* `POST /tasks`: Create a new task. (Body: `{"description": "string", "is_completed": boolean}`)
* `GET /tasks/{task_id}`: Retrieve a single task by ID.
* `PUT /tasks/{task_id}`: Update a task by ID. (Body: `{"description": "string", "is_completed": boolean}` - fields optional)
* `DELETE /tasks/{task_id}`: Delete a task by ID.

*(See `http://localhost:8000/docs` for detailed request/response schemas)*

---

*This README provides a comprehensive guide to understanding, setting up, and running the To-Do application.*
