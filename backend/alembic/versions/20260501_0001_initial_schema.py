"""initial schema

Revision ID: 20260501_0001
Revises: 
Create Date: 2026-05-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260501_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "agents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("phone_number", sa.String(length=15), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("location_area", sa.String(length=100), nullable=False),
        sa.Column("agency_name", sa.String(length=100), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("total_leads_matched", sa.Integer(), nullable=True),
        sa.Column("total_leads_converted", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone_number"),
    )
    op.create_index("ix_agents_created_at", "agents", ["created_at"], unique=False)
    op.create_index("ix_agents_email", "agents", ["email"], unique=True)
    op.create_index("ix_agents_full_name", "agents", ["full_name"], unique=False)
    op.create_index("ix_agents_id", "agents", ["id"], unique=False)
    op.create_index("ix_agents_is_active", "agents", ["is_active"], unique=False)
    op.create_index("ix_agents_location_area", "agents", ["location_area"], unique=False)
    op.create_index("ix_agents_password_hash", "agents", ["password_hash"], unique=False)
    op.create_index("ix_agents_phone_number", "agents", ["phone_number"], unique=True)
    op.create_index("ix_agents_rating", "agents", ["rating"], unique=False)
    op.create_index("idx_location_active", "agents", ["location_area", "is_active"], unique=False)

    op.create_table(
        "tenant_leads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("phone_number", sa.String(length=15), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("location_preference", sa.String(length=100), nullable=False),
        sa.Column("budget_min", sa.Integer(), nullable=True),
        sa.Column("budget_max", sa.Integer(), nullable=False),
        sa.Column("property_type", sa.String(length=50), nullable=False),
        sa.Column("move_in_date", sa.Date(), nullable=False),
        sa.Column("lead_score", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phone_number"),
    )
    op.create_index("ix_tenant_leads_created_at", "tenant_leads", ["created_at"], unique=False)
    op.create_index("ix_tenant_leads_full_name", "tenant_leads", ["full_name"], unique=False)
    op.create_index("ix_tenant_leads_id", "tenant_leads", ["id"], unique=False)
    op.create_index("ix_tenant_leads_location_preference", "tenant_leads", ["location_preference"], unique=False)
    op.create_index("ix_tenant_leads_move_in_date", "tenant_leads", ["move_in_date"], unique=False)
    op.create_index("ix_tenant_leads_phone_number", "tenant_leads", ["phone_number"], unique=True)
    op.create_index("ix_tenant_leads_status", "tenant_leads", ["status"], unique=False)
    op.create_index("idx_budget_type", "tenant_leads", ["budget_max", "property_type"], unique=False)
    op.create_index("idx_location_status", "tenant_leads", ["location_preference", "status"], unique=False)
    op.create_index("idx_move_in_date", "tenant_leads", ["move_in_date"], unique=False)

    op.create_table(
        "lead_purchases",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("agent_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("payment_reference", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.ForeignKeyConstraint(["lead_id"], ["tenant_leads.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("payment_reference"),
    )
    op.create_index("ix_lead_purchases_agent_id", "lead_purchases", ["agent_id"], unique=False)
    op.create_index("ix_lead_purchases_created_at", "lead_purchases", ["created_at"], unique=False)
    op.create_index("ix_lead_purchases_id", "lead_purchases", ["id"], unique=False)
    op.create_index("ix_lead_purchases_lead_id", "lead_purchases", ["lead_id"], unique=False)
    op.create_index("ix_lead_purchases_payment_reference", "lead_purchases", ["payment_reference"], unique=True)
    op.create_index("ix_lead_purchases_status", "lead_purchases", ["status"], unique=False)
    op.create_index("idx_agent_lead", "lead_purchases", ["agent_id", "lead_id"], unique=True)
    op.create_index("idx_payment_status", "lead_purchases", ["payment_reference", "status"], unique=False)

    op.create_table(
        "lead_matches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("agent_id", sa.Integer(), nullable=False),
        sa.Column("match_score", sa.Float(), nullable=False),
        sa.Column("match_reason", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.ForeignKeyConstraint(["lead_id"], ["tenant_leads.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_lead_matches_agent_id", "lead_matches", ["agent_id"], unique=False)
    op.create_index("ix_lead_matches_created_at", "lead_matches", ["created_at"], unique=False)
    op.create_index("ix_lead_matches_id", "lead_matches", ["id"], unique=False)
    op.create_index("ix_lead_matches_lead_id", "lead_matches", ["lead_id"], unique=False)
    op.create_index("ix_lead_matches_status", "lead_matches", ["status"], unique=False)
    op.create_index("idx_lead_agent", "lead_matches", ["lead_id", "agent_id"], unique=True)


def downgrade() -> None:
    op.drop_index("idx_lead_agent", table_name="lead_matches")
    op.drop_index("ix_lead_matches_status", table_name="lead_matches")
    op.drop_index("ix_lead_matches_lead_id", table_name="lead_matches")
    op.drop_index("ix_lead_matches_id", table_name="lead_matches")
    op.drop_index("ix_lead_matches_created_at", table_name="lead_matches")
    op.drop_index("ix_lead_matches_agent_id", table_name="lead_matches")
    op.drop_table("lead_matches")

    op.drop_index("idx_payment_status", table_name="lead_purchases")
    op.drop_index("idx_agent_lead", table_name="lead_purchases")
    op.drop_index("ix_lead_purchases_status", table_name="lead_purchases")
    op.drop_index("ix_lead_purchases_payment_reference", table_name="lead_purchases")
    op.drop_index("ix_lead_purchases_lead_id", table_name="lead_purchases")
    op.drop_index("ix_lead_purchases_id", table_name="lead_purchases")
    op.drop_index("ix_lead_purchases_created_at", table_name="lead_purchases")
    op.drop_index("ix_lead_purchases_agent_id", table_name="lead_purchases")
    op.drop_table("lead_purchases")

    op.drop_index("idx_move_in_date", table_name="tenant_leads")
    op.drop_index("idx_location_status", table_name="tenant_leads")
    op.drop_index("idx_budget_type", table_name="tenant_leads")
    op.drop_index("ix_tenant_leads_status", table_name="tenant_leads")
    op.drop_index("ix_tenant_leads_phone_number", table_name="tenant_leads")
    op.drop_index("ix_tenant_leads_move_in_date", table_name="tenant_leads")
    op.drop_index("ix_tenant_leads_location_preference", table_name="tenant_leads")
    op.drop_index("ix_tenant_leads_id", table_name="tenant_leads")
    op.drop_index("ix_tenant_leads_full_name", table_name="tenant_leads")
    op.drop_index("ix_tenant_leads_created_at", table_name="tenant_leads")
    op.drop_table("tenant_leads")

    op.drop_index("idx_location_active", table_name="agents")
    op.drop_index("ix_agents_rating", table_name="agents")
    op.drop_index("ix_agents_phone_number", table_name="agents")
    op.drop_index("ix_agents_password_hash", table_name="agents")
    op.drop_index("ix_agents_location_area", table_name="agents")
    op.drop_index("ix_agents_is_active", table_name="agents")
    op.drop_index("ix_agents_id", table_name="agents")
    op.drop_index("ix_agents_full_name", table_name="agents")
    op.drop_index("ix_agents_email", table_name="agents")
    op.drop_index("ix_agents_created_at", table_name="agents")
    op.drop_table("agents")