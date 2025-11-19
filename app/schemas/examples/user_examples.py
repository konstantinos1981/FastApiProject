from typing import Any, Dict

# -----------------------
# User Schemas Examples
# -----------------------

user_read_example:Dict [str, Any] = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "organization": "Tech Innovators",
    "username": "john_doe123",
    "is_active": True,
    "created_at": "2025-10-24T12:00:00",
    "updated_at": "2025-10-24T12:30:00"
}

user_create_example:Dict [str, Any] = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "username": "johnDoe123",
    "password": "Comp1exP@ssw0rd",
    "confirm_password": "Comp1exP@ssw0rd"
}

user_update_example:Dict [str, Any] = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "username": "johnDoe123"
}

user_with_todos_example:Dict [str, Any] = {
    **user_read_example,
    "todos": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "owner_id": 1,
            "title": "Buy groceries",
            "description": "Milk, Eggs, Bread",
            "is_completed": False,
            "created_at": "2025-10-23T18:00:00",
            "updated_at": "2025-10-24T10:00:00"
        },
        {
            "id": "550e8400-e29b-41d4-a716-446655449999",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Read book",
            "description": "Read 'Atomic Habits'",
            "is_completed": True,
            "created_at": "2025-10-23T18:00:00",
            "updated_at": "2025-10-24T10:00:00"
        }
    ]
}

user_password_change_example:Dict [str, Any] = {
    "old_password": "OldP@ssw0rd",
    "new_password": "NewC0mpl3xP@ssw0rd",
    "confirm_password": "NewC0mpl3xP@ssw0rd"
}