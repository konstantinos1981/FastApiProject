# FastAPI User-Todo Application

A modern REST API built with FastAPI, SQLAlchemy, and Python that manages users and their todos.

## Features

- User authentication and authorization with JWT tokens
- Role-based access control (User/Admin roles)
- Todo management system
- Refresh token support with secure cookies
- RESTful API endpoints
- SQLAlchemy ORM integration
- Environment-based configuration

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic (v2)
- Python 3.11+
- SQLite (local development)
- JWT Authentication
- BCrypt password hashing

## Project structure

```
fast_api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── admin_router.py      # Admin endpoints
│   │       ├── auth_router.py       # Authentication endpoints
│   │       ├── dependancies.py      # FastAPI dependencies (db, get_current_user, ...)
│   │       └── jwt_handler.py       # JWT helpers
│   ├── core/
│   │   └── config.py                # Settings management
│   ├── db/
│   │   └── database.py              # Database engine / session
│   ├── models/
│   │   ├── user.py                  # SQLAlchemy User model (includes UserRole enum)
│   │   └── todo.py                  # SQLAlchemy Todo model
│   ├── schemas/
│   │   ├── user_schema.py           # Pydantic user schemas (UserRead, UserCreate, ...)
│   │   └── todo_schema.py           # Pydantic todo schemas
│   └── example.env                  # Example environment variables
├── main.py                          # App entrypoint
├── check_settings.py                # Helper to verify settings load
├── .env                             # Local environment variables (not committed)
├── requirements.txt                 # Python dependencies
└── README.md
```

## Getting started (local)

1. Clone the repository

```bash
git clone https://github.com/konstantinos1981/FastApiProject
cd fast_api
```

2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create your .env

```bash
cp app/example.env .env
# Edit .env and set values (DATABASE_URL, SECRET_KEY, REFRESH_SECRET_KEY, etc.)
```

Example .env values (example.env shipped with the repo):

```
PROJECT_NAME="Todo API"
DATABASE_URL="sqlite:///./data.db"
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_SECRET_KEY="your-refresh-secret-key"
```

5. Verify settings load

```bash
python check_settings.py
```

6. Run the app

```bash
uvicorn app.main:app --reload
```

Open API docs:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Important endpoints

Authentication:

- POST /auth/signup — register user
- POST /auth/admin_signup — register admin
- POST /auth/token — obtain access token
- POST /auth/refresh — refresh access token (secure cookie)
- POST /auth/logout — clear refresh token

Admin (example):

- GET /admin/ — admin root (returns current admin user)
- GET /admin/users — list users (admin only)
- GET /admin/users/{username} — fetch user by username (admin only)
- GET /admin/users/user_email/{email} — fetch user by email (admin only)

Notes:

- The API returns Pydantic response models (UserRead, TodoRead) that omit sensitive fields (e.g. hashed_password).
- Ensure tokens you use belong to users with the required role for protected endpoints.

## Contributing

1. Fork the repo
2. Create a branch: git checkout -b feature/your-feature
3. Commit: git commit -m "feat: short description"
4. Push and open a PR

## License

MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
