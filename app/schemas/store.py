from app.ma import ma
from app.models import StoreModel
from app.models import ItemModel
from app.schemas.item import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        load_instance = True
        dump_only = ("id",)
        include_fk = True
