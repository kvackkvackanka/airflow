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

"""fix mssql not null constraint and drop pk

Revision ID: a43123bc7c24
Revises: cf5dc11e79ad
Create Date: 2018-06-17 10:16:31.412131

"""
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a43123bc7c24'
down_revision = 'cf5dc11e79ad'
branch_labels = None
depends_on = None



def upgrade():
    """Apply Remove id column from xcom"""
    conn = op.get_bind()

    if conn.dialect.name == 'mssql':
        inspector = Inspector.from_engine(conn)
        pk_name = inspector.get_pk_constraint("xcom")["name"]
        with op.batch_alter_table('xcom') as bop:
            bop.alter_column('key', default='return_value', nullable=False)
            bop.drop_constraint(pk_name, type_='primary')

def downgrade():
    """Unapply Remove id column from xcom"""
    conn = op.get_bind()

    if conn.dialect.name == 'mssql':
        with op.batch_alter_table('xcom') as bop:
            bop.create_constraint('pk_key', type_='primary')
            bop.alter_column('xcom', 'key', nullable=True)
