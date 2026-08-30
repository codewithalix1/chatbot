from fastapi import HTTPException

from models.user import UserCreate, UserUpdate


class UserService:

    def __init__(self, supabase):
        self.supabase = supabase

    def get_users(self):
        response = (
            self.supabase
            .table("users")
            .select("*")
            .execute()
        )

        return response.data

    def get_user(self, user_id: str):
        response = (
            self.supabase
            .table("users")
            .select("*")
            .eq("id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return response.data[0]

    def search_users(self, name: str):
        response = (
            self.supabase
            .table("users")
            .select("*")
            .ilike("name", f"%{name}%")
            .execute()
        )

        return response.data

    def create_user(self, user: UserCreate):
        response = (
            self.supabase
            .table("users")
            .insert(user.model_dump())
            .execute()
        )

        return response.data[0]

    def update_user(
        self,
        user_id: str,
        user: UserUpdate
    ):
        data = {
            key: value
            for key, value in user.model_dump().items()
            if value is not None
        }

        if not data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update"
            )

        response = (
            self.supabase
            .table("users")
            .update(data)
            .eq("id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return response.data[0]

    def delete_user(self, user_id: str):
        existing = (
            self.supabase
            .table("users")
            .select("*")
            .eq("id", user_id)
            .execute()
        )

        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        (
            self.supabase
            .table("users")
            .delete()
            .eq("id", user_id)
            .execute()
        )

        return {
            "message": "User deleted successfully"
        }