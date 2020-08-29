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
        url = os.environ.get('SQL_SERVER_URL') if not url else url
        self.url = make_url(url)
        self.db = os.environ.get('SQL_DATABASE') if not db else db
        # Dev defaults (if no environment variables are set)
        if self.url is None:
            url_config = {
                'drivername': 'mysql+pymysql',
                'username': 'root',
                'password': 'root',
                'host': 'localhost',
                'port': 3306
            }
            self.url = URL(**url_config)
        if self.db is None:
            self.db = 'Default'


    def _extend_url(self, url):
        # Input validation
        if type(url) == str:
            url = make_url(url)
        # Add self.db object to URL object
        url_config = url.translate_connect_args()
        url_config['drivername'] = url.drivername
        url_config['database'] = self.db
        db_url = URL(**url_config)

        return db_url


    def load(self, url, db, schema=None, table=None):
        """
        Load data from database using specified url, db, schema and table name

        """
        if table is None:
            raise 'Table should be specified'
        # Connect to database with sqlalchemy
        db_url = _extend_url(url, db)
        engine = sqla.create_engine(db_url)
        # Load data from database - include schema in table name if not using postgres
        rdbms = db_url.drivername.split('+')[0]
        if rdbms == 'postgresql':
            data = pd.read_sql_table(table, engine, schema=schema, index_col=None)
        else:
            if schema:
                table = '_'.join([schema, table])
            data = pd.read_sql_table(table, engine, index_col=None)

        return data


    def save(data, url, db, schema=None, table=None):
        """
        Save pandas DataFrame to database using specified url, db, schema and table name
        """

        # Input validation
        if table is None:
            raise 'Table should be specified'
        assert type(data) == pd.DataFrame

        # Connect to database with sqlalchemy (create database if it doesn't exist)
        db_url = _extend_url(url, db)
        if not database_exists(db_url):
            create_database(db_url, encoding='UTF8MB4')
        engine = sqla.create_engine(db_url)

        # Save data to database - include schema in table name if not using postgres
        rdbms = db_url.drivername.split('+')[0]
        if rdbms == 'postgresql':
            data.to_sql(table, engine, schema=schema, if_exists='replace', index=False)
        else:
            if schema:
                table = '_'.join([schema, table])
            data.to_sql(table, engine, if_exists='replace', index=False)


    if __name__ == "__main__":

        # Get database config
        url, db, _ = get_config()

        # List schemas / databases
        engine = sqla.create_engine(url)
        insp = sqla.inspect(engine)
        db_list = insp.get_schema_names()
        print('Existing databases:\n', db_list)

        # Allow the user to specify for which database to display tables
        import sys
        if len(sys.argv) == 2:
            db = sys.argv[1]

        # Get tables for database 'db' if it exists
        if db in db_list:
            db_url = _extend_url(url, db)
            engine = sqla.create_engine(db_url)
            table_list = engine.table_names()
            print(f'Tables in {db}:\n', table_list)
        else:
            print(f'Unknown database: {db}')
