from app.models.order import OrderModel
from app.ma import ma


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
        load_instance = True
        include_fk = True
        # dump_only = ("id", "status", )
