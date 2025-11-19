from typing import Any, Dict

# -----------------------
# User Schemas Examples
# -----------------------

organization_read_example: Dict[str, Any] = {
    "org_id": "660e8400-e29b-41d4-a716-446655440000",
    "org_name": "Tech Innovators",
    "org_email": "contact@techinnovators.com",
    "org_display_name": "Tech Innovators",
    "org_owner_id": "550e8400-e29b-41d4-a716-446655440000",
    "org_type": "for_profit",
    "is_active": True,
    "created_at": "2025-10-20T09:00:00",
    "updated_at": "2025-10-22T15:30:00",
}

organization_create_example: Dict[str, Any] = {
    "org_name": "Tech Innovators",
    "org_email": "contact@techinnovators.com",
    "org_type": "for_profit",
}


organization_update_example: Dict[str, Any] = {
    "org_name": "Tech Innovators Ltd.",
    "org_owner_id": "550e8400-e29b-41d4-a716-446655440000",
    "org_email": "contact@techinnovators.com",  
}