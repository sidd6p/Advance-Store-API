import os

from typing import List
from requests import Response, post


class MailGun:
    MAILGUM_DOMAIN = os.getenv("MAILGUM_DOMAIN")
    MAILGUM_API = os.getenv("MAILGUM_API")
    FROM_TITLE = os.getenv("FROM_TITLE")

    @classmethod
    def send_email(
        cls, emails: List[str], subject: str, text: str, html: str
    ) -> Response:
        return post(
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
