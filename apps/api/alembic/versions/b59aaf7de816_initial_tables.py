"""initial_tables

Revision ID: b59aaf7de816
Revises:
Create Date: 2026-02-08 14:08:30.587048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b59aaf7de816'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

idea_status = sa.Enum('discovered', 'analyzed', 'planned', 'selected', 'in_progress', name='ideastatus')
agent_status = sa.Enum('pending', 'running', 'completed', 'failed', name='agentstatus')


def upgrade() -> None:
    """Create business_ideas and agent_runs tables."""
    idea_status.create(op.get_bind(), checkfirst=True)
    agent_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'business_ideas',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('source', sa.String(length=100), nullable=False),
        sa.Column('source_url', sa.String(length=2000), nullable=True),
        sa.Column('business_potential', sa.Float(), nullable=True),
        sa.Column('market_size_score', sa.Float(), nullable=True),
        sa.Column('competition_score', sa.Float(), nullable=True),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('composite_score', sa.Float(), nullable=True),
        sa.Column('status', idea_status, nullable=False, server_default='discovered'),
        sa.Column('raw_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('analysis_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('research_run_id', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'agent_runs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('research_run_id', sa.String(length=100), nullable=False),
        sa.Column('agent_name', sa.String(length=100), nullable=False),
        sa.Column('status', agent_status, nullable=False, server_default='pending'),
        sa.Column('llm_provider', sa.String(length=50), nullable=False, server_default='groq'),
        sa.Column('result_summary', sa.Text(), nullable=True),
        sa.Column('result_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_agent_runs_research_run_id', 'agent_runs', ['research_run_id'])


def downgrade() -> None:
    """Drop business_ideas and agent_runs tables."""
    op.drop_index('ix_agent_runs_research_run_id', table_name='agent_runs')
    op.drop_table('agent_runs')
    op.drop_table('business_ideas')
    agent_status.drop(op.get_bind(), checkfirst=True)
    idea_status.drop(op.get_bind(), checkfirst=True)
