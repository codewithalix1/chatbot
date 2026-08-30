from typing import Optional

from langchain_core.tools import tool

from dependencies import get_supabase
from services.user_service import UserService
from ai.rag import search_knowledge


@tool
def search_users(name: str):
    """
    Search for users by name.

    Use this when the administrator wants to find a user
    or when you need to identify a user before updating them.
    """

    supabase = get_supabase()
    service = UserService(supabase)

    return service.search_users(name)


@tool
def create_user(
    name: str,
    email: str,
    phone: Optional[str] = None,
    city: Optional[str] = None,
):
    """
    Create a new user.

    Email is required.
    Name, phone, and city are optional.
    """

    from models.user import UserCreate

    supabase = get_supabase()
    service = UserService(supabase)

    user = UserCreate(
        name=name,
        email=email,
        phone=phone,
        city=city,
    )

    return service.create_user(user)


@tool
def update_user(
    user_id: str,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    city: Optional[str] = None,
):
    """
    Update an existing user.

    Only fields explicitly provided by the administrator
    should be changed.
    """

    from models.user import UserUpdate

    supabase = get_supabase()
    service = UserService(supabase)

    user = UserUpdate(
        name=name,
        email=email,
        phone=phone,
        city=city,
    )

    return service.update_user(
        user_id,
        user,
    )


@tool
def delete_user(user_id: str):
    """
    Delete an existing user.

    Only call this tool after the administrator has explicitly
    confirmed that the user should be deleted.
    """

    supabase = get_supabase()
    service = UserService(supabase)

    return service.delete_user(user_id)


@tool
def search_knowledge_base(query: str):
    """
    Search the application's knowledge base.

    Use this for questions about:
    - user management rules
    - available user fields
    - user creation requirements
    - update rules
    - deletion rules
    - system policies
    - how the user management system works

    Do NOT use this tool to retrieve actual user information.
    Actual user information must come from Supabase.
    """

    documents = search_knowledge(query)

    if not documents:
        return "No relevant information was found in the knowledge base."

    results = []

    for document in documents:
        title = document.metadata.get("title", "Knowledge")
        content = document.page_content

        results.append(
            f"Title: {title}\n"
            f"Content: {content}"
        )

    return "\n\n".join(results)