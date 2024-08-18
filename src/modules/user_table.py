from flask import request
from .database_transactions import add_to_table, get_record_field_from_table
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
        response = add_to_table(EMPLOYEE_TABLE_NAME, EMPLOYEE_TABLE_ATTRIBUTES, attribute_value_list)
        return response

    except KeyError as error:
        return response_format(400,
                               f'Missing or incorrect JSON attributes. Error related to extracting key value: {error}')


def get_user_password():
    try:
        # Extract user name value
        request_data = request.get_json()
        username = request_data["user-name"]

        # Get password by running query then return response
        database_output = get_record_field_from_table(EMPLOYEE_TABLE_NAME, "password", f"WHERE username = '{username}'")
        return database_output
    except KeyError:
        return response_format(400, f'Missing user name in request')
