import traceback

from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.user import UserSchema
from app.models.user import UserModel
from app.blocklist import BLOCKLIST
from app.library.mailgun import MailGunException
from app.models.confirmation import ConfirmationModel
from app.library.strings import get_text
from app.library.password_hasing import encrypt_password, check_encrypted_password

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())
        user.password = encrypt_password(user.password)

        if UserModel.find_by_username(user.username):
            return {"message": get_text("USER_ALREADY_EXISTS")}, 400

        if UserModel.find_by_email(user.email):
            return {"message": get_text("EMAIL_ALREADY_EXISTS")}, 400

        try:
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": get_text("CREATED_SUCCESSFULLY")}, 201
        except MailGunException as error:
            user.delete_from_db()
            return {"message": str(error)}, 500
        except:
            try:
                traceback.print_exc()
                user.delete_from_db()
                return {"message": get_text("FAILED_TO_CREATE")}, 500
            except SQLAlchemyError as error:
                return {"message": str(error)}, 500


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": get_text("USER_NOT_FOUND")}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": get_text("USER_NOT_FOUND")}, 404
        user.delete_from_db()
        return {"message": get_text("USER_DELETED")}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = user_schema.load(request.get_json(), partial=("email",))

        user = UserModel.find_by_username(data.username)

        # this is what the `authenticate()` function did in security.py
        if user and check_encrypted_password(data.password, user.password):
            # identity= is what the identity() function did in security.py—now stored in the JWT
            confirmation = user.most_recent_confirmation()
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
            else:
                return {"message": get_text("NOT_ACTIVATED_ERROR").format(user)}, 400

        return {"message": get_text("INVALID_CREDENTIALS")}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLOCKLIST.add(jti)
        return {"message": get_text("USER_LOGGED_OUT").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class SetPassword(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        user_data = user_schema.load(request.get_json())

        try:
            user = UserModel.find_by_username(user_data.username)

            if not user:
                return {"message": get_text("USER_NOT_FOUND")}, 400
            user.password = encrypt_password(user_data.password)
            user.save_to_db()
            return {"message": get_text("USER_PASSWORD_UPDATED")}, 201
        except SQLAlchemyError as error:
            return {"message": str(error)}, 500
