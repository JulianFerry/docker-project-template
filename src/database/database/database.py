import os
import pandas as pd
import sqlalchemy as sqla
from sqlalchemy.engine.url import URL, make_url
from sqlalchemy_utils import database_exists, create_database


class Database:

    def __init__(self, url=None, db=None):
        """
        Load database config for SQLalchemy
        
        This function will try the following to load the config:
        - Use the arguments passed to this function
        - Fetch SQL_SERVER_URL and SQL_DATABASE environment variables
        - Default database on http://localhost:3306

        """
        if url:
            url = make_url(url)
        else:
            url = make_url(os.environ.get('SQL_SERVER_URL'))
        db = db if db else os.environ.get('SQL_DATABASE')
        # Dev defaults (if no env variables)
        if url is None:
            url_config = {
                'drivername': 'mysql+pymysql',
                'username': 'root',
                'password': 'root',
                'host': 'localhost',
                'port': 3306
            }
            url = URL(**url_config)
        if db is None:
            db = 'Default'
        self.url = url
        self.db = db
        # Connect
        self.create(self.db)
        self.connect(self.db)

    def _db_url(self, db):
        """Extend self.url with a database name"""
        url_config = self.url.translate_connect_args()
        url_config['drivername'] = self.url.drivername
        url_config['database'] = db
        db_url = URL(**url_config)
        return db_url

    def create(self, db):
        """Create database"""
        db_url = self._db_url(db)
        if not database_exists(db_url):
            create_database(db_url, encoding='UTF8MB4')

    def connect(self, db, create=False):
        """Connect to database in RDBMS"""
        db_url = self._db_url(db)
        if not database_exists(db_url):
            raise ValueError(f'database not found: {db}')
        self.engine = sqla.create_engine(db_url)
        # Store database info
        insp = sqla.inspect(self.engine)
        self.rdbms = db_url.drivername.split('+')[0]
        self.db = db
        self.databases = insp.get_schema_names()
        self.tables = self.engine.table_names()

    def load(self, table, schema=None):
        """
        Load data from database
        Include schema in table name if not using postgres

        """
        # Load data from database
        if self.rdbms == 'postgresql':
            data = pd.read_sql_table(table, self.engine, schema=schema, index_col=None)
        else:
            if schema:
                table = '_'.join([schema, table])
            data = pd.read_sql_table(table, self.engine, index_col=None)
        return data

    def save(self, data, table, schema=None):
        """
        Save pandas DataFrame to database
        Include schema in table name if not using postgres

        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError('data should be a pandas dataframe')
        if self.rdbms == 'postgresql':
            data.to_sql(table, self.engine, schema=schema, if_exists='replace', index=False)
        else:
            if schema:
                table = '_'.join([schema, table])
            data.to_sql(table, self.engine, if_exists='replace', index=False)


# if __name__ == "__main__":

#     # User input argument: database for which to display tables
#     import sys
#     arg = sys.argv[1] if len(sys.argv) == 2 else None

#     db = Database()
#     print(f'Databases: {db.databases}')

#     # Get tables for user input database if it exists
#     if arg:
#         db.connect(arg)
#         print(f'Tables in {arg}: {db.tables}')
