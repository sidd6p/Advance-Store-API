from ma import ma
from models import StoreModel
from models import ItemModel
from schemas.item import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)
    class Meta:
        model = StoreModel
        load_instance = True
        dump_only = ("id",)
        include_fk = True