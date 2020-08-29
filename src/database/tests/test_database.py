from database import Database

import os
import pandas as pd
import sqlalchemy as sqla
from sqlalchemy.engine.url import make_url, URL
from sqlalchemy_utils import database_exists

TEST_DIR = os.path.dirname(__file__)


def clean():
    """Clean up test files"""
    for f in [os.path.join(TEST_DIR, 'database.sqlite')]:
        if os.path.exists(f):
            os.remove(f)
clean()


class TestDatabase:
    url = make_url('sqlite:///')
    db = os.path.join(TEST_DIR, 'database.sqlite')
    db_url = 'sqlite:///' + db
    schema = 'test'
    table = 'table'
    database = Database(url, db)

    def test_load(self):
        """Test that Database loads data from a sqlite database"""

        # Set up: create table inside database
        table_name = '_'.join([self.schema, self.table])
        engine = sqla.create_engine(self.db_url)
        engine.execute(
            f'CREATE TABLE "{table_name}" ('
                'id INTEGER NOT NULL,'
                'name VARCHAR, '
                'PRIMARY KEY (id));'
        )
        engine.execute(
            f'INSERT INTO "{table_name}" '
                '(id, name) '
                'VALUES (1,"raw1")'
        )

        # Function call
        data = self.database.load(self.table, self.schema)

        # Test that: the data is loaded correctly
        assert data.shape == (1, 2)
        assert list(data.columns) == ['id', 'name']
        assert data.values.tolist() == [[1, 'raw1']]

        # Clean up
        clean()


    def test_save(self):
        """Test that Database saves data to a sqlite database"""

        # Set up: data to save
        data = pd.DataFrame({
            'id': [1, 2],
            'name': ['raw1', 'raw2']
        })

        # Function call
        self.database.save(data, self.table, self.schema)

        # Test that: the database exists
        assert database_exists(self.db_url)

        # Test that: the table exists
        table_name = '_'.join([self.schema, self.table])
        engine = sqla.create_engine(self.db_url)
        assert table_name in engine.table_names()

        # Clean up
        clean()
