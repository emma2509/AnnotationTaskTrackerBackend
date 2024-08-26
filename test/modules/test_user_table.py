from src.modules.user_table import add_user, get_user_password, get_users, get_user_access_level
from unittest.mock import patch
from src.app import app
import pytest


class TestAddUser:

    @pytest.fixture()
    def set_up(self):
        self.valid_json_input = {
            "user-name": "test-user",
            "first-name": "test-first-name",
            "last-name": "test-last-name",
            "team": "test-team",
            "admin": "test-admin",
            "password": "test-password"
        }

    @pytest.mark.parametrize("expected_response,mock_return_value",
                             [
                                 ({'body': 'Data successfully added', 'statusCode': 200},
                                  {'body': 'Data successfully added', 'statusCode': 200}),
                                 ({'body': 'Error: fake error', 'statusCode': 500},
                                  {'body': 'Error: fake error', 'statusCode': 500})
                             ])
    @patch('src.modules.user_table.add_to_table')
    def test_add_user(self, mock_add_to_table, expected_response, mock_return_value, set_up):
        # Arrange
        mock_add_to_table.return_value = mock_return_value
        with app.test_request_context(method='POST', json=self.valid_json_input):
            # Act
            actual_response = add_user()

            # Assert
            assert expected_response == actual_response
            mock_add_to_table.assert_called_with("employee",
                                                 ['username', 'firstname', 'lastname', 'team', 'admin', 'password'],
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


class TestGetUserPassword:
    # Bellow tests different situations for both when a password is found and isn't
    @pytest.mark.parametrize("expected_response,mock_return_value",
                             [
                                 ({'body': 'fake-password', 'statusCode': 200},
                                  {'body': 'fake-password', 'statusCode': 200}),
                                 ({'body': 'Error: fake error', 'statusCode': 500},
                                  {'body': 'Error: fake error', 'statusCode': 500}),
                                 ({'body': 'Error: no records found', 'statusCode': 500},
                                  {'body': 'Error: no records found', 'statusCode': 500})
                             ])
    @patch('src.modules.user_table.get_record_field_from_table')
    def test_return_user_password(self, mock_get_field, expected_response, mock_return_value):
        # Arrange
        fake_input = {
            "user-name": "test-user"
        }
        employee_table = "employee"
        attribute = "password"
        condition = "WHERE username = 'test-user'"
        mock_get_field.return_value = mock_return_value

        with app.test_request_context(method='POST', json=fake_input):
            # Act
            actual_response = get_user_password()

            # Assert
            assert expected_response == actual_response
            mock_get_field.assert_called_with(employee_table, attribute, condition)

    @patch('src.modules.user_table.get_record_field_from_table')
    def test_invalid_input(self, mock_get_field):
        # Arrange
        fake_input = {}
        expected_response = {"statusCode": 400, "body": "Missing user name in request"}
        with app.test_request_context(method='POST', json=fake_input):
            # Act
            actual_response = get_user_password()

            # Assert
            assert expected_response == actual_response
            mock_get_field.assert_not_called()

    @patch('src.modules.user_table.get_record_field_from_table')
    def test_exception_raised_user_password(self, mock_get_field, ):
        # Arrange
        mock_get_field.side_effect = Exception("error")
        fake_input = {
            "user-name": "test-user"
        }
        expected_response = {"statusCode": 400, "body": "Error: error"}

        with app.test_request_context(method='POST', json=fake_input):
            # Act
            actual_response = get_user_password()

            # Assert
            assert expected_response == actual_response


class TestGetUsers:
    @patch('src.modules.user_table.get_record_field_from_table')
    def test_get_users(self, mock_get_record):
        # Arrange
        mock_get_record.return_value = {"statusCode": 200, "body": "Success"}
        expected_response = {"statusCode": 200, "body": "Success"}

        # Act
        actual_response = get_users()

        # Assert
        assert expected_response == actual_response
        mock_get_record.assert_called_with("employee", "username", "")


class TestGetUserAccessLevel:
    valid_input = {
        "user-name": "test-user"
    }

    @patch('src.modules.user_table.get_record_field_from_table')
    def test_invalid_input(self, mock_get_field):
        # Arrange
        invalid_input = {}
        expected_response = {"statusCode": 400, "body": "Missing user name in request"}

        with app.test_request_context(method='POST', json=invalid_input):
            # Act
            actual_response = get_user_access_level()

            # Assert
            assert expected_response == actual_response
            mock_get_field.assert_not_called()

    @patch('src.modules.user_table.get_record_field_from_table')
    def test_success_response(self, mock_get_field):
        # Arrange
        mock_get_field.return_value = {'body': 'fake-password', 'statusCode': 200}
        expected_response = {'body': 'fake-password', 'statusCode': 200}

        with app.test_request_context(method='POST', json=self.valid_input):
            # Act
            actual_response = get_user_access_level()

            # Assert
            assert expected_response == actual_response
            mock_get_field.assert_called_with("employee", "admin", "WHERE username = 'test-user'")

    @patch('src.modules.user_table.get_record_field_from_table')
    def test_exception_raise(self, mock_get_field):
        # Arrange
        mock_get_field.side_effect = Exception("test-error")
        expected_response = {'body': 'Error: test-error', 'statusCode': 400}

        with app.test_request_context(method='POST', json=self.valid_input):
            # Act
            actual_response = get_user_access_level()

            # Assert
            assert expected_response == actual_response
