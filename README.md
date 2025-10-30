# FastAPI User-Todo Application

A modern REST API built with FastAPI, SQLAlchemy, and Python that manages users and their todos.

## Features

- User authentication and authorization with JWT tokens
- Role-based access control (User/Admin roles)
- Todo management system
- RESTful API endpoints
- SQLAlchemy ORM integration
- Environment-based configuration
- Refresh token support with secure cookies

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- Python 3.x
- SQLite (Database)
- JWT Authentication
- BCrypt password hashing

## Project Structure

```
fast_api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth_router.py    # Authentication endpoints
│   │       ├── dependancies.py   # FastAPI dependencies
│   │       └── jwt_handler.py    # JWT token management
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py            # Settings management
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py          # Database configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   └── todo.py             # Todo model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py      # User Pydantic models
│   │   ├── todo_schema.py      # Todo Pydantic models
│   │   └── examples/           # Schema examples
│   └── example.env             # Environment template
├── main.py                     # Application entry point
├── check_settings.py           # Settings verification
├── .env                        # Environment variables
├── requirements.txt            # Project dependencies
└── README.md                   # This file
```

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/konstantinos1981/FastApiProject
cd fast_api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
   - Copy `app/example.env` to `.env` in the root directory
   - Update the values in `.env`:

```env
PROJECT_NAME="Todo API"
DATABASE_URL="sqlite:///./data.db"
SECRET_KEY="your-secure-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_SECRET_KEY="your-secure-refresh-key"
```

5. Verify settings:

```bash
python check_settings.py
```

6. Run the application:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, you can access:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /auth/signup` - Register new user
- `POST /auth/admin_signup` - Register new admin
- `POST /auth/token` - Login and get access token
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout and clear refresh token

### Users

- `GET /auth/users` - List all users (admin only)
- `GET /auth/users/info` - Get current user info
- `GET /auth/users/{username}` - Get user by username (admin only)
- `GET /auth/users/user_email/{email}` - Get user by email (admin only)

## Models

### User Model

- UUID-based primary key
- Role-based access (user/admin)
- Timestamp tracking (created_at, updated_at)
- Secure password hashing
- Email and username uniqueness
- One-to-many relationship with todos

### Todo Model

- UUID-based primary key
- Title and description fields
- Completion status tracking
- Timestamp tracking
- Many-to-one relationship with users

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

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
