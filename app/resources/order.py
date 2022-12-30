from collections import Counter

from flask_restful import Resource
from flask import request

from app.library.strings import get_text
from app.models.item import ItemModel
from app.models.order import OrderModel, ItemsInOrders


class Order(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        items = []
        item_id_quantities = Counter(data["item_ids"])

        for _id, count in item_id_quantities.most_common():
            item = ItemModel.find_by_id(str(_id))
            if not item:
                return {"message": get_text("ITEM_NOT_FOUND")}, 404
            items.append(ItemsInOrders(item_id=_id, quantity=count))

        order = OrderModel(items=items, status="pending")
        order.save_to_db()

        return {"message": get_text("ORDER_PLACED")}, 200
