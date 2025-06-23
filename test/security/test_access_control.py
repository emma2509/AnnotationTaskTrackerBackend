# <-***** os (2025) [7] - START
import os
# ->***** os (2025) [7] - END

from src.app import app, log_in_route, delete_annotation_route

account_user_name = os.environ["TEST_ACCOUNT_USERNAME"]
account_password = os.environ["TEST_ACCOUNT_PASSWORD"]


def test_access_denied_with_invalid_password():
    headers = {
        "requester-user-name": account_user_name,
        "requester-password": "incorrect-password",
    }
    with app.test_request_context(method="POST", headers=headers):
        response = log_in_route()
        assert {"body": "Authentication failed.", "statusCode": 401} == response


def test_action_denied_with_invalid_permissions():
    headers = {
        "requester-user-name": account_user_name,
        "requester-password": account_password,
    }
    with app.test_request_context(
        method="POST", json={"annotation-id": "X"}, headers=headers
    ):
        response = delete_annotation_route()
        assert {"body": "Incorrect permissions.", "statusCode": 403} == response
