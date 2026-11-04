# 🎬 StreamPlus API

A modern, asynchronous RESTful API for **StreamPlus** — a video and movie streaming platform. Built with **FastAPI**, **SQLAlchemy (Async)**, and **Pydantic**, featuring dual-database support (PostgreSQL & SQLite), passwordless OTP authentication, JWT security, user watchlist management, catalog administration, and automated mock data generation.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Project Architecture](#-project-architecture)
- [Key Features](#-key-features)
- [File & Directory Structure](#-file--directory-structure)
- [Tech Stack](#-tech-stack)
- [Configuration & Environment Variables](#-configuration--environment-variables)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Server](#running-the-server)
- [API Documentation & Endpoints](#-api-documentation--endpoints)
  - [Core & System](#core--system)
  - [Authentication (`/api/v1/auth`)](#authentication-apiv1auth)
  - [User & Profile Management (`/api/v1/users`)](#user--profile-management-apiv1users)
  - [Movies Catalog (`/api/v1/movies`)](#movies-catalog-apiv1movies)
  - [Admin & Moderation (`/api/v1/admin`)](#admin--moderation-apiv1admin)
- [Database Models](#-database-models)
- [Mock Data Generation](#-mock-data-generation)
- [Deployment (Render)](#-deployment-render)
- [License](#-license)

---

## 🚀 Overview

StreamPlus API powers backend streaming operations:
- **Authentication**: Passwordless email OTP verification with JWT token pairs (access & refresh).
- **Dual-Database Architecture**: Zero-friction local development with SQLite (`aiosqlite`), seamless production scalability with PostgreSQL (`asyncpg`).
- **Streaming Catalog**: Comprehensive metadata modeling for movies, genres, ratings, cast, and custom alphanumeric movie identifiers (`stp-0001`).
- **User Profiles & Watchlists**: Profile preferences, notification toggles, geolocation support, and personalized movie watchlists.
- **Admin Dashboard**: Real-time metrics, user status controls, and account approvals.

---

## 🏗 Project Architecture

```
streamplus-main/
├── render.yaml                    # Cloud deployment specification (Render Blueprint)
├── requirements.txt               # Python package dependencies
├── .vscode/
│   └── settings.json              # Postman & VS Code development preferences
└── backend-dev1/                  # Main application package
    ├── .env                       # Local environment variables configuration
    ├── .gitignore                 # Git ignore rules
    ├── login.txt                  # Sample test account credentials & profile payload
    ├── main.py                    # Application entrypoint & FastAPI lifespan setup
    └── app/
        ├── api/
        │   ├── __init__.py
        │   └── v1/                # Version 1 API routers
        │       ├── admin.py       # Admin dashboard & user moderation routes
        │       ├── auth.py        # OTP dispatch & JWT verification endpoints
        │       ├── movies.py      # Movie listing & creation routes
        │       └── users.py       # Profile & watchlist management routes
        ├── core/
        │   ├── config.py          # Pydantic Settings & environment resolver
        │   ├── database.py        # Async SQLAlchemy engine & session factory
        │   └── security.py        # Passlib, JWT helpers, OTP lifecycle & SMTP mailer
        ├── faker/
        │   ├── mock_movies.json   # Seed movie dataset
        │   ├── mock_users.json    # Seed user dataset (Ghanaian locale profiles)
        │   ├── movieMock.py       # Movie mock data generation script
        │   └── userMock.py        # User mock data generation script
        └── models/
            ├── admin.py           # Admin schemas (AccountApproval, AccountBan, Status)
            ├── auth.py            # Auth schemas (EmailRequest, OTPVerify, Tokens)
            ├── category.py        # SQLAlchemy Category model
            ├── movie_types.py     # Custom MovieID TypeDecorator & ID generator
            ├── movies.py          # MovieList & WatchListBase models & schemas
            ├── series.py          # TV Series model draft
            ├── user_types.py      # Cross-dialect UUID TypeDecorator (PostgreSQL/SQLite)
            └── users.py           # User model, Enums, and Pydantic schemas
```

---

## ✨ Key Features

1. **Async-First Execution**:
   - Built on Starlette and ASGI standard using `asyncio` for non-blocking I/O.
   - Asynchronous ORM sessions via SQLAlchemy 2.0 with `asyncpg` and `aiosqlite`.

2. **Dual-Database Support**:
   - Automatically switches dialect depending on `ENVIRONMENT` and `USE_SQLITE_FOR_DEV`.
   - Custom cross-compatible database types (`UUID` and `MovieID`) that adapt cleanly to PostgreSQL native types or SQLite string types.

3. **Passwordless OTP Authentication**:
   - Generates and emails verification OTP codes with configurable TTL (default 5 minutes).
   - In-memory OTP storage with rate limiting and retry safeguards (3 max attempts).
   - Auto-registration for first-time OTP users.

4. **JWT Security & Role-Based Access Control**:
   - HMAC-SHA256 token signing with configurable expiration.
   - User roles: `CLIENT`, `TASKER`, and `ADMIN`.
   - Subscription service tiers: `FREE`, `PREMIUM`, and `PREMIUM_PLUS`.

5. **Movie Management**:
   - Custom sequential identifiers (`stp-0001`, `stp-0002`).
   - Pydantic field validators ensuring titles, minimum runtime, and rating thresholds.
   - User watchlist relationship with movie details and tracking.

6. **Automated Seed Data**:
   - Pre-configured `Faker` scripts generating realistic movie metadata and user profiles.

---

## 📂 File & Directory Structure

| Path | Description |
|---|---|
| `requirements.txt` | Python runtime dependencies (FastAPI, Uvicorn, SQLAlchemy, Pydantic, etc.) |
| `render.yaml` | Infrastructure as Code (IaC) configuration for deploying to Render |
| `backend-dev1/main.py` | FastAPI application initialization, CORS setup, lifespan DB connection, and router mounts |
| `backend-dev1/app/core/config.py` | Settings class loading variables from `.env`, computing dynamic database URLs |
| `backend-dev1/app/core/database.py` | Engine creation (`postgresql+asyncpg` or `sqlite+aiosqlite`), `get_db` dependency, and `init_db` |
| `backend-dev1/app/core/security.py` | Bcrypt hashing, JWT token encoding/decoding, OTP generation, and email dispatch |
| `backend-dev1/app/api/v1/auth.py` | OTP send, verify, and resend endpoints |
| `backend-dev1/app/api/v1/users.py` | User profile retrieval/updates and user watchlist management |
| `backend-dev1/app/api/v1/movies.py` | Movie catalog retrieval and movie creation endpoints |
| `backend-dev1/app/api/v1/admin.py` | Admin dashboard statistics, approvals, and user moderation |
| `backend-dev1/app/models/` | SQLAlchemy models and Pydantic validation schemas |
| `backend-dev1/app/faker/` | Mock generators and JSON mock datasets |

---

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Server**: [Uvicorn](https://www.uvicorn.org/) (ASGI)
- **Database ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async Engine)
- **Database Drivers**:
  - [asyncpg](https://github.com/MagicStack/asyncpg) (PostgreSQL Async Driver)
  - [aiosqlite](https://github.com/omnilib/aiosqlite) (SQLite Async Driver)
- **Data Validation & Settings**: [Pydantic](https://docs.pydantic.dev/) & [pydantic-settings](https://github.com/pydantic/pydantic-settings)
- **Security & Tokens**: [python-jose](https://github.com/mpdavis/python-jose) (JWT) & [passlib](https://passlib.readthedocs.io/) (Bcrypt)
- **Cloud Deployment**: [Render](https://render.com/)

---

## ⚙️ Configuration & Environment Variables

Create or update the `.env` file inside `backend-dev1/`:

```ini
# Environment
ENVIRONMENT=development         # 'development', 'testing', or 'production'
DEBUG=True

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/streamplus
DATABASE_TEST_URL=sqlite:///./test_db.sqlite3
USE_SQLITE_FOR_DEV=True
USE_SQLITE=False

# JWT Security
SECRET_KEY=YourSuperSecretKeyGoesHere
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_IN_MINS=30
REFRESH_TOKEN_EXPIRE_IN_DAYS=7

# OTP Verification
OTP_EXPIRE_IN_MINS=5
OTP_LENGTH=6
USE_FIXED_OTP_LENGTH_FOR_TESTING=True
FIXED_OTP_VALUE=123456

# CORS
ALLOWED_ORIGINS=["*"]

# Email (SMTP for OTP dispatch)
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAILS_FROM_EMAIL=noreply@streamplus.com
EMAILS_FROM_NAME=StreamPlus

# Storage (MinIO / S3)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=streamplus
MINIO_SECURE=False

# Cache & SMS
REDIS_URL=redis://localhost:6379
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

> [!NOTE]
> When `ENVIRONMENT=development` and `USE_FIXED_OTP_LENGTH_FOR_TESTING=True`, the API uses `123456` as the OTP code and logs it directly to stdout instead of sending an email.

---

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.10 or higher
- **Git**
- Optional: **PostgreSQL** (if running against a live PostgreSQL database instead of SQLite)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd streamplus-main
   ```

2. **Create and activate a virtual environment**:
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   Make sure `backend-dev1/.env` exists and contains appropriate configurations.

### Running the Server

Navigate to the `backend-dev1` directory and launch Uvicorn:

```bash
cd backend-dev1
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The database tables are automatically initialized during the application lifespan startup.

---

## 📖 API Documentation & Endpoints

Once the application is running, interact with the interactive API docs:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Core & System

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status and links to documentation |
| `GET` | `/health` | System health check (environment, database status, python version) |

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/send-otp` | Request a verification code to email (registers new user if absent) |
| `POST` | `/api/v1/auth/verify-otp` | Submit OTP; validates code, activates user, returns JWT tokens |
| `POST` | `/api/v1/auth/resend-otp` | Resend verification OTP code |

### User & Profile Management (`/api/v1/users`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/users/profile/{user_id}` | Retrieve profile details by User UUID |
| `POST` | `/api/v1/users/profile` | Create a new user profile |
| `PUT` | `/api/v1/users/profile/{user_id}` | Update existing user profile attributes |
| `GET` | `/api/v1/users/watchlist/user/{user_id}` | Retrieve user's movie watchlist |
| `POST` | `/api/v1/users/watchlist/user/{user_id}` | Add a movie to user's watchlist |
| `PUT` | `/api/v1/users/watchlist/user/{user_id}` | Remove a movie from user's watchlist |
| `DELETE` | `/api/v1/users/watchlist/user/{user_id}` | Clear user's entire watchlist |

### Movies Catalog (`/api/v1/movies`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/movies/` | List all available movies in the catalog |
| `GET` | `/api/v1/movies/{movie_id}` | Retrieve details for a specific movie |
| `POST` | `/api/v1/movies/` | Add a new movie to the catalog |

### Admin & Moderation (`/api/v1/admin`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/admin/dashboard` | Aggregated metrics (total movies and total users) |
| `GET` | `/api/v1/admin/dashboard/users` | Retrieve all registered users |
| `GET` | `/api/v1/admin/approvals` | List pending unapproved accounts |
| `PUT` | `/api/v1/admin/approvals/{user_id}` | Update account approval status |
| `PUT` | `/api/v1/admin/bans/{user_id}` | Update account status (ban/unban/suspend) |
| `GET` | `/api/v1/admin/serviceStatus` | List users with service tier changes |
| `PUT` | `/api/v1/admin/serviceStatus/{user_id}` | Modify user subscription service tier |
| `GET` | `/api/v1/admin/users/{user_id}` | Admin fetch user by ID |
| `DELETE` | `/api/v1/admin/users/{user_id}` | Admin delete user by ID |

---

## 🗄 Database Models

- **`User`** (`users`):
  - Primary Key: `UUID`
  - Fields: `phone`, `email`, `first_name`, `last_name`, `role`, `status`, `service`, `profile_picture`, `date_of_birth`, `gender`, `bio`, `watch_list`, `location`, `address`, `is_email_verified`, `is_phone_verified`, `preferences`, `notification_settings`, timestamps.
- **`MovieList`** (`movie_list`):
  - Primary Key: `MovieID` (e.g. `stp-0001`)
  - Fields: `title`, `category`, `description`, `poster_url`, `trailer_url`, `duration`, `release_year`, `rating`, `cast_members`, `producer`, `views`, timestamps.
- **`WatchListBase`** (`watchlist`):
  - Composite Key: `movie_id` (FK `movie_list.id`), `user_id` (FK `users.id`)
  - Fields: `title`, `poster_url`, `trailer_url`, timestamps.
- **`Category`** (`category`):
  - Primary Key: `id` (Integer)
  - Fields: `name`, `description`.

---

## 🎲 Mock Data Generation

Mock data scripts are located in `backend-dev1/app/faker/`:

- **Generate Mock Movies**:
  ```bash
  cd backend-dev1/app/faker
  python movieMock.py
  ```
  Generates `mock_movies.json` with realistic movie titles, posters, directors, runtimes, and ratings.

- **Generate Mock Users**:
  ```bash
  cd backend-dev1/app/faker
  python userMock.py
  ```
  Generates `mock_users.json` with localized Ghanaian phone numbers, geolocations, and profile configurations.

---

## ☁️ Deployment (Render)

The project includes a ready-to-use [`render.yaml`](file:///c:/subdrive/codebase/Fastapi/work/streamplus-main/render.yaml) blueprint:

```yaml
services:
  - type: web
    name: advanced-api-backend
    runtime: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: cd backend-dev1 && uvicorn main:app --host 0.0.0.0 --port $PORT
```

To deploy:
1. Connect your GitHub/GitLab repository to **Render**.
2. Select **Blueprints** and deploy using `render.yaml`.
3. Provide environment variables (`DATABASE_URL`, `SECRET_KEY`, etc.) in the Render dashboard.

---

## 📄 License

This project is licensed under the MIT License - feel free to adapt and expand for your streaming application needs.

