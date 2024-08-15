import psycopg2
from ..config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


def get_database_connection():
    db_connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    db_cursor = db_connection.cursor()
    return db_connection, db_cursor


def end_database_connection(db_connection, db_cursor):
    db_cursor.close()
    db_connection.commit()
    db_connection.close()


def add_to_table(table_name, attributes, values):
    db_connection, db_cursor = get_database_connection()

    attribute_list = ", ".join(attributes)  # creates a string list for the SQL command
    value_placeholder = "%s" + ", %s" * (len(attributes) - 1)  # create string placeholder for SQL command
    sql = f'INSERT INTO {table_name} ({attribute_list}) VALUES ({value_placeholder});'
    db_cursor.execute(sql, values)

    end_database_connection(db_connection, db_cursor)
