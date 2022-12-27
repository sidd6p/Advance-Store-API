import os

from typing import List
from requests import Response, post


FAILED_API_LOAD = "Failed to load MailGun API Key"
FAILED_DOMAIN_LOAD = "Failed to load MailGun Domain"


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MailGun:
    MAILGUM_DOMAIN = os.getenv("MAILGUM_DOMAIN")
    MAILGUM_API = os.getenv("MAILGUM_API")
    FROM_TITLE = os.getenv("FROM_TITLE")

    @classmethod
    def send_email(
        cls, emails: List[str], subject: str, text: str, html: str
    ) -> Response:
        if cls.MAILGUM_API is None:
            raise MailGunException(FAILED_API_LOAD)
        if cls.MAILGUM_DOMAIN is None:
            raise MailGunException(FAILED_DOMAIN_LOAD)
        response = post(
            url=f"https://api.mailgun.net/v3/{cls.MAILGUM_DOMAIN}/messages",
            auth=("api", f"{cls.MAILGUM_API}"),
            data={
                "from": f"{cls.FROM_TITLE} <mailgun@{cls.MAILGUM_DOMAIN}>",
                "to": emails,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )
        if response.status_code != 200:
            raise MailGunException("Error in sending the mail")
        return response
