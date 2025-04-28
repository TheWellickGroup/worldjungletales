import requests
from django.conf import settings


class Recaptcha:
    def __init__(self):
        if not settings.RECAPTCHA_SECRET_KEY or settings.RECAPTCHA_SITE_KEY:
            raise ValueError(
                "RECAPTCHA_SECRET_KEY and RECAPTCHA_SITE_KEY must be provided!"
            )
        self.secret_key = settings.RECAPTCHA_SECRET_KEY
        self.verify_url = "https://www.google.com/recaptcha/api/siteverify"

    def verify(self, recaptcha_response):
        payload = {
            "secret": self.secret_key,
            "response": recaptcha_response,
        }
        response = requests.post(self.verify_url, data=payload)
        result = response.json()
        return result.get("success")
