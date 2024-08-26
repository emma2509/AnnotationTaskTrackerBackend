import psycopg2
from ..config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .api_response import response_format


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


# Create
def add_to_table(table_name, attributes, values):
    try:
        db_connection, db_cursor = get_database_connection()

        attribute_list = ", ".join(attributes)  # creates a string list for the SQL command
        value_placeholder = "%s" + ", %s" * (len(attributes) - 1)  # create string placeholder for SQL command
        sql = f'INSERT INTO {table_name} ({attribute_list}) VALUES ({value_placeholder});'
        db_cursor.execute(sql, values)

        end_database_connection(db_connection, db_cursor)
    except psycopg2.Error as error:
        return response_format(500, f'Error with adding to the database. Error: {error}')
    except Exception as error:
        return response_format(500, f'Error: {error}')
    else:
        return response_format(200, 'Data successfully added')


# Update. Condition is in the form of 'WHERE something = something'
def update_field(table_name, field, value, condition):
    try:
        db_connection, db_cursor = get_database_connection()

        sql = f"UPDATE {table_name} SET {field} = '{value}' {condition};"
        db_cursor.execute(sql)

        end_database_connection(db_connection, db_cursor)

        return response_format(200, 'Data successfully updated')
    except psycopg2.Error as error:
        return response_format(500, f'Error with database when updating record. Error: {error}')
    except Exception as error:
        return response_format(500, f'Error: {error}')


# Read
def get_record_field_from_table(table_name, field, condition):
    try:
        db_connection, db_cursor = get_database_connection()

        sql = f"SELECT {field} FROM {table_name} {condition};"
        db_cursor.execute(sql)
        database_output = db_cursor.fetchall()

        end_database_connection(db_connection, db_cursor)

        if not database_output:
            return response_format(500, "Error: no records found")

        return response_format(200, database_output)

    except psycopg2.Error as error:
        return response_format(500, f'Error with reading from the database: {error}')
    except Exception as error:
        return response_format(500, f'Error: {error}')


# Delete. Condition is in the form of 'WHERE something = something' and helps identify what records is being deleted
def delete_record(table_name, condition):
    try:
        db_connection, db_cursor = get_database_connection()

        sql = f"DELETE FROM {table_name} {condition};"
        db_cursor.execute(sql)

        end_database_connection(db_connection, db_cursor)

        return response_format(200, "Successfully deleted record")

    except psycopg2.Error as error:
        return response_format(500, f'Error with deleting from the database: {error}')
    except Exception as error:
        return response_format(500, f'Error: {error}')
