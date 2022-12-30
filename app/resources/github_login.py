import os

from flask_restful import Resource
from flask import g, request
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token

from app.oa import github
from app.models.user import UserModel
from app.library.strings import get_text
from app.library.password_hasing import encrypt_password
from app.models.confirmation import ConfirmationModel


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(
            callback="http://localhost:5000/login/github/authorized"
        )


class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = github.authorized_response()
        if resp is None or resp.get("access_token") is None:
            return {
                "message": request.args["error"],
            }, 500

        g.access_token = resp["access_token"]
        github_user = github.get("user")

        username = github_user.data["login"]
        email = github_user.data["email"]
        user = UserModel.find_by_username(username)

        if not user:
            try:
                user = UserModel(
                    username=username,
                    email=email,
                    password=encrypt_password(
                        os.environ.get("RANDOM_PASSWORD", "28907SDF34")
                    ),
                )
                user.save_to_db()
                confimation = ConfirmationModel(user.id)
                confimation.confirmed = True
                confimation.save_to_db()

                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
            except SQLAlchemyError as error:
                return {"message": str(error)}, 500
        else:
            return {"message", get_text("USER_ALREADY_EXISTS")}, 400
