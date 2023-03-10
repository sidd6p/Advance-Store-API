from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required

from app.models.item import ItemModel
from app.schemas.item import ItemSchema
from app.library.strings import get_text

# from app.library.stripe_helper import create_stripe_product

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {"message": get_text("ITEM_NOT_FOUND")}, 404

    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            return {"message": get_text("NAME_ALREADY_EXISTS").format(name)}, 400
        item_json = request.get_json()
        item_json["name"] = name
        # item_json["stripe_id"] = create_stripe_product(
        #     str(item_json["store_id"]) + name
        # )
        item = item_schema.load(item_json)
        try:
            item.save_to_db()
        except:
            return {"message": get_text("ERROR_INSERTING")}, 500

        return item_schema.dump(item), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": get_text("ITEM_DELETED")}, 200
        return {"message": get_text("ITEM_DELETED")}, 404

    @classmethod
    def put(cls, name: str):
        item_json = request.get_json()
        item_json["name"] = name
        item = ItemModel.find_by_name(item_json["name"])

        if item:
            item.price = item_json["price"]
        else:
            item = item_schema.load(item_json)

        item.save_to_db()

        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": item_list_schema.dump(ItemModel.find_all())}, 200
