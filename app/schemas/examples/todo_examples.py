from typing import Any, Dict
# -----------------------
# Todo Schemas Examples
# -----------------------
todo_read_example:Dict [str, Any] = {
    "id": "550e8400-e29b-41d4-a716-446655449999",
    "owner_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, Eggs, Bread",
    "is_completed": False,
    "created_at": "2025-10-23T18:00:00",
    "updated_at": "2025-10-24T10:00:00"
}

todo_create_example:Dict [str, Any] = {
    "title": "Buy groceries",
    "description": "Milk, Eggs, Bread"
}
