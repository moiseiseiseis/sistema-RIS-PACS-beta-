"""estructura inicial

Revision ID: b6d6cffe47d4
Revises: 
Create Date: 2025-04-04 21:25:34.177421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6d6cffe47d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pacientes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('identificacion', sa.String(length=20), nullable=False),
    sa.Column('fecha_nacimiento', sa.Date(), nullable=True),
    sa.Column('genero', sa.String(length=1), nullable=True),
    sa.Column('telefono', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('historial', sa.Text(), nullable=True),
    sa.Column('fecha_registro', sa.DateTime(), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('identificacion')
    )
    op.create_table('citas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=False),
    sa.Column('fecha_hora', sa.DateTime(), nullable=False),
    sa.Column('tipo_estudio', sa.String(length=50), nullable=False),
    sa.Column('estado', sa.String(length=20), nullable=True),
    sa.Column('notas', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['paciente_id'], ['pacientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('citas')
    op.drop_table('pacientes')
    # ### end Alembic commands ###
