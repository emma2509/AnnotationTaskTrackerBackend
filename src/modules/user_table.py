from flask import request
import psycopg2
from .database_transactions import add_to_table
from ..config import EMPLOYEE_TABLE_NAME, EMPLOYEE_TABLE_ATTRIBUTES
from .api_response import response_format


def add_user():
    try:
        # Extract the values in the JSON request
        request_data = request.get_json()
        attribute_value_list = [
            request_data["user-name"],
            request_data["first-name"],
            request_data["second-name"],
            request_data["team"],
            request_data["admin"],
            request_data["password"]
        ]

        # Add record to database
        add_to_table(EMPLOYEE_TABLE_NAME, EMPLOYEE_TABLE_ATTRIBUTES, attribute_value_list)
        return response_format(200, 'Data successfully added')

    except KeyError as error:
        return response_format(400,
                               f'Missing or incorrect JSON attributes. Error related to extracting key value: {error}')
    except psycopg2.DatabaseError as error:
        return response_format(500, f'Error with write to database: {error}')
    except Exception as error:
        return response_format(500, f'Error: {error}')
