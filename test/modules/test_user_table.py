# <-***** bcrypt (2025) [2] - START
import bcrypt
# ->***** bcrypt (2025) [2] - END

from src.modules.user_table import (
    add_user,
    get_users,
)

# <-***** unittest (2025) [5] - START
from unittest.mock import patch

# ->***** unittest (2025) [5] - END
from src.app import app

# <-***** pytest (2015) [6] - START
import pytest
# ->***** pytest (2015) [6] - END


class TestAddUser:
    @pytest.fixture()
    def set_up(self):
        self.valid_json_input = {
            "user-name": "test-user",
            "first-name": "test-first-name",
            "last-name": "test-last-name",
            "team": "test-team",
            "admin": "test-admin",
            "password": "test-password",
        }

    @pytest.mark.parametrize(
        "expected_response,mock_return_value",
        [
            (
                {"body": "Data successfully added", "statusCode": 200},
                {"body": "Data successfully added", "statusCode": 200},
            ),
            (
                {"body": "Error: fake error", "statusCode": 500},
                {"body": "Error: fake error", "statusCode": 500},
            ),
        ],
    )
    @patch("src.modules.user_table.add_to_table")
    @patch("src.modules.user_table.authenticate")
    def test_add_user(
        self, mock_auth, mock_add_to_table, expected_response, mock_return_value, set_up
    ):
        # Arrange
        mock_auth.return_value = {"statusCode": 200, "body": "admin"}
        mock_add_to_table.return_value = mock_return_value
        with app.test_request_context(method="POST", json=self.valid_json_input):
            # Act
            actual_response = add_user()

            # Assert
            assert expected_response == actual_response
            assert mock_add_to_table.call_args.args[0] == "employee"
            assert mock_add_to_table.call_args.args[1] == [
                "username",
                "firstname",
                "lastname",
                "team",
                "admin",
                "password",
            ]
            assert (
                mock_add_to_table.call_args.args[2][:-1]
                == list(self.valid_json_input.values())[:-1]
            )
            assert bcrypt.checkpw(
                self.valid_json_input["password"].encode("utf-8"),
                mock_add_to_table.call_args.args[2][-1].encode("utf-8"),
            )

    @patch("src.modules.user_table.add_to_table")
    @patch("src.modules.user_table.authenticate")
    def test_invalid_input(self, mock_auth, mock_add_to_table):
        # Arrange
        mock_auth.return_value = {"statusCode": 200, "body": "admin"}
        invalid_json_input = {
            "user-name": "test-user",
        }
        expected_response = {
            "statusCode": 400,
            "body": "Missing or incorrect JSON attributes. Error related to extracting key value: 'password'",
        }
        with app.test_request_context(method="POST", json=invalid_json_input):
            # Act
            actual_response = add_user()

            # Assert
            assert expected_response == actual_response
            mock_add_to_table.assert_not_called()


class TestGetUsers:
    @patch("src.modules.user_table.get_record_field_from_table")
    @patch("src.modules.user_table.authenticate")
    def test_get_users(self, mock_auth, mock_get_record):
        # Arrange
        mock_auth.return_value = {"statusCode": 200, "body": "admin"}
        mock_get_record.return_value = {"statusCode": 200, "body": "Success"}
        expected_response = {"statusCode": 200, "body": "Success"}

        # Act
        actual_response = get_users()

        # Assert
        assert expected_response == actual_response
        mock_get_record.assert_called_with("employee", ["username"])
