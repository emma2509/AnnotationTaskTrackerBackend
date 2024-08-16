from src.modules.user_table import add_user
from unittest.mock import patch
from src.app import app
import psycopg2
import pytest

valid_json_input = {
    "user-name": "test-user",
    "first-name": "test-first-name",
    "second-name": "test-second-name",
    "team": "test-team",
    "admin": "test-admin",
    "password": "test-password"
}


class TestAddUser:

    @patch('src.modules.user_table.add_to_table')
    def test_successful_add_user(self, mock_add_to_table):
        # Arrange
        expected_response = {
            "statusCode": 200,
            "body": "Data successfully added",
        }
        with app.test_request_context(method='POST', json=valid_json_input):
            # Act
            actual_response = add_user()

            # Assert
            assert expected_response == actual_response
            mock_add_to_table.assert_called_with("employee",
                                                 ['username', 'firstname', 'secondname', 'team', 'admin', 'password'],
                                                 list(valid_json_input.values()))

    @patch('src.modules.user_table.add_to_table')
    def test_invalid_input(self, mock_add_to_table):
        # Arrange
        invalid_json_input = {
            "user-name": "test-user",
        }
        expected_response = {
            "statusCode": 400,
            "body": "Missing or incorrect JSON attributes. Error related to extracting key value: 'first-name'",
        }
        with app.test_request_context(method='POST', json=invalid_json_input):
            # Act
            actual_response = add_user()

            # Assert
            assert expected_response == actual_response
            mock_add_to_table.assert_not_called()

    @pytest.mark.parametrize("exception,expected_error_message",
                             [(Exception('test-error'), "Error: test-error"),
                              (psycopg2.DatabaseError('test-error'), "Error with write to database: test-error")])
    def test_errors_raised(self, exception, expected_error_message):
        # Arrange
        with patch('src.modules.user_table.add_to_table', side_effect=exception):
            expected_response = {
                "statusCode": 500,
                "body": expected_error_message,
            }
            with app.test_request_context(method='POST', json=valid_json_input):
                # Act
                actual_response = add_user()

                # Assert
                assert expected_response == actual_response
