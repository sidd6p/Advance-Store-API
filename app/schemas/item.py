from app.models.item import ItemModel
from app.models.store import StoreModel
from app.ma import ma


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_instance = True
        include_fk = True
        load_only = ("store",)
        dump_only = ("id", "stripe_id")
