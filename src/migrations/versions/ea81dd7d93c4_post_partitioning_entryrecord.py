"""Post Partitioning EntryRecord

Revision ID: ea81dd7d93c4
Revises: f3773720bca4
Create Date: 2022-11-15 13:17:33.914286

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ea81dd7d93c4"
down_revision = "f3773720bca4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "login_history", ["id", "device_type"])
    op.create_unique_constraint(None, "login_history_desktop", ["id", "device_type"])
    op.create_unique_constraint(None, "login_history_notebook", ["id", "device_type"])
    op.create_unique_constraint(None, "login_history_other", ["id", "device_type"])
    op.create_unique_constraint(None, "login_history_phone", ["id", "device_type"])
    op.create_unique_constraint(None, "login_history_tablet", ["id", "device_type"])
    op.create_unique_constraint(None, "login_history_tv", ["id", "device_type"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "login_history_tv", type_="unique")
    op.drop_constraint(None, "login_history_tablet", type_="unique")
    op.drop_constraint(None, "login_history_phone", type_="unique")
    op.drop_constraint(None, "login_history_other", type_="unique")
    op.drop_constraint(None, "login_history_notebook", type_="unique")
    op.drop_constraint(None, "login_history_desktop", type_="unique")
    op.drop_constraint(None, "login_history", type_="unique")
    # ### end Alembic commands ###