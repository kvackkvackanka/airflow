#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Remove id column from xcom

Revision ID: bbf4a7ad0465
Revises: a43123bc7c24
Create Date: 2019-10-29 13:53:09.445943

"""

from alembic import op
from sqlalchemy import Column, Integer
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'bbf4a7ad0465'
down_revision = 'a43123bc7c24'
branch_labels = None
depends_on = None


def upgrade():
    """Apply Remove id column from xcom"""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    with op.batch_alter_table('xcom') as bop:
        xcom_columns = [col.get('name') for col in inspector.get_columns("xcom")]

        if "id" in xcom_columns:
            if conn.dialect.name == 'mssql':
                pk_name = inspector.get_pk_constraint('xcom')['name']
                bop.drop_constraint(pk_name, type_='primary')

            bop.drop_column('id')
            bop.drop_index('idx_xcom_dag_task_date')

            if conn.dialect.name == "mssql":
                bop.alter_column('key', existing_type=mssql.VARCHAR(512), nullable=False)
                bop.alter_column('execution_date', existing_type=mssql.DATETIME2(), nullable=False)
                
            bop.create_primary_key('pk_xcom', ['dag_id', 'task_id', 'key', 'execution_date'])


def downgrade():
    """Unapply Remove id column from xcom"""
    with op.batch_alter_table('xcom') as bop:
        bop.drop_constraint('pk_xcom', type_='primary')
        bop.add_column(Column('id', Integer, primary_key=True))
        bop.create_index('idx_xcom_dag_task_date', ['dag_id', 'task_id', 'key', 'execution_date'])
