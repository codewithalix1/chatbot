from fastapi import APIRouter, Depends

from models.user import UserCreate, UserUpdate
from services.user_service import UserService
from dependencies import get_supabase

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users(
    supabase=Depends(get_supabase)
):
    return UserService(supabase).get_users()


@router.get("/search")
def search_users(
    name: str,
    supabase=Depends(get_supabase)
):
    return UserService(supabase).search_users(name)


@router.get("/{user_id}")
def get_user(
    user_id: str,
    supabase=Depends(get_supabase)
):
    return UserService(supabase).get_user(user_id)


@router.post("/")
def create_user(
    user: UserCreate,
    supabase=Depends(get_supabase)
):
    return UserService(supabase).create_user(user)


@router.patch("/{user_id}")
def update_user(
    user_id: str,
    user: UserUpdate,
    supabase=Depends(get_supabase)
):
    return UserService(supabase).update_user(
        user_id,
        user
    )


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    supabase=Depends(get_supabase)
):
    return UserService(supabase).delete_user(user_id)