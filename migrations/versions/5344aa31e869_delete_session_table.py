"""Delete session table

Revision ID: 5344aa31e869
Revises: ba07013f7487
Create Date: 2023-01-24 01:06:09.937794

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5344aa31e869"
down_revision = "ba07013f7487"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_post_reactions_id", table_name="post_reactions")
    op.drop_table("post_reactions")
    op.drop_index("ix_posts_id", table_name="posts")
    op.drop_table("posts")
    op.drop_index("ix_sessions_token", table_name="sessions")
    op.drop_table("sessions")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('users_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("nickname", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(length=40), autoincrement=False, nullable=True),
        sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_table(
        "sessions",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("token", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "expires", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="sessions_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="sessions_pkey"),
    )
    op.create_index("ix_sessions_token", "sessions", ["token"], unique=False)
    op.create_table(
        "posts",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('posts_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("text", sa.VARCHAR(length=2000), autoincrement=False, nullable=True),
        sa.Column("date", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="posts_user_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="posts_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_posts_id", "posts", ["id"], unique=False)
    op.create_table(
        "post_reactions",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("post_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("reaction", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("date", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"], ["posts.id"], name="post_reactions_post_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="post_reactions_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="post_reactions_pkey"),
    )
    op.create_index("ix_post_reactions_id", "post_reactions", ["id"], unique=False)
    # ### end Alembic commands ###
