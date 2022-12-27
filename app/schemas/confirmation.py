from app.models import ConfirmationModel
from app.ma import ma


class ConfirmationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfirmationModel
        load_instance = True
        include_fk = True
        load_only = "user_id"
        dump_only = ("id", "expire_at", "confirmed")
