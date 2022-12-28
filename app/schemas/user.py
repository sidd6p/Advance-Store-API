# from marshmallow import Schema, fields

# class UserSchema(Schema):
#     # class Meta:
#     #     load_only=("password",)
#     #     dump_only = ("id", )

#     id = fields.Int(dump_only=True)
#     username = fields.Str(required=True)
#     password = fields.Str(required=True, load_only=True)

from marshmallow import pre_dump

from app.ma import ma
from app.models import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password",)
        dump_only = ("id", "confirmation")

    @pre_dump
    def _pre_dump(self, user: UserModel, **kwargs):
        user.confirmation = [user.most_recent_confirmation()]
        return user
