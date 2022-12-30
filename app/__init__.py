import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class
from flask_migrate import Migrate
from marshmallow import ValidationError
from dotenv import load_dotenv

load_dotenv()

from app.db import db
from app.ma import ma
from app.oa import oauth
from app import default_config
from app.blocklist import BLOCKLIST
from app.resources.user import (
    UserRegister,
    UserLogin,
    User,
    TokenRefresh,
    UserLogout,
    SetPassword,
)
from app.resources.item import Item, ItemList
from app.resources.store import Store, StoreList
from app.resources.confirmation import Confirmation, ConfirmationByUser
from app.resources.image import ImageUpload, Image
from app.resources.github_login import GithubLogin, GithubAuthorize
from app.library.images_helper import IMAGE_SET


def create_app(config_file=default_config):
    app = Flask(__name__)

    app.config.from_object(config_file)
    app.config.from_envvar("APPLICATION_SETTINGS")
    patch_request_class(app, 10 * 1024 * 1024)  # 10 MB
    configure_uploads(app, IMAGE_SET)

    jwt = JWTManager(app)
    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(error):
        return jsonify(error), 400

    # This method will check if a token is blocklisted, and will be called automatically when blocklist is enabled
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    api.add_resource(Store, "/store/<string:name>")
    api.add_resource(StoreList, "/stores")
    api.add_resource(Item, "/item/<string:name>")
    api.add_resource(ItemList, "/items")
    api.add_resource(UserRegister, "/register")
    api.add_resource(User, "/user/<int:user_id>")
    api.add_resource(UserLogin, "/login")
    api.add_resource(TokenRefresh, "/refresh")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(Confirmation, "/user_confirmation/<string:confirmation_id>")
    api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
    api.add_resource(SetPassword, "/user/password")
    api.add_resource(ImageUpload, "/upload/image")
    api.add_resource(Image, "/image/<string:filename>")
    api.add_resource(GithubLogin, "/login/github")
    api.add_resource(GithubAuthorize, "/login/github/authorized")

    return app
