from flask import request
import bcrypt

from .authentication import authenticate
from .database_transactions import add_to_table, get_record_field_from_table
from ..config import EMPLOYEE_TABLE_NAME, EMPLOYEE_TABLE_ATTRIBUTES
from .api_response import response_format


def add_user():
    try:
        # Extract the values in the JSON request
        request_data = request.get_json()
        hashed_password = bcrypt.hashpw(request_data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        attribute_value_list = [
            request_data["user-name"],
            request_data["first-name"],
            request_data["last-name"],
            request_data["team"],
            request_data["admin"],
            hashed_password,
        ]

        # Add record to database
        response = add_to_table(
            EMPLOYEE_TABLE_NAME, EMPLOYEE_TABLE_ATTRIBUTES, attribute_value_list
        )
        return response

    except KeyError as error:
        return response_format(
            400,
            f"Missing or incorrect JSON attributes. Error related to extracting key value: {error}",
        )
    except Exception as error:
        return response_format(400, f"Error: {error}")


def get_users():
    auth = authenticate()
    if auth["statusCode"] != 200:
        return auth
    return get_record_field_from_table(EMPLOYEE_TABLE_NAME, ["username"])
