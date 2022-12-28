import os

from typing import List
from flask import request, url_for
from requests import Response

from app.library.mailgun import MailGun
from app.db import db
from app.models.confirmation import ConfirmationModel

MAILGUM_DOMAIN = os.getenv("MAILGUM_DOMAIN")
MAILGUM_API = os.getenv("MAILGUM_API")
FROM_TITLE = os.getenv("FROM_TITLE")


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    confirmation = db.relationship(
        "ConfirmationModel",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def most_recent_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    def all_confirmation(self) -> List["ConfirmationModel"]:
        return self.confirmation.order_by(ConfirmationModel.expire_at)

    def send_confirmation_email(self) -> Response:
        # url_root = http://127.0.0.1:5000/
        # url_root[:-1] = http://127.0.0.1:5000
        # url_for("userconfirm", user_id=self.id)
        link = request.url_root[:-1] + url_for(
            "confirmation", confirmation_id=self.most_recent_confirmation().id
        )
        subject = "Registration Confirmation"
        emails = [self.email]
        text = f"Please click link to confirm user {link}"
        html = None
        return MailGun.send_email(emails, subject, text, html)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
