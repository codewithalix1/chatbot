KNOWLEDGE_BASE = [
    {
        "title": "User Creation",
        "content": """
Administrators can create new users through the user management assistant.

Required field:
- Email

Optional fields:
- Name
- Phone
- City

The email address must be unique.
"""
    },
    {
        "title": "User Updates",
        "content": """
Administrators can update an existing user's name, email, phone, or city.

Before updating a user by name, the assistant should search for the user first.

If multiple users match, the administrator must identify the correct user.
"""
    },
    {
        "title": "User Deletion",
        "content": """
Administrators can delete users.

The assistant must request explicit confirmation before deleting a user.

The assistant must identify the exact user before deletion.
"""
    },
    {
        "title": "User Search",
        "content": """
Administrators can search for users by name or email.

The assistant must never invent user information.

User information must come from the database.
"""
    },
    {
        "title": "User Fields",
        "content": """
The user management system supports these fields:

- Name
- Email
- Phone
- City

Email addresses must be unique.
"""
    }
]