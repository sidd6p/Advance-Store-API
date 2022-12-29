import os

from flask import url_for

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_BLOCKLIST_ENABLED = True
JWT_BLOCKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]  # allow blocklisting for access and refresh tokens
UPLOADED_IMAGES_DEST = os.path.join("app", "static", "images")
