from django.conf import settings
from django.utils import timezone
from supabase import Client, create_client


def get_supabase_client():
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("Supabase URL and Service Role Key must be set in settings.")

    supabase: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )
    return supabase


def upload_to_supabase_bucket(bucket_name, image_file):
    supabase = get_supabase_client()

    file_name = f"{bucket_name}/-{timezone.now()}-{image_file.name}"
    file_content = image_file.read()

    _ = supabase.storage.from_(settings.SUPABASE_BUCKET).upload(file_name, file_content)

    return supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(file_name)
