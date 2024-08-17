from src.modules.user_table import add_user, get_user_password
from unittest.mock import patch
from src.app import app
import psycopg2
import pytest


class TestAddUser:

    @pytest.fixture()
    def set_up(self):
        self.valid_json_input = {
            "user-name": "test-user",
            "first-name": "test-first-name",
            "second-name": "test-second-name",
            "team": "test-team",
            "admin": "test-admin",
            "password": "test-password"
        }

    @patch('src.modules.user_table.add_to_table')
    def test_successful_add_user(self, mock_add_to_table, set_up):
        # Arrange
        expected_response = {
            "statusCode": 200,
            "body": "Data successfully added",
        }
        with app.test_request_context(method='POST', json=self.valid_json_input):
            # Act
            actual_response = add_user()

            # Assert
            assert expected_response == actual_response
            mock_add_to_table.assert_called_with("employee",
                                                 ['username', 'firstname', 'secondname', 'team', 'admin', 'password'],
                                                 list(self.valid_json_input.values()))

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
                             [
                                 (Exception('test-error'), "Error: test-error"),
                                 (psycopg2.DatabaseError('test-error'), "Error with write to database: test-error")
                             ])
    def test_errors_raised(self, exception, expected_error_message, set_up):
        # Arrange
        with patch('src.modules.user_table.add_to_table', side_effect=exception):
            expected_response = {
                "statusCode": 500,
                "body": expected_error_message,
            }
            with app.test_request_context(method='POST', json=self.valid_json_input):
                # Act
                actual_response = add_user()

                # Assert
                assert expected_response == actual_response


class TestGetUserPassword:

    @pytest.fixture
    def set_up(self):
        self.fake_input = {
            "user-name": "test-user"
        }
        self.employee_table = "employee"
        self.attribute = "password"
        self.condition = "WHERE username = 'test-user'"

    # Bellow tests different situations for both when a password is found and isn't
    @pytest.mark.parametrize("expected_response,mock_return_value",
                             [
                                 ({'body': 'fake-password', 'statusCode': 200}, "fake-password"),
                                 ({'body': 'Error: no records found', 'statusCode': 500}, "")
                             ])
    @patch('src.modules.user_table.get_field_from_table')
    def test_return_user_password(self, mock_get_field, expected_response, mock_return_value, set_up):
        # Arrange
        mock_get_field.return_value = mock_return_value

        with app.test_request_context(method='GET', json=self.fake_input):
            # Act
            actual_response = get_user_password()

            # Assert
            assert expected_response == actual_response
            mock_get_field.assert_called_with(self.employee_table, self.attribute, self.condition)

    @pytest.mark.parametrize("exception,expected_response",
                             [
                                 (Exception('test-error'), {'body': 'Error: test-error', 'statusCode': 500}),
                                 (psycopg2.DatabaseError('test-error'),
                                  {'body': 'Error with reading from the database: test-error', 'statusCode': 500})
                             ])
    @patch('src.modules.user_table.get_field_from_table')
    def test_error_returned(self, mock_get_field, exception, expected_response, set_up):
        # Arrange
        mock_get_field.side_effect = exception

        with app.test_request_context(method='GET', json=self.fake_input):
            # Act
            actual_response = get_user_password()

            # Assert
            assert expected_response == actual_response
            mock_get_field.assert_called_with(self.employee_table, self.attribute, self.condition)
