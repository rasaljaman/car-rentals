from supabase import create_client
from decouple import config
import uuid

supabase = create_client(
    config("SUPABASE_URL"),
    config("SUPABASE_SERVICE_ROLE_KEY"),
)

def upload_to_supabase(file, bucket):
    """
    Uploads file to Supabase Storage and returns public URL
    """
    file_ext = file.name.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"

    supabase.storage.from_(bucket).upload(
        file_name,
        file.read(),
        {"content-type": file.content_type},
    )

    public_url = supabase.storage.from_(bucket).get_public_url(file_name)
    return public_url