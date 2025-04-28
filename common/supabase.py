from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from supabase import Client, create_client

from common.constants import ARTICLE_IMAGES_BUCKET


class StorageClient:
    def __init__(self):
        if (
            not settings.SUPABASE_URL
            or not settings.SUPABASE_SERVICE_ROLE_KEY
            or not settings.SUPABASE_BUCKET
        ):
            raise ValueError(
                "Supabase URL and Service Role Key must be set in settings."
            )

        self.client: Client = create_client(
            settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
        )
        self.article_bucket = ARTICLE_IMAGES_BUCKET
        self.bucket = settings.SUPABASE_BUCKET

    def _upload_to_supabase_bucket(self, image_file):

        file_name = f"{self.article_bucket}/-{timezone.now()}-{image_file.name}"
        file_content = image_file.read()

        _ = self.client.storage.from_(self.bucket).upload(file_name, file_content)

        return self.client.storage.from_(self.bucket).get_public_url(file_name)

    def _delete_image_from_bucket(self, image_url):
        file = f"{self.article_bucket}/{image_url}"
        response = self.client.storage.from_(self.bucket).remove([file])
        return response

    def upload_article_cover(self, request, old_image_url=None):
        image_url = old_image_url

        if "image" in request.FILES:
            image = request.FILES["image"]
            try:
                image_url = self._upload_to_supabase_bucket(image)
            except Exception as e:
                messages.warning(
                    request, f"Failed to upload image {image.name}: {str(e)}"
                )
                return old_image_url

        if old_image_url and image_url != old_image_url:
            self._delete_image_from_bucket(old_image_url)

        return image_url
