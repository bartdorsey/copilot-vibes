"""
Revision ID: 20240514_add_owner_extra_fields
Revises: 20240514_add_pet_extra_fields
Create Date: 2025-05-14
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20240514_add_owner_extra_fields"
down_revision = "20240514_add_pet_extra_fields"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "owners", sa.Column("email", sa.String(), nullable=True, unique=True)
    )
    op.add_column("owners", sa.Column("phone", sa.String(), nullable=True))
    op.add_column("owners", sa.Column("address", sa.String(), nullable=True))
    op.add_column("owners", sa.Column("city", sa.String(), nullable=True))
    op.add_column("owners", sa.Column("state", sa.String(), nullable=True))
    op.add_column("owners", sa.Column("zip_code", sa.String(), nullable=True))
    op.add_column("owners", sa.Column("country", sa.String(), nullable=True))
    op.add_column(
        "owners", sa.Column("date_of_birth", sa.String(), nullable=True)
    )


def downgrade():
    op.drop_column("owners", "date_of_birth")
    op.drop_column("owners", "country")
    op.drop_column("owners", "zip_code")
    op.drop_column("owners", "state")
    op.drop_column("owners", "city")
    op.drop_column("owners", "address")
    op.drop_column("owners", "phone")
    op.drop_column("owners", "email")
