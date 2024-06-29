"""Added relationships

Revision ID: af60d97fa145
Revises: 611cd0717b85
Create Date: 2024-06-28 09:10:02.251093

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'af60d97fa145'
down_revision = '611cd0717b85'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Drop foreign key constraints if they exist
    fk_cities_country = 'fk_cities_country_id'
    if fk_cities_country in [fk['name'] for fk in inspector.get_foreign_keys('cities')]:
        op.drop_constraint(fk_cities_country, 'cities', type_='foreignkey')
    
    with op.batch_alter_table('cities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('country_code', sa.String(length=36), nullable=False, server_default='DEFAULT_CODE'))
        batch_op.create_foreign_key('fk_cities_country_code', 'countries', ['country_code'], ['id'])
        batch_op.drop_column('country_id')

    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.add_column(sa.Column('host_id', sa.String(length=36), nullable=False))
        if 'fk_places_user_id' in [fk['name'] for fk in inspector.get_foreign_keys('places')]:
            batch_op.drop_constraint('fk_places_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_places_host_id', 'users', ['host_id'], ['id'])
        batch_op.drop_column('user_id')

    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('host_id', sa.String(length=36), nullable=False))
        if 'fk_reviews_user_id' in [fk['name'] for fk in inspector.get_foreign_keys('reviews')]:
            batch_op.drop_constraint('fk_reviews_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_reviews_host_id', 'users', ['host_id'], ['id'])
        batch_op.drop_column('user_id')

    # Workaround to remove the default value
    op.execute('PRAGMA foreign_keys=off;')

    with op.batch_alter_table('cities', schema=None) as batch_op:
        batch_op.alter_column('country_code', server_default=None)

    op.execute('PRAGMA foreign_keys=on;')


def downgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint('fk_reviews_host_id', type_='foreignkey')
        batch_op.add_column(sa.Column('user_id', sa.VARCHAR(length=36), nullable=False))
        batch_op.create_foreign_key('fk_reviews_user_id', 'users', ['user_id'], ['id'])
        batch_op.drop_column('host_id')

    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.drop_constraint('fk_places_host_id', type_='foreignkey')
        batch_op.add_column(sa.Column('user_id', sa.VARCHAR(length=36), nullable=False))
        batch_op.create_foreign_key('fk_places_user_id', 'users', ['user_id'], ['id'])
        batch_op.drop_column('host_id')

    with op.batch_alter_table('cities', schema=None) as batch_op:
        batch_op.drop_constraint('fk_cities_country_code', type_='foreignkey')
        batch_op.add_column(sa.Column('country_id', sa.VARCHAR(length=36), nullable=False))
        batch_op.create_foreign_key('fk_cities_country_id', 'countries', ['country_id'], ['id'])
        batch_op.drop_column('country_code')
