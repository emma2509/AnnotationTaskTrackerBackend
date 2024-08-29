import pytest
from src.config import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD
from src.modules.database_transactions import (
    get_database_connection,
    end_database_connection,
    add_to_table,
    get_record_field_from_table,
    update_field,
    delete_record,
)
import psycopg2
from unittest.mock import patch


class TestGetDatabaseConnection:

    def test_successful_database_connection(self):
        # Act
        db_connection, db_cursor = get_database_connection()

        # Assert
        # check database connection object was created successfully with the correct details
        connection_details = psycopg2.extensions.ConnectionInfo(db_connection)
        assert connection_details.dbname == DB_NAME
        assert connection_details.user == DB_USER
        assert connection_details.password == DB_PASSWORD
        assert connection_details.host == DB_HOST

        # check database cursor is connected to the database connection
        assert db_cursor.connection == db_connection

        # Clean up
        db_cursor.close()
        db_connection.close()

    # Test if exception is raised when incorrect values are passed in
    @pytest.mark.parametrize(
        "config_variable,config_value",
        [
            ("DB_NAME", "fake-name"),
            ("DB_USER", "fake-user"),
            ("DB_PASSWORD", "fake-password"),
            ("DB_HOST", "fake-host"),
        ],
    )
    def test_unsuccessful_database_connection(self, config_variable, config_value):
        # Arrange
        with patch(
            f"src.modules.database_transactions.{config_variable}", config_value
        ):
            # Act & Assert
            with pytest.raises(Exception):
                get_database_connection()


class TestEndDatabaseConnection:
    def test_connection_terminated(self):
        # Arrange
        db_connection, db_cursor = get_database_connection()

        # Act
        end_database_connection(db_connection, db_cursor)

        # Assert
        assert not db_connection.closed == "0"  # 0 indicates connection is open
        assert db_cursor.closed is True


class TestAddToTable:
    def test_successful_add_to_table(self):
        # Arrange
        with patch(
            "src.modules.database_transactions.psycopg2.connect"
        ) as mock_connect:
            mock_connection_obj = (
                mock_connect.return_value
            )  # connection object returned from psycopg2.connect
            mock_cursor_obj = (
                mock_connection_obj.cursor.return_value
            )  # cursor object returned from connection obj

            table_name = "test-table"
            attributes = ["first-attribute", "second-attribute"]
            values = ["value-one", "value-two"]

            expected_sql = "INSERT INTO test-table (first-attribute, second-attribute) VALUES (%s, %s);"
            expected_response = {"statusCode": 200, "body": "Data successfully added"}

            # Act
            actual_response = add_to_table(table_name, attributes, values)

            # Assert
            mock_cursor_obj.execute.assert_called_with(expected_sql, values)
            assert expected_response == actual_response

    @pytest.mark.parametrize(
        "expected_response,mock_side_effect",
        [
            ({"statusCode": 500, "body": "Error: test-error"}, Exception("test-error")),
            (
                {
                    "statusCode": 500,
                    "body": "Error with adding to the database. Error: test-error",
                },
                psycopg2.Error("test-error"),
            ),
        ],
    )
    def test_fail_add_to_table(self, expected_response, mock_side_effect):
        # Arrange
        with patch(
            "src.modules.database_transactions.psycopg2.connect"
        ) as mock_connect:
            mock_connection_obj = (
                mock_connect.return_value
            )  # connection object returned from psycopg2.connect
            mock_cursor_obj = (
                mock_connection_obj.cursor.return_value
            )  # cursor object returned from connection obj
            mock_cursor_obj.execute.side_effect = mock_side_effect

            # Act
            actual_response = add_to_table("", "", "")

            # Assert
            assert expected_response == actual_response


class TestGetFieldFromTable:
    @pytest.mark.parametrize("condition", ["", "WHERE test-condition"])
    def test_get_field(self, condition):
        # Arrange
        with patch(
            "src.modules.database_transactions.psycopg2.connect"
        ) as mock_connect:
            mock_connection_obj = (
                mock_connect.return_value
            )  # connection object returned from psycopg2.connect
            mock_cursor_obj = (
                mock_connection_obj.cursor.return_value
            )  # cursor object returned from connection obj
            mock_cursor_obj.fetchall.return_value = "mock response"

            table_name = "test-table"
            field = "test-field"
            expected_sql = f"SELECT test-field FROM test-table {condition};"
            expected_response = {"statusCode": 200, "body": "mock response"}

            # Act
            actual_response = get_record_field_from_table(table_name, field, condition)

            # Assert
            mock_cursor_obj.execute.assert_called_with(expected_sql)
            assert expected_response == actual_response

    def test_no_field_found(self):
        # Arrange
        with patch(
            "src.modules.database_transactions.psycopg2.connect"
        ) as mock_connect:
            mock_connection_obj = (
                mock_connect.return_value
            )  # connection object returned from psycopg2.connect
            mock_cursor_obj = (
                mock_connection_obj.cursor.return_value
            )  # cursor object returned from connection obj
            mock_cursor_obj.fetchall.return_value = None

            table_name = "test-table"
            field = "test-field"
            expected_sql = f"SELECT test-field FROM test-table ;"
            expected_response = {"statusCode": 500, "body": "Error: no records found"}

            # Act
            actual_response = get_record_field_from_table(table_name, field, "")

            # Assert
            mock_cursor_obj.execute.assert_called_with(expected_sql)
            assert expected_response == actual_response

    @pytest.mark.parametrize(
        "expected_response,mock_side_effect",
        [
            ({"statusCode": 500, "body": "Error: test-error"}, Exception("test-error")),
            (
                {
                    "statusCode": 500,
                    "body": "Error with reading from the database: test-error",
                },
                psycopg2.Error("test-error"),
            ),
        ],
    )
    def test_fail_get_field(self, expected_response, mock_side_effect):
        # Arrange
        with patch(
            "src.modules.database_transactions.psycopg2.connect"
        ) as mock_connect:
            mock_connection_obj = (
                mock_connect.return_value
            )  # connection object returned from psycopg2.connect
            mock_cursor_obj = (
                mock_connection_obj.cursor.return_value
            )  # cursor object returned from connection obj
            mock_cursor_obj.execute.side_effect = mock_side_effect

            # Act
            actual_response = get_record_field_from_table("", "", "")

            # Assert
            assert expected_response == actual_response


class TestUpdateField:
    @pytest.mark.parametrize("condition", ["", "WHERE test-condition"])
    def test_success_update_field(self, condition):
        # Arrange
        with patch(
            "src.modules.database_transactions.psycopg2.connect"
        ) as mock_connect:
            mock_connection_obj = (
                mock_connect.return_value
            )  # connection object returned from psycopg2.connect
            mock_cursor_obj = (
                mock_connection_obj.cursor.return_value
            )  # cursor object returned from connection obj

            table_name = "test-table"
            field = "test-field"
            value = "test-value"
            expected_sql = (
                f"UPDATE test-table SET test-field = 'test-value' {condition};"
            )
            expected_response = {"statusCode": 200, "body": "Data successfully updated"}

            # Act
            actual_response = update_field(table_name, field, value, condition)

            # Assert
            mock_cursor_obj.execute.assert_called_with(expected_sql)
            assert expected_response == actual_response

    @pytest.mark.parametrize(
        "expected_response,mock_side_effect",
        [
            ({"statusCode": 500, "body": "Error: test-error"}, Exception("test-error")),
            (
                {
                    "statusCode": 500,
                    "body": "Error with database when updating record. Error: test-error",
                },
                psycopg2.Error("test-error"),
            ),
        ],
    )
    def test_fail_update_field(self, expected_response, mock_side_effect):
        # Arrange
        with patch(
            "src.modules.database_transactions.psycopg2.connect"
        ) as mock_connect:
            mock_connection_obj = (
                mock_connect.return_value
            )  # connection object returned from psycopg2.connect
            mock_cursor_obj = (
                mock_connection_obj.cursor.return_value
            )  # cursor object returned from connection obj
            mock_cursor_obj.execute.side_effect = mock_side_effect

            # Act
            actual_response = update_field("", "", "", "")

            # Assert
            assert expected_response == actual_response


class TestDeleteRecord:
    def test_successful_delete(self):
        # Arrange
        with patch(
            "src.modules.database_transactions.psycopg2.connect"
        ) as mock_connect:
            mock_connection_obj = (
                mock_connect.return_value
            )  # connection object returned from psycopg2.connect
            mock_cursor_obj = (
                mock_connection_obj.cursor.return_value
            )  # cursor object returned from connection obj

            table_name = "test-table"
            condition = "WHERE field=value"

            expected_sql = "DELETE FROM test-table WHERE field=value;"
            expected_response = {
                "statusCode": 200,
                "body": "Successfully deleted record",
            }

            # Act
            actual_response = delete_record(table_name, condition)

            # Assert
            mock_cursor_obj.execute.assert_called_with(expected_sql)
            assert expected_response == actual_response

    @pytest.mark.parametrize(
        "expected_response,mock_side_effect",
        [
            ({"statusCode": 500, "body": "Error: test-error"}, Exception("test-error")),
            (
                {
                    "statusCode": 500,
                    "body": "Error with deleting from the database: test-error",
                },
                psycopg2.Error("test-error"),
            ),
        ],
    )
    def test_fail_delete(self, expected_response, mock_side_effect):
        # Arrange
        with patch(
            "src.modules.database_transactions.psycopg2.connect"
        ) as mock_connect:
            mock_connection_obj = (
                mock_connect.return_value
            )  # connection object returned from psycopg2.connect
            mock_cursor_obj = (
                mock_connection_obj.cursor.return_value
            )  # cursor object returned from connection obj
            mock_cursor_obj.execute.side_effect = mock_side_effect

            # Act
            actual_response = delete_record("", "")

            # Assert
            assert expected_response == actual_response
