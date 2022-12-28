from app.ma import ma
from app.models.store import StoreModel
from app.models.item import ItemModel
from app.schemas.item import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        load_instance = True
        dump_only = ("id",)
        include_fk = True
