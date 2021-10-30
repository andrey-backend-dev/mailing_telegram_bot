from dotenv import load_dotenv
import os
from typing import Optional
from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.connection_cext import CMySQLConnection
import mysql.connector
load_dotenv()


cnx: Optional[CMySQLConnection] = None
cursor: Optional[CMySQLCursor] = None


def connect_mysql(first: bool = False):
    global cnx, cursor
    cnx = mysql.connector.connect(
        user=os.getenv('NAME'),
        password=os.getenv('PASSWORD')
    )
    cursor = cnx.cursor()
    if not first:
        use_database(os.getenv("DBNAME"))
    return cursor


def disconnect_mysql():
    global cnx, cursor
    if cnx and cursor:
        cnx.close()
        cursor.close()
        return
    print("You have not connected MySQL yet.")


def create_database(db_name):
    try:
        cursor.execute(f"CREATE DATABASE {db_name}")
    except mysql.connector.Error as err:
        print(f'Failed creating {db_name} database.\n{err}')
    print(f'Database {db_name} created successfully.')
    use_database(db_name)


def create_table(db_name, table_name, settings):
    use_database(db_name)
    try:
        cursor.execute(f"CREATE TABLE {table_name} ({settings})")
    except mysql.connector.Error as err:
        print(f'Failed creating {table_name} table.\n{err}')
    print(f'Table {table_name} created successfully.')


def use_database(db_name):
    try:
        cursor.execute(f"USE {db_name}")
    except mysql.connector.Error as err:
        print(f'Failed using {db_name} database.\n{err}')


def drop_database(db_name):
    try:
        cursor.execute(f"DROP DATABASE {db_name}")
    except mysql.connector.Error as err:
        if err.errno != 1008:
            print(f'Failed to drop the {db_name} database\n{err}')
            exit(1)
        print(f"You can't drop {db_name} database, cause it does not exists.")
    else:
        print(f'Database {db_name} successfully dropped.')


def commit():
    cnx.commit()


if __name__ == '__main__':
    db_name = os.getenv('DBNAME')
    connect_mysql(first=True)
    drop_database(db_name)
    create_database(db_name)
    create_table(db_name, 'users', "id INT UNSIGNED,"
                                         "username varchar(20) NOT NULL,"
                                         "language varchar(2) NOT NULL DEFAULT 'en',"
                                         "has_rights boolean NOT NULL DEFAULT FALSE,"
                                         "primary key(id)")
    disconnect_mysql()
