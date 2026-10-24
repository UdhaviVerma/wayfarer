"""initial schema

Revision ID: 20261024_01
Revises:
Create Date: 2026-10-24
"""

from alembic import op
import sqlalchemy as sa


revision = "20261024_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "countries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("work_life_balance_score", sa.Float(), nullable=False),
        sa.Column("visa_difficulty_score", sa.Float(), nullable=False),
        sa.Column("pr_difficulty_score", sa.Float(), nullable=False),
        sa.Column("healthcare_score", sa.Float(), nullable=False),
        sa.Column("safety_score", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_countries_id"), "countries", ["id"], unique=False)
    op.create_unique_constraint("uq_country_name", "countries", ["name"])
    op.create_unique_constraint("uq_country_code", "countries", ["code"])

    op.create_table(
        "salaries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=120), nullable=False),
        sa.Column("average_annual_salary_usd", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["country_id"], ["countries.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_salaries_id"), "salaries", ["id"], unique=False)

    op.create_table(
        "taxes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("effective_tax_percent", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["country_id"], ["countries.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_taxes_id"), "taxes", ["id"], unique=False)

    op.create_table(
        "cost_of_living",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("rent_usd", sa.Float(), nullable=False),
        sa.Column("living_expenses_usd", sa.Float(), nullable=False),
        sa.Column("transport_usd", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["country_id"], ["countries.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cost_of_living_id"), "cost_of_living", ["id"], unique=False)

    op.create_table(
        "visa_programs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("visa_name", sa.String(length=120), nullable=False),
        sa.Column("pathway_summary", sa.Text(), nullable=False),
        sa.Column("processing_time_months", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["country_id"], ["countries.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_visa_programs_id"), "visa_programs", ["id"], unique=False)

    op.create_table(
        "job_market",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("skill", sa.String(length=120), nullable=False),
        sa.Column("demand_score", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["country_id"], ["countries.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_job_market_id"), "job_market", ["id"], unique=False)

    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("reasoning", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["country_id"], ["countries.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_recommendations_id"), "recommendations", ["id"], unique=False)

    op.create_table(
        "chat_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("response", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_chat_history_id"), "chat_history", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_chat_history_id"), table_name="chat_history")
    op.drop_table("chat_history")
    op.drop_index(op.f("ix_recommendations_id"), table_name="recommendations")
    op.drop_table("recommendations")
    op.drop_index(op.f("ix_job_market_id"), table_name="job_market")
    op.drop_table("job_market")
    op.drop_index(op.f("ix_visa_programs_id"), table_name="visa_programs")
    op.drop_table("visa_programs")
    op.drop_index(op.f("ix_cost_of_living_id"), table_name="cost_of_living")
    op.drop_table("cost_of_living")
    op.drop_index(op.f("ix_taxes_id"), table_name="taxes")
    op.drop_table("taxes")
    op.drop_index(op.f("ix_salaries_id"), table_name="salaries")
    op.drop_table("salaries")
    op.drop_constraint("uq_country_code", "countries", type_="unique")
    op.drop_constraint("uq_country_name", "countries", type_="unique")
    op.drop_index(op.f("ix_countries_id"), table_name="countries")
    op.drop_table("countries")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
