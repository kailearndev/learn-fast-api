
from core.supabase import supabase


def get_or_create_user(user):
    res = supabase.table("users") \
        .select("*") \
        .eq("id", user.id) \
        .execute()

    if res.data:
        return res.data[0]

    created = supabase.table("users").insert({
        "id": user.id,
        "email": user.email,
        "role": "user"
    }).execute()

    return created.data[0]
