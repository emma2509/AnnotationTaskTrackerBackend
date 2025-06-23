# <-***** flask (2010) [1] - START
from flask import request
# ->***** flask (2010) [1] - END
# <-***** bcrypt (2025) [2] - START
import bcrypt
# ->***** bcrypt (2025) [2] - END

from ..config import EMPLOYEE_TABLE_NAME
from .api_response import response_format
from .database_transactions import get_record_field_from_table_with_condition


def authenticate():
    try:
        request_headers = request.headers
        username = request_headers["requester-user-name"]
        password = request_headers["requester-password"]
        # Get actual password for account to check against inputted password
        get_user_password = get_record_field_from_table_with_condition(
            EMPLOYEE_TABLE_NAME, ["password"], "username", username
        )

        # Get user admin field value
        is_user_admin = get_record_field_from_table_with_condition(
            EMPLOYEE_TABLE_NAME, ["admin"], "username", username
        )

        if get_user_password["statusCode"] != 200:
            return get_user_password
        if is_user_admin["statusCode"] != 200:
            return is_user_admin

        hashed_password = get_user_password["body"][0][0]
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            if is_user_admin["body"][0][0]:
                return response_format(200, "Authenticated, you have admin access")
            else:
                return response_format(200, "Authenticated, you have regular access")
        else:
            return response_format(401, "Authentication failed.")
    except KeyError as error:
        return response_format(
            400,
            f"Missing or incorrect JSON attributes. Error related to extracting key value: {error}",
        )
    except Exception as error:
        return response_format(400, f"Error: {error}")
