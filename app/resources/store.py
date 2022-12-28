from flask_restful import Resource

from app.models import StoreModel
from app.schemas.store import StoreSchema
from app.library.strings import get_text


store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store), 200
        return {"message": get_text("STORE_NOT_FOUND")}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {"message": get_text("NAME_ALREADY_EXISTS").format(name)}, 400

        store = StoreModel(name=name)

        try:
            store.save_to_db()
        except:
            return {"message": get_text("ERROR_INSERTING")}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": get_text("STORE_DELETED")}, 200

        return {"message": get_text("STORE_NOT_FOUND")}, 404


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {"stores": store_list_schema.dump(StoreModel.find_all())}, 200
