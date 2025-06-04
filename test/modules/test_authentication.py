from unittest.mock import patch

import bcrypt

from src.modules.authentication import authenticate
from src.app import app
import pytest


class TestAuthenticate:
    generic_fail_message = {"statusCode": 400, "body": "Error: Fail"}
    generic_success_message = {"statusCode": 200, "body": "Success"}
    empty_input = {}
    valid_input = {"requester-user-name": "username", "requester-password": "pass123"}
    correct_password_hash = bcrypt.hashpw(
        valid_input["requester-password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf8")
    incorrect_password_hash = bcrypt.hashpw(
        "wrong pass".encode("utf-8"), bcrypt.gensalt()
    ).decode("utf8")

    @pytest.mark.parametrize(
        "mock_get_side_effect,expected_response",
        [
            (  # test_exception_raised_during_db_action
                Exception("Fail"),
                generic_fail_message,
            ),
            (  # test_fail_to_get_password
                [generic_fail_message, generic_fail_message],
                generic_fail_message,
            ),
            (  # test_fail_to_get_access_level
                [generic_success_message, generic_fail_message],
                generic_fail_message,
            ),
            (  # test_incorrect_password
                [
                    {"body": [[incorrect_password_hash]], "statusCode": 200},
                    {"body": [[True]], "statusCode": 200},
                ],
                {"body": "Authentication failed.", "statusCode": 401},
            ),
            (  # test_correct_password_with_admin_user
                [
                    {"body": [[correct_password_hash]], "statusCode": 200},
                    {"body": [[True]], "statusCode": 200},
                ],
                {"body": "Authenticated, you have admin access", "statusCode": 200},
            ),
            (  # test_correct_password_with_regular_user
                [
                    {"body": [[correct_password_hash]], "statusCode": 200},
                    {"body": [[False]], "statusCode": 200},
                ],
                {"body": "Authenticated, you have regular access", "statusCode": 200},
            ),
        ],
    )
    @patch("src.modules.authentication.get_record_field_from_table_with_condition")
    def test_inputs(self, mock_get_field, mock_get_side_effect, expected_response):
        # Arrange
        mock_get_field.side_effect = mock_get_side_effect

        with app.test_request_context(method="GET", headers=self.valid_input):
            # Act
            actual_response = authenticate()

            # Assert
            assert expected_response == actual_response

    @patch("src.modules.authentication.get_record_field_from_table_with_condition")
    def test_invalid_input(self, mock_get_field):
        # Arrange
        expected_response = {
            "statusCode": 400,
            "body": "Missing or incorrect JSON attributes. Error related to extracting key value: 'HTTP_REQUESTER_USER_NAME'",
        }
        with app.test_request_context(method="GET", headers=self.empty_input):
            # Act
            actual_response = authenticate()

            # Assert
            assert expected_response == actual_response
            mock_get_field.assert_not_called()
