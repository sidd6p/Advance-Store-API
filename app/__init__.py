import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv

from app.db import db
from app.ma import ma
from app.blocklist import BLOCKLIST
from app.resources.user import (
    UserRegister,
    UserLogin,
    User,
    TokenRefresh,
    UserLogout,
)
from app.resources.item import Item, ItemList
from app.resources.store import Store, StoreList
from app.resources.confirmation import Confirmation, ConfirmationByUser
from app.models import *

load_dotenv()


def create_app():

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.secret_key = os.getenv(
        "SECRET_KEY"
    )  # could do app.config['JWT_SECRET_KEY'] if we prefer

    api = Api(app)
    jwt = JWTManager(app)
    db.init_app(app)
    ma.init_app(app)

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
    api.add_resource(ConfirmationByUser, "/confirmation.user/<int:user_id>")

    return app
