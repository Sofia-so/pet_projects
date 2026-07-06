# Flask Diary Web Application

[![Tests](https://github.com/Sofia-so/pet_projects/actions/workflows/tests.yml/badge.svg)](https://github.com/Sofia-so/pet_projects/actions/workflows/tests.yml)

A simple web application for managing diaries and notes built with Flask.

## Tech Stack
- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Alembic
- Flask-Login
- Jinja2
- HTML
- Git
- Pytest
- GitHub Actions

## Features

-  User registration and authentication (Flask-Login)
-  User profile management (edit, delete account)
-  Diary management system
-  CRUD operations for notes (create, read, update, delete)
-  One-to-Many relationships (User → Diaries → Notes)
-  PostgreSQL database integration via SQLAlchemy ORM
-  Database migrations using Alembic
-  Data validation and error handling
-  HTML templates with Jinja2
-  Automated tests with Pytest and Flask Test Client
 
 ## Continuous Integration
 
The project uses GitHub Actions to:
- automatically install dependencies;
- run Alembic database migrations;
- execute the Pytest test suite;
- verify every push and pull request.

## Database Diagram

![Database Diagram](docs/erd.png)

## Project Purpose

This project was created to practice backend development with Flask, including authentication, database design, and testing.

## Getting Started

### Clone the repository

```bash
git clone https://github.com/Sofia-so/pet_projects.git
cd pet_projects
```

### Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file based on `.env.example`.

### Apply database migrations

```bash
alembic upgrade head
```

### Run the application

```bash
flask --app app:create_app --debug run
```

## License

No license has been specified for this project.
---

##  Author

**Sofia Sudarkova**

GitHub: https://github.com/Sofia-so  
Email: sudarkovasofia0@gmail.com
