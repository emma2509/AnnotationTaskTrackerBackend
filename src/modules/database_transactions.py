import psycopg2
from psycopg2.sql import Identifier, SQL

from ..config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .api_response import response_format


def get_database_connection():
    db_connection = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    db_cursor = db_connection.cursor()
    return db_connection, db_cursor


def end_database_connection(db_connection, db_cursor):
    db_cursor.close()
    db_connection.commit()
    db_connection.close()


# Create
def add_to_table(table_name, fields, values):
    try:
        db_connection, db_cursor = get_database_connection()

        list_field = []
        for field in fields:
            list_field.append(Identifier(field))
        value_placeholder = "%s" + ", %s" * (
            len(fields) - 1
        )  # create string placeholder for SQL command
        sql = SQL(
            "INSERT INTO {table_name} ({fields}) VALUES (" + value_placeholder + ")"
        ).format(
            table_name=Identifier(table_name),
            fields=SQL(",").join(list_field),
        )
        db_cursor.execute(sql, values)

        end_database_connection(db_connection, db_cursor)
    except psycopg2.Error as error:
        return response_format(
            500, f"Error with adding to the database. Error: {error}"
        )
    except Exception as error:
        return response_format(500, f"Error: {error}")
    else:
        return response_format(200, "Data successfully added")


# Update field based on passed in condition
def update_field(
    table_name, field_to_update, new_value, condition_field, condition_value
):
    try:
        db_connection, db_cursor = get_database_connection()

        sql = SQL(
            "UPDATE {table_name} SET {field_to_update} = (%s) WHERE {condition_field} = (%s);"
        ).format(
            table_name=Identifier(table_name),
            field_to_update=Identifier(field_to_update),
            condition_field=Identifier(condition_field),
        )
        db_cursor.execute(sql, (new_value, condition_value))

        end_database_connection(db_connection, db_cursor)

        return response_format(200, "Data successfully updated")
    except psycopg2.Error as error:
        return response_format(
            500, f"Error with database when updating record. Error: {error}"
        )
    except Exception as error:
        return response_format(500, f"Error: {error}")


# Read with condition applied
def get_record_field_from_table_with_condition(
    table_name, fields, condition_field, condition_value
):
    try:
        db_connection, db_cursor = get_database_connection()

        list_field = []
        for field in fields:
            list_field.append(Identifier(field))
        sql = SQL(
            "SELECT {fields} FROM {table_name} WHERE {condition_field} = (%s);"
        ).format(
            fields=SQL(",").join(list_field),
            table_name=Identifier(table_name),
            condition_field=Identifier(condition_field),
        )
        db_cursor.execute(sql, (condition_value,))
        database_output = db_cursor.fetchall()

        end_database_connection(db_connection, db_cursor)

        if not database_output:
            return response_format(500, "Error: no records found")

        return response_format(200, database_output)

    except psycopg2.Error as error:
        return response_format(500, f"Error with reading from the database: {error}")
    except Exception as error:
        return response_format(500, f"Error: {error}")


# Read with no condition applied
def get_record_field_from_table(table_name, fields):
    try:
        db_connection, db_cursor = get_database_connection()
        list_of_fields = ",".join(fields)
        sql = f"SELECT {list_of_fields} FROM {table_name};"
        db_cursor.execute(sql)
        database_output = db_cursor.fetchall()

        end_database_connection(db_connection, db_cursor)

        if not database_output:
            return response_format(500, "Error: no records found")

        return response_format(200, database_output)

    except psycopg2.Error as error:
        return response_format(500, f"Error with reading from the database: {error}")
    except Exception as error:
        return response_format(500, f"Error: {error}")


# Read with join
def get_record_joined_table(table_name, fields, join_statement):
    try:
        db_connection, db_cursor = get_database_connection()
        list_of_fields = ",".join(fields)
        sql = f"SELECT {list_of_fields} FROM {table_name} {join_statement};"

        db_cursor.execute(sql)
        database_output = db_cursor.fetchall()

        end_database_connection(db_connection, db_cursor)

        if not database_output:
            return response_format(500, "Error: no records found")

        return response_format(200, database_output)

    except psycopg2.Error as error:
        return response_format(500, f"Error with reading from the database: {error}")
    except Exception as error:
        return response_format(500, f"Error: {error}")


# Delete certain record based on condition
def delete_record(table_name, condition_field, condition_value):
    try:
        db_connection, db_cursor = get_database_connection()
        sql = SQL("DELETE FROM {table_name} WHERE {condition_field} = (%s);").format(
            table_name=Identifier(table_name),
            condition_field=Identifier(condition_field),
        )
        db_cursor.execute(sql, (condition_value,))

        end_database_connection(db_connection, db_cursor)

        return response_format(200, "Successfully deleted record")

    except psycopg2.Error as error:
        return response_format(500, f"Error with deleting from the database: {error}")
    except Exception as error:
        return response_format(500, f"Error: {error}")
