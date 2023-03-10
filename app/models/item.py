from typing import List

from app.db import db

# from app.library.stripe_helper import delete_stripe_product


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)
    # stripe_id = db.Column(db.String())

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel", back_populates="items")

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id: str) -> "ItemModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        # delete_stripe_product(self.stripe_id)
        db.session.delete(self)
        db.session.commit()
