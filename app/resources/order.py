from flask_restful import Resource
from flask import request

from app.library.strings import get_text
from app.models.item import ItemModel
from app.models.order import OrderModel


class Order(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        items = []

        for _id in data["items_ids"]:
            item = ItemModel.fnd_by_id(_id)
            if not item:
                return {"message": get_text("ITEM_NOT_FOUND")}, 404
            items.append(item)

        order = OrderModel(items=items, status="pending")
        order.save_to_db()
