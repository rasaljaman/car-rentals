from supabase import create_client
from decouple import config

supabase = create_client(
    config("SUPABASE_URL"),
    config("SUPABASE_SERVICE_ROLE_KEY"),
)