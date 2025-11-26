![alt text](image.png)

---

## 1. Assignment Details

| Field                 | Information                                                           |
| :-------------------- | :-------------------------------------------------------------------- |
| **Course Code:**      | DBAS 3200                                                             |
| **Course Name:**      | Data-Driven Application Programming                                   |
| **Instructor:**       | Davis Boudreau                                                        |
| **Assignment Title:** | Mini-Project 0 — Dockerized Django + PostgreSQL Environment (“myapp”) |
| **Assignment Type:**  | Foundational Mini-Project (Individual)                                |
| **Version:**          | 1.1  (Updated for PostgreSQL Integration)                             |
| **Last Updated:**     | Fall 2025                                                             |
| **Estimated Time:**   | 8–10 hours                                                            |
| **Pre-Requisites:**   | Python, SQL, Docker, VS Code, Git basics                              |
| **Due Date:**         | (Insert)                                                              |
| **Weight:**           | 10 %                                                                  |

---

## 2. Overview / Purpose / Objectives

### **Purpose**

You’ll build a **fully containerized Django web app** (“`myapp`”) that connects to a **PostgreSQL database** using Docker and Compose.
This project forms the technical foundation for later DBAS 3200 mini-projects involving data models, APIs, and reports.

### **Why This Matters**

Industry teams deploy database-driven back-ends inside containers for **consistency, scalability, and reliability**.
By mastering Docker + Django + Postgres now, you’ll be prepared to develop, migrate, and deploy complex data-driven systems confidently.

### **Objectives**

1. Configure and run Django + Postgres in Docker Compose.
2. Secure environment variables using `.env`.
3. Automate build / run tasks with a Makefile.
4. Render dynamic HTML templates using Django.
5. Reflect on how containers, databases, and frameworks interact.

---

## 3. Learning Outcomes Addressed

* Implement and deploy a data-driven web application in containers.
* Use Django ORM with PostgreSQL.
* Apply DevOps automation and configuration management.
* Explain connections between application, database, and environment layers.

---

## 4. Pre-Requisites (Expanded with Context)

| Area                             | Skills & Context                                                        |
| -------------------------------- | ----------------------------------------------------------------------- |
| **CLI & Git**                    | Navigate, commit, and manage project files.                             |
| **Python & Django**              | Understand project vs app structure, views, urls.                       |
| **SQL Fundamentals**             | Basic DDL/DML, relational schemas (PostgreSQL focus).                   |
| **Docker Basics**                | Difference between image, container, volume, network.                   |
| **Docker Compose**               | Multi-service coordination (app + db).                                  |
| **Make Utility**                 | Simplify repeated commands via targets.                                 |
| **Environment Variables (.env)** | Store credentials and config outside code for security and flexibility. |

---

## 5. Assignment Description / Use Case

You’ll create `myapp`, a minimal Django project with a PostgreSQL backend, all orchestrated through Docker Compose.
It displays a simple home page (“Hello from myapp”) using Django templates.
This structure becomes your base for future projects (Event Management, APIs, Reports).

---

## 6. Tasks / Instructions — Step by Step

Each step includes **What / Why / How** for clarity.

---

### **Step 0 — Initialize Project**

**What:** Create a clean folder.
**Why:** Defines Docker build context and keeps organization clean.
**How:**

```bash
mkdir myapp && cd myapp
```

---

### **Step 1 — requirements.txt**

**What:** List dependencies.
**Why:** Pin packages for consistent builds.
**How:**

```txt
Django>=5.0,<6.0
gunicorn>=21.2
psycopg2-binary>=2.9
```

---

### **Step 2 — .dockerignore**

**What:** Exclude unneeded files from the build context.
**Why:** Smaller, faster images.
**How:**

```
__pycache__/
*.pyc
*.sqlite3
*.log
.env
.git
.gitignore
media/
staticfiles/
```

---

### **Step 3 — .gitignore**

**What:** Prevent temporary files from being tracked by Git.
**Why:** Keeps repo clean and secure.
**How:** `.gitignore`

```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.log
*.sqlite3

# Virtual Environments
venv/
env/

# Django Static and Media
media/
staticfiles/

# Docker
*.pid
*.tar
*.bak
*.swp
.env

# IDE files
.vscode/
.idea/
.DS_Store
```

---

### **Step 4 — .env**

**What:** Configuration for environment variables.
**Why:** Central place for sensitive info (e.g., DB credentials).
**How:** `.env`

```bash
# Django
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=*
DJANGO_SECRET_KEY=change_me_please

# Postgres
POSTGRES_DB=myapp_db
POSTGRES_USER=myapp_user
POSTGRES_PASSWORD=myapp_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

### **Step 5 — Dockerfile**

**What:** Blueprint for building the web app image.
**Why:** Ensures every student and system runs the same stack.
**How:**

```Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

### **Step 6 — docker-compose.yml**

**What:** Orchestrates the web and database containers.
**Why:** Compose creates a shared network and persistent volume for Postgres.
**How:**

```yaml
services:
  db:
    image: postgres:16
    container_name: myapp_db
    env_file:
      - .env
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    container_name: myapp_web
    env_file:
      - .env
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  pgdata:
```

---

### **Step 7 — Makefile**

**What:** Simplifies frequent commands and loads `.env`.
**Why:** Improves efficiency and standardization.
**How:**

```Makefile
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: build up down logs shell migrate makemigrations superuser clean

build:
\tdocker compose build

up:
\tdocker compose up

down:
\tdocker compose down

logs:
\tdocker compose logs -f

shell:
\tdocker compose run --rm web bash

migrate:
\tdocker compose run --rm web python manage.py migrate

makemigrations:
\tdocker compose run --rm web python manage.py makemigrations

superuser:
\tdocker compose run --rm web python manage.py createsuperuser

clean:
\tdocker compose down -v --remove-orphans
\tdocker system prune -f
```

---

### **Step 8 — Create Django Project**

```bash
docker compose run --rm web django-admin startproject myapp .
```

---

### **Step 9 — Update settings.py for PostgreSQL**

**What:** Use .env variables to configure database.
**Why:** Makes the app portable and secure.
**How:**

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DJANGO_DEBUG") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "changeme")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
    }
}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

---

### **Step 10 — Migrate Database**

```bash
make migrate
```

---

### **Step 11 — Run Application**

```bash
make up
```

Visit **[http://localhost:8000](http://localhost:8000)**

---

### **Step 12 — Create App**

```bash
mkdir -p apps
docker compose run --rm web python manage.py startapp myapp apps/myapp
```

In `settings.py`:

```python
INSTALLED_APPS += ['apps.myapp']
```

---

### **Step 13 — Templates (HTML)**

See **Templates — What / Why / How** below for detailed steps to create `base.html` and `home.html`.

---

### **Step 14 — Superuser (optional)**

```bash
make superuser
```

---

### **Step 15 — Production Mode (optional)**

Replace the runserver command with Gunicorn:

```yaml
command: gunicorn myapp.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Use only with `DEBUG=0` and proper static file serving.

---

## 7. Templates (HTML) — What / Why / How

### **T1 — Templates Folder**

In `settings.py`:

```python
'DIRS': [BASE_DIR / 'templates'],
```

---

### **T2 — Base Layout**

`templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}myapp{% endblock %}</title>
</head>
<body>
  <header><h1><a href="/">myapp</a></h1></header>
  <main>{% block content %}{% endblock %}</main>
  <footer><small>&copy; 2025 myapp</small></footer>
</body>
</html>
```

---

### **T3 — Home Template**

`templates/home.html`

```html
{% extends "base.html" %}
{% block title %}Home · myapp{% endblock %}
{% block content %}
  <h2>Welcome to myapp</h2>
  <p>{{ message }}</p>
{% endblock %}
```

---

### **T4 — View & URL**

`apps/myapp/views.py`

```python
from django.shortcuts import render
def home(request):
    return render(request, "home.html", {"message": "Hello from myapp with PostgreSQL!"})
```

`myapp/urls.py`

```python
from django.contrib import admin
from django.urls import path
from apps.myapp.views import home
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
]
```

---

## 8. Final Folder Structure

```
myapp/
├─ .env
├─ .gitignore
├─ .dockerignore
├─ Dockerfile
├─ docker-compose.yml
├─ Makefile
├─ requirements.txt
├─ manage.py
├─ myapp/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ apps/
│  ├─ __init__.py
│  └─ myapp/
│     ├─ __init__.py
│     ├─ views.py
│     ├─ models.py
│     ├─ admin.py
│     └─ migrations/
│        └─ __init__.py
├─ templates/
│  ├─ base.html
│  └─ home.html
└─ static/
   └─ css/
      └─ styles.css
```

---

## 9. Deliverables

Submit ZIP named:

```
studentid_dbas3200_MP0_django-docker.zip
```

Include all files and a **README.md** explaining:

* How to build and run (`make build → make up`)
* Purpose of `.env`, Dockerfile, Makefile
* Reflection answers (Section 10)

---

## 10. Reflection & Takeaways (Thinking Tasks)

Students must answer in their README (150–300 words total):

1. **Environment Design:** How does Docker improve the consistency of a data-driven application team?
2. **Database Integration:** What advantages does PostgreSQL bring over SQLite for multi-user projects?
3. **Configuration:** Why should database credentials and keys be stored in `.env` and not committed to Git?
4. **Automation:** In what ways does the Makefile simplify the developer workflow?
5. **Next Step:** How might this environment support future assignments that use models, API routes, or analytics?

---

## 11. Assessment Rubric (10 pts)

| Criterion                       | Exceeds (A)                                               | Meets (B)              | Developing (C) | Not Attempted (0) |
| ------------------------------- | --------------------------------------------------------- | ---------------------- | -------------- | ----------------- |
| **Docker + Postgres Setup (3)** | Builds, runs, migrates successfully with .env integration | Runs with minor issues | Partial setup  | Fails to run      |
| **Django Structure (2)**        | Proper project/app structure                              | Mostly correct         | Incomplete     | Missing           |
| **Makefile Automation (2)**     | All targets functional and .env loaded                    | Basic targets work     | Limited use    | Missing           |
| **Templates (2)**               | Base + Home pages render with dynamic data                | Functional HTML        | Incomplete     | Missing           |
| **Reflection (1)**              | Insightful and connected to learning outcomes             | Adequate               | Minimal        | Missing           |

---

## 12. Submission Guidelines

Submit your ZIP through Brightspace before the deadline.
Ensure the project runs locally with:

```bash
make build
make migrate
make up
```

---

## 13. Resources / Equipment

* **Software:** Docker Desktop, PostgreSQL image, VS Code.
* **Hardware:** ≥ 8 GB RAM.
* **References:**

  * [Django Docs](https://docs.djangoproject.com/)
  * [Docker Compose Docs](https://docs.docker.com/compose/)
  * [PostgreSQL Docs](https://www.postgresql.org/docs/)
  * [GNU Make Manual](https://www.gnu.org/software/make/manual/make.html)

---

## 14.


Excellent — adding PostgreSQL makes this a complete *real-world backend foundation* for DBAS 3200, and `.gitignore` is essential for good professional hygiene.

Here’s your **final integrated version** — fully rewritten, cohesive, and classroom-ready for upload to Brightspace.
It includes all sections (assignment, PostgreSQL integration, templates, folder structure, reflections, rubric, `.gitignore`, and Makefile improvements).

---

# 🧱 **DBAS 3200 – Mini-Project 0: Dockerized Django + PostgreSQL Application (“myapp”)**

## 1. Assignment Details

| Field                 | Information                                                           |
| :-------------------- | :-------------------------------------------------------------------- |
| **Course Code:**      | DBAS 3200                                                             |
| **Course Name:**      | Data-Driven Application Programming                                   |
| **Instructor:**       | Davis Boudreau                                                        |
| **Assignment Title:** | Mini-Project 0 – Dockerized Django + PostgreSQL Environment (“myapp”) |
| **Assignment Type:**  | Foundational Mini-Project (Individual)                                |
| **Version:**          | 1.2 (PostgreSQL Enhanced)                                             |
| **Last Updated:**     | Fall 2025                                                             |
| **Estimated Time:**   | 8–10 hours                                                            |
| **Pre-Requisites:**   | Python, SQL, Docker, VS Code, Git                                     |
| **Weight:**           | 10 %                                                                  |
| **Due Date:**         | (fill in)                                                             |

---

## 2. Overview / Purpose / Objectives

### Purpose

You’ll build a **fully containerized Django web application** that connects to a **PostgreSQL database** using Docker and Compose. This provides the base environment for all future DBAS 3200 mini-projects.

### Why This Matters

Developers and DevOps teams deploy database-backed apps in containers for consistency, scalability, and reproducibility. Learning Docker + Django + Postgres sets the foundation for production-ready data systems.

### Objectives

1. Configure and run Django + PostgreSQL in Docker Compose.
2. Manage environment variables securely via `.env`.
3. Automate build and run tasks using a Makefile.
4. Implement HTML templates in Django.
5. Reflect on containerization, database connectivity, and workflow automation.

---

## 3. Learning Outcomes Addressed

* Deploy a data-driven web application using Docker and PostgreSQL.
* Use Django ORM for database operations.
* Apply DevOps automation concepts.
* Explain links between frameworks, databases, and containers.

---

## 4. Pre-Requisites (Expanded)

| Area                      | Context                                  |
| ------------------------- | ---------------------------------------- |
| **CLI + Git**             | Navigate, commit, run terminal commands. |
| **Python + Django**       | Understand project vs app structure.     |
| **SQL (Postgres)**        | DDL/DML, primary keys, relations.        |
| **Docker Concepts**       | Images, containers, volumes, ports.      |
| **Compose**               | Manages multi-service stacks (app + db). |
| **Make Utility**          | Automates repetitive tasks.              |
| **Environment Variables** | Store config and secrets outside code.   |

---

## 5. Assignment Description / Use Case

Create `myapp`, a Django project running in Docker with PostgreSQL as its database. The homepage renders via Django templates and this architecture will extend into MP1–MP3 projects.

---

## 6. Tasks / Instructions (What / Why / How)

### Step 0 – Project Setup

**What:** Create a clean project folder.
**Why:** Defines Docker context and keeps organization clean.
**How:**

```bash
mkdir myapp && cd myapp
```

---

### Step 1 – requirements.txt

**What:** Dependency list. **Why:** Reproducible builds.

```txt
Django>=5.0,<6.0
gunicorn>=21.2
psycopg2-binary>=2.9
```

---

### Step 2 – .dockerignore

Exclude unnecessary files for smaller images.

```
__pycache__/
*.pyc
*.sqlite3
*.log
.env
.git
.gitignore
media/
staticfiles/
```

---

### Step 3 – .gitignore

Prevent temporary and sensitive files from Git.

```
__pycache__/
*.pyc
*.log
venv/
env/
media/
staticfiles/
.env
.vscode/
.idea/
.DS_Store
```

---

### Step 4 – .env

**What:** Environment configuration.
**Why:** Separates code from secrets and infrastructure.

```bash
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=*
DJANGO_SECRET_KEY=change_me_please

POSTGRES_DB=myapp_db
POSTGRES_USER=myapp_user
POSTGRES_PASSWORD=myapp_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

### Step 5 – Dockerfile

**What:** Build definition for the web service.
**Why:** Creates consistent Django runtime.

```Dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

### Step 6 – docker-compose.yml

**What:** Defines both database and web services.
**Why:** Compose links containers on a shared network.

```yaml
services:
  db:
    image: postgres:16
    container_name: myapp_db
    env_file: .env
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    container_name: myapp_web
    env_file: .env
    depends_on:
      - db
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"

volumes:
  pgdata:
```

---

### Step 7 – Makefile (with .env support)

**What:** Automates workflow commands. **Why:** Saves time and prevents errors.

```Makefile
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: build up down logs shell migrate makemigrations superuser clean

build:
\tdocker compose build

up:
\tdocker compose up

down:
\tdocker compose down

logs:
\tdocker compose logs -f

shell:
\tdocker compose run --rm web bash

migrate:
\tdocker compose run --rm web python manage.py migrate

makemigrations:
\tdocker compose run --rm web python manage.py makemigrations

superuser:
\tdocker compose run --rm web python manage.py createsuperuser

clean:
\tdocker compose down -v --remove-orphans
\tdocker system prune -f
```

---

### Step 8 – Initialize Django Project

```bash
docker compose run --rm web django-admin startproject myapp .
```

---

### Step 9 – Configure settings.py (for Postgres)

```python
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DJANGO_DEBUG") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "changeme")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
    }
}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

---

### Step 10 – Apply Migrations

```bash
make migrate
```

---

### Step 11 – Run and Verify

```bash
make up
```

Visit **[http://localhost:8000](http://localhost:8000)**

---

### Step 12 – Create App

```bash
mkdir -p apps
docker compose run --rm web python manage.py startapp myapp apps/myapp
```

In `settings.py`:

```python
INSTALLED_APPS += ['apps.myapp']
```

---

### Step 13 – Templates (HTML)

Add `templates/base.html` and `templates/home.html`.

#### base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}myapp{% endblock %}</title>
</head>
<body>
  <header><h1><a href="/">myapp</a></h1></header>
  <main>{% block content %}{% endblock %}</main>
  <footer><small>&copy; 2025 myapp</small></footer>
</body>
</html>
```

#### home.html

```html
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block content %}
  <h2>Welcome to myapp</h2>
  <p>{{ message }}</p>
{% endblock %}
```

#### views.py

```python
from django.shortcuts import render
def home(request):
    return render(request, "home.html", {"message": "Hello from myapp with PostgreSQL!"})
```

#### urls.py

```python
from django.contrib import admin
from django.urls import path
from apps.myapp.views import home
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
]
```

---

### Step 14 – (Option) Create Superuser

```bash
make superuser
```

---

### Step 15 – (Option) Production Command

```yaml
command: gunicorn myapp.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

---

## 7. Final Folder Structure

```
myapp/
├─ .env
├─ .gitignore
├─ .dockerignore
├─ Dockerfile
├─ docker-compose.yml
├─ Makefile
├─ requirements.txt
├─ manage.py
├─ myapp/
│  ├─ settings.py
│  ├─ urls.py
│  └─ ...
├─ apps/
│  └─ myapp/
│    ├─ views.py
│    └─ migrations/
├─ templates/
│  ├─ base.html
│  └─ home.html
└─ static/
   └─ css/styles.css
```

---

## 8. Deliverables

Submit:

```
studentid_dbas3200_MP0_django-docker.zip
```

Include all project files and a **README.md** with answers to reflection questions.

---

## 9. Reflection & Takeaways

Answer briefly (150–300 words):

1. How does Docker ensure consistency across development machines?
2. What benefits does PostgreSQL offer over SQLite in multi-user apps?
3. Why should environment variables like passwords stay outside source control?
4. What value does a Makefile bring to team collaboration?
5. How will this setup support future DBAS 3200 projects involving ORM and APIs?

---

## 10. Rubric (10 points)

| Criterion                   | Exceeds (A)                        | Meets (B)       | Developing (C) | Not Attempted (0) |
| :-------------------------- | :--------------------------------- | :-------------- | :------------- | :---------------- |
| Docker + Postgres Setup (3) | Runs cleanly; .env integrated      | Minor issues    | Partial        | Fails             |
| Django Structure (2)        | Proper project/app organization    | Mostly correct  | Incomplete     | Missing           |
| Makefile Automation (2)     | Targets fully working, .env loaded | Core targets ok | Limited        | Missing           |
| Templates (2)               | Base + Home pages render properly  | Functional      | Partial        | Missing           |
| Reflection (1)              | Insightful and technical           | Adequate        | Minimal        | Missing           |

---

## 11. Submission Guidelines

* Upload ZIP to Brightspace by deadline.
* Confirm the project runs:

```bash
make build
make migrate
make up
```

---

## 12. Resources

* **Software:** Docker Desktop, Postgres 16 image, VS Code.
* **Docs:** [Django](https://docs.djangoproject.com/) | [Docker](https://docs.docker.com/) | [Compose](https://docs.docker.com/compose/) | [PostgreSQL](https://www.postgresql.org/docs/) | [GNU Make](https://www.gnu.org/software/make/manual/make.html)

---

## 13. Academic Policies

Follow NSCC academic integrity guidelines. Cite any borrowed code or templates.

---

