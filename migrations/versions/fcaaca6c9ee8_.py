"""empty message

Revision ID: fcaaca6c9ee8
Revises: 
Create Date: 2022-12-29 23:25:20.896510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fcaaca6c9ee8"
down_revision = None
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

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.alter_column(
            "price",
            existing_type=sa.Float(precision=2),
            type_=sa.REAL(),
            existing_nullable=False,
        )

    # ### end Alembic commands ###
