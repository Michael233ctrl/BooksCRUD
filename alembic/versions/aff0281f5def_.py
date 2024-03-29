"""empty message

Revision ID: aff0281f5def
Revises: 420d0020490e
Create Date: 2022-07-25 14:37:49.989021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aff0281f5def"
down_revision = "420d0020490e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("book_tags_tag_id_fkey", "book_tags", type_="foreignkey")
    op.drop_constraint("book_tags_book_id_fkey", "book_tags", type_="foreignkey")
    op.create_foreign_key(
        None, "book_tags", "book", ["book_id"], ["id"], ondelete="SET NULL"
    )
    op.create_foreign_key(
        None, "book_tags", "tag", ["tag_id"], ["id"], ondelete="SET NULL"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "book_tags", type_="foreignkey")
    op.drop_constraint(None, "book_tags", type_="foreignkey")
    op.create_foreign_key(
        "book_tags_book_id_fkey", "book_tags", "book", ["book_id"], ["id"]
    )
    op.create_foreign_key(
        "book_tags_tag_id_fkey", "book_tags", "tag", ["tag_id"], ["id"]
    )
    # ### end Alembic commands ###
