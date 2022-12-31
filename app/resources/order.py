from collections import Counter

from flask_restful import Resource
from flask import Flask, redirect, request
from stripe import error

from app.library.strings import get_text
from app.models.item import ItemModel
from app.models.order import OrderModel, ItemsInOrders
from app.schemas.order import OrderSchema


order_schema = OrderSchema()


class Order(Resource):
    @classmethod
    def get(cls):
        return order_schema.dump(OrderModel.find_all(), many=True), 200

    @classmethod
    def post(cls):
        data = request.get_json()
        items = []
        item_id_quantities = Counter(data["item_ids"])
        amount = 0.0
        total_items = 0

        for _id, count in item_id_quantities.most_common():
            item = ItemModel.find_by_id(str(_id))
            if not item:
                return {"message": get_text("ITEM_NOT_FOUND")}, 404
            items.append(ItemsInOrders(item_id=_id, quantity=count))
            total_items = total_items + count
            amount = amount + (item.price * count)

        order = OrderModel(
            items=items,
            status="pending",
            amount=amount * 100,
            description=f"There are total {total_items} items with amount {amount} in this order",
        )
        order.save_to_db()

        try:
            order.charge_with_stripe()
            order.set_status("completed")
            return order_schema.dump(order), 200
        except error.StripeError as err:
            order.set_status("failed")
            return {"messgae": str(err)}, 500
            return {"message": get_text("ORDER_FAILED")}, 500
