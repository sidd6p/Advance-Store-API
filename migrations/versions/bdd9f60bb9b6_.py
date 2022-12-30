"""empty message

Revision ID: bdd9f60bb9b6
Revises: 08b6e4137a75
Create Date: 2022-12-31 01:21:32.394249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bdd9f60bb9b6"
down_revision = "08b6e4137a75"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.alter_column(
            "price",
            existing_type=sa.REAL(),
            type_=sa.Float(precision=2),
            existing_nullable=False,
        )

    with op.batch_alter_table("orders", schema=None) as batch_op:
        batch_op.add_column(sa.Column("amount", sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column("description", sa.String(length=80), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("orders", schema=None) as batch_op:
        batch_op.drop_column("description")
        batch_op.drop_column("amount")

    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.alter_column(
            "price",
            existing_type=sa.Float(precision=2),
            type_=sa.REAL(),
            existing_nullable=False,
        )

    # ### end Alembic commands ###
