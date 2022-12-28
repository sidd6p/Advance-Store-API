import traceback
import time

from flask_restful import Resource
from flask import make_response, render_template

from app.models import ConfirmationModel, UserModel
from app.schemas import ConfirmationSchema
from app.library.mailgun import MailGunException
from app.library.strings import get_text

confirmation_Schema = ConfirmationSchema(many=True)
USER_NOT_FOUND = get_text("USER_NOT_FOUND")


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
    def get(cls, user_id: int):
        """
        This endpoint is used for testing and viewing Confirmation models and should not be exposed to public.
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        return (
            {
                "current_time": int(time.time()),
                # we filter the result by expiration time in descending order for convenience
                "confirmation": confirmation_Schema.dump(user.all_confirmation()),
            },
            200,
        )

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
