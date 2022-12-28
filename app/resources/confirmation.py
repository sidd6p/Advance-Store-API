import traceback

from flask_restful import Resource
from flask import make_response, render_template

from app.models import ConfirmationModel, UserModel
from app.schemas import ConfirmationSchema
from app.resources.user import USER_NOT_FOUND
from app.library.mailgun import MailGunException

confirmation_Schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        """
        Return confirmation HTML page
        """
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": "NOT_FOUND"}, 404

        if confirmation.is_expired:
            return {"message": "CONFIRMATION_EXPIRED"}, 400

        if confirmation.confirmed:
            return {"message": "CONFIRMATION_ALREADY_CONFIRMED"}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email),
            200,
            headers,
        )


class ConfirmationByUser(Resource):
    @classmethod
    def post(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        try:
            confirmation = user.most_recent_confirmation()
            if confirmation:
                if confirmation.confirmed:
                    return {"message": "Already Confirmed"}, 400
                confirmation.force_to_expire()

            print("okok")
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": "Resend sucessfully"}, 200
        except MailGunException as error:
            return {"message": str(error)}, 500
        except:
            return {"message": traceback.print_exc()}, 500
