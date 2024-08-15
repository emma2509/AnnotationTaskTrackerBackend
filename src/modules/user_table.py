from flask import request
import psycopg2
from .database_transactions import add_to_table
from ..config import EMPLOYEE_TABLE_NAME, EMPLOYEE_TABLE_ATTRIBUTES


def add_user():
    try:
        # Extract the values in the JSON request
        request_data = request.get_json()
        value_list = list(request_data.values())

        # Add record to database
        add_to_table(EMPLOYEE_TABLE_NAME, EMPLOYEE_TABLE_ATTRIBUTES, value_list)
        return 'Data successfully added'

    except KeyError as error:
        return f'Missing or incorrect JSON attributes. Error related to extracting key value: {error}'
    except psycopg2.DatabaseError as error:
        return f'Error with write to database: {error}'
    except Exception as e:
        return f'Error: {e}'
