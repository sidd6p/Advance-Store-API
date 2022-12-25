from models import ItemModel, StoreModel
from ma import ma


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_instance = True
        include_fk = True
        load_only = ("store",)
        dump_only = ("id",)
