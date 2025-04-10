"""empty message

Revision ID: 6478e94fc93a
Revises: 
Create Date: 2025-04-10 11:38:40.196631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6478e94fc93a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'USER', name='userroleenum'), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema='security'
    )

    # Insert the admin user
    op.execute(
        """
        INSERT INTO security.user (name, role, email, password)
        VALUES (
            'admin', 
            'ADMIN', 
            'admin@admin.com', 
            '$2b$12$Mo90lZ8UKbWf41X/N8T.UemUUuYD.CmdSpBAIBp0v4nl/YET4W.GG'
        )
        """
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user', schema='security')
    # ### end Alembic commands ###
