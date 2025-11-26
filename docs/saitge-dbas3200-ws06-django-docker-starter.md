![alt text](image.png)

---


## Workshop Details

| Field                | Information                                                  |
| :------------------- | :----------------------------------------------------------- |
| **Course**           | DBAS 3200 — Data-Driven Application Programming              |
| **Week**             | 6                                                            |
| **Workshop Title**   | Django Stack in Docker with PostgreSQL and pgAdmin           |
| **Instructor**       | Davis Boudreau                                               |
| **Estimated Time**   | 2.5 – 3 hours                                                |
| **Pre-Requisites**   | Completed MP1 (ORM CRUD project); Docker Desktop installed   |
| **Software / Tools** | VS Code, Docker Desktop, PostgreSQL 16, pgAdmin, Python 3.12 |

---

## 1  Workshop Overview

Students will:

1. Create a Dockerized development stack (Django + PostgreSQL + pgAdmin).
2. Fix the `manage.py` startup issue by bootstrapping the project inside the container correctly.
3. Connect Django to PostgreSQL via `.env` variables.
4. Verify the application via browser and pgAdmin.
5. Understand how this stack forms the foundation for a modular DAL and future REST integration.

---

## 2  Learning Outcomes Addressed

* **Outcome 2:** Create and manage a data connection.
* **Outcome 6:** Develop professional project setup and containerization.
* **Outcome 7:** Enhance portfolio with technical stack artifacts.
* **Outcome 1 (prep):** Prepare for ORM and DAL refactoring in Week 7.

---

## 3  Background Concepts

| Concept                  | Purpose                                                               |
| :----------------------- | :-------------------------------------------------------------------- |
| **Docker Compose**       | Runs multiple containers (web, db, pgAdmin) as a single stack.        |
| **Service names as DNS** | Inside Compose, `db` is the hostname Django uses to reach PostgreSQL. |
| **.env configuration**   | Separates secrets and ports from the Compose file.                    |
| **Health check**         | Delays Django start until the database is ready.                      |
| **Bind mounts**          | Share code between host and container for live editing in VS Code.    |

---

## 4  Activity Tasks / Instructions

### Step 0  Prepare Your Project Folder

1. Create a new folder:
   `mkdir django-wk6 && cd django-wk6`
2. Open it in VS Code.
3. Create the following files in the root.

---

### Step 1  Project Configuration Files

**`.env`**

```env
POSTGRES_DB=django_wk6
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
DB_HOST=db
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
PGADMIN_PORT=5050
DJANGO_SECRET_KEY=dev-secret-change-me
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=*
WEB_PORT=8000
```

**`requirements.txt`**

```txt
Django==5.1.1
psycopg2-binary==2.9.9
python-dotenv==1.0.1
```

**`Dockerfile`**

```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
```

**`docker-compose.yml`**

```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 3s
      retries: 30

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
    ports:
      - "${PGADMIN_PORT}:80"
    depends_on:
      - db

  web:
    build: .
    container_name: wk6_web
    command: bash -lc "test -f manage.py || django-admin startproject core . && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    environment:
      DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY}
      DJANGO_DEBUG: ${DJANGO_DEBUG}
      DJANGO_ALLOWED_HOSTS: ${DJANGO_ALLOWED_HOSTS}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_HOST: ${DB_HOST}
      POSTGRES_PORT: ${POSTGRES_PORT}
    volumes:
      - .:/app
    ports:
      - "${WEB_PORT}:8000"
    depends_on:
      db:
        condition: service_healthy

volumes:
  pg_data:
```

> **New fix:** The `test -f manage.py || django-admin startproject` line automatically creates the project inside `/app` if it doesn’t exist, preventing the “manage.py not found” error.

**`Makefile`**

```makefile
.PHONY: up down logs web makemigrations migrate createsuperuser

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

web:
	docker compose exec web bash

makemigrations:
	docker compose exec web python manage.py makemigrations

migrate:
	docker compose exec web python manage.py migrate

createsuperuser:
	docker compose exec web python manage.py createsuperuser
```

---

### Step 2  Start the Stack and Auto-Create the Project

Run:

```bash
make up
```

Docker will:

1. Build the web image.
2. Spin up PostgreSQL and pgAdmin.
3. Detect no `manage.py` → create the `core` project automatically.
4. Run migrations and start the server.

Check:

```bash
docker compose ps
docker compose logs -f web
```

→ should display: `Starting development server at http://0.0.0.0:8000/`.

---

### Step 3  Verify the Stack

* Browser → **[http://localhost:8000](http://localhost:8000)** → Django welcome page
* Browser → **[http://localhost:5050](http://localhost:5050)** → pgAdmin (login from `.env`)
  Add a server → Host = `db` → see `django_wk6` DB.

---

### Step 4  Add a Starter App

Inside the container:

```bash
make web
python manage.py startapp starter
```

**`starter/views.py`**

```python
from django.http import HttpResponse
def hello(request):
    return HttpResponse("Hello from Django in Docker 👋")
```

**`core/core/urls.py`**

```python
from django.contrib import admin
from django.urls import path
from starter.views import hello

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", hello),
]
```

Refresh → “Hello from Django in Docker 👋”.

---

### Step 5  Create Superuser and Check Admin

```bash
make createsuperuser
```

→ Visit **[http://localhost:8000/admin](http://localhost:8000/admin)** → login → confirm DB tables exist.

---

### Step 6  Concept Review and Next Steps

| Concept                | Why it Matters                                  |
| :--------------------- | :---------------------------------------------- |
| **Healthcheck**        | Prevents “DB not ready” errors during startup.  |
| **Bind Mount**         | Allows code editing in VS Code without rebuild. |
| **Environment Vars**   | Keeps credentials out of version control.       |
| **Service DNS**        | `db` is the hostname Django uses inside Docker. |
| **Auto-Bootstrap Fix** | Guarantees `manage.py` exists on first run.     |

---

## 5  Deliverables

* `.env`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `Makefile`
* Generated `core/` Django project + `starter/` app
* Screenshots: home page, pgAdmin database view, admin login
* Short README explaining how the auto-creation fix works

---

## 6  Reflection Questions

1. Why does Django connect to `db` instead of `localhost` inside Docker?
2. How does the healthcheck avoid the “DB connection refused” error?
3. What does the `test -f manage.py || django-admin startproject` command do?
4. Why store configuration in `.env` instead of hard-coding in `settings.py`?
5. How can this stack be extended to include a frontend or API?

---

## 7  Evaluation Criteria

| Category                       | Description                                            | Weight |
| :----------------------------- | :----------------------------------------------------- | :----: |
| **Stack Setup & Run**          | All containers build and run; Django home page visible |   40%  |
| **Fix Implementation**         | Auto-creation works; no `manage.py` errors             |   20%  |
| **Database Integration**       | pgAdmin connection verified                            |   20%  |
| **Documentation & Reflection** | Clear steps and answers                                |   20%  |

---
