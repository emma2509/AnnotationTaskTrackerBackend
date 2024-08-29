from unittest.mock import patch
from src.modules.annotation_table import (
    get_all_annotations,
    add_annotation_task,
    update_annotation_record,
    delete_annotation_record,
)
from src.app import app


class TestGetAllAnnotations:
    @patch("src.modules.annotation_table.get_record_field_from_table")
    def test_get_all_annotations(self, mock_get_fields):
        # Arrange
        mock_get_fields.return_value = {"statusCode": 200, "body": "fields"}
        expected_response = {"statusCode": 200, "body": "fields"}

        # Act
        actual_response = get_all_annotations()

        # Assert
        assert expected_response == actual_response
        mock_get_fields.assert_called_with("annotation", "*", "")


class TestAddAnnotation:
    json_input = {
        "user-name": "fake-username",
        "annotation-status": "fake-status",
        "original-data": "fake-data",
        "annotated-data": "fake-data",
        "tags": "fake-tags",
    }

    @patch("src.modules.annotation_table.add_to_table")
    def test_success_add_annotation(self, mock_add_record):
        # Arrange
        mock_add_record.return_value = {"statusCode": 200, "body": "Success"}
        expected_response = {"statusCode": 200, "body": "Success"}

        # Act
        with app.test_request_context(method="POST", json=self.json_input):
            actual_response = add_annotation_task()

            # Assert
            assert expected_response == actual_response
            mock_add_record.assert_called_with(
                "annotation",
                [
                    "username",
                    "annotationstatus",
                    "originaldata",
                    "annotateddata",
                    "tags",
                ],
                ["fake-username", "fake-status", "fake-data", "fake-data", "fake-tags"],
            )

    @patch("src.modules.annotation_table.add_to_table")
    def test_fail_add_annotation(self, mock_add_record):
        # Arrange
        expected_response = {
            "statusCode": 400,
            "body": "Missing or incorrect JSON attributes. Error related to extracting key value: 'user-name'",
        }
        json_input = {}

        # Act
        with app.test_request_context(method="POST", json=json_input):
            actual_response = add_annotation_task()

            # Assert
            assert expected_response == actual_response
            mock_add_record.assert_not_called()

    @patch("src.modules.annotation_table.add_to_table")
    def test_exception_raised_add_annotation(self, mock_add_record):
        # Arrange
        mock_add_record.side_effect = Exception("error")
        expected_response = {"statusCode": 400, "body": "Error: error"}

        # Act
        with app.test_request_context(method="POST", json=self.json_input):
            actual_response = add_annotation_task()

            # Assert
            assert expected_response == actual_response


class TestUpdateAnnotationRecord:
    json_input = {
        "annotation-id": "fake-id",
        "user-name": "fake-name",
        "annotation-status": "fake-status",
        "original-data": "fake-text",
        "annotated-data": "fake-text",
        "tags": "fake-tags",
    }
    condition = "WHERE annotationid = fake-id"
    annotation_table_name = "annotation"
    annotation_table_fields = (
        "username,annotationstatus,originaldata,annotateddata,tags"
    )
    mock_get_records_response = {
        "statusCode": 200,
        "body": [("fake-name", "fake-status", "fake-text", "fake-text", "fake-tags")],
    }

    def test_invalid_input(self):
        # Arrange
        invalid_input = {}
        expected_response = {
            "statusCode": 400,
            "body": "Missing or incorrect JSON attributes. Error related to extracting key value: 'user-name'",
        }

        # Act
        with app.test_request_context(method="POST", json=invalid_input):
            actual_response = update_annotation_record()

            # Assert
            assert expected_response == actual_response

    @patch("src.modules.annotation_table.get_record_field_from_table")
    def test_get_record_error(self, mock_get_record):
        # Arrange
        mock_get_record.return_value = {
            "statusCode": 500,
            "body": "Error: no records found",
        }
        expected_response = {"statusCode": 500, "body": "Error: no records found"}

        # Act
        with app.test_request_context(method="POST", json=self.json_input):
            actual_response = update_annotation_record()

            # Assert
            assert expected_response == actual_response
            mock_get_record.assert_called_with(
                self.annotation_table_name, self.annotation_table_fields, self.condition
            )

    @patch("src.modules.annotation_table.get_record_field_from_table")
    @patch("src.modules.annotation_table.update_field")
    def test_no_updates_done(self, mock_update_field, mock_get_record):
        # Arrange
        mock_get_record.return_value = self.mock_get_records_response
        expected_response = {"statusCode": 200, "body": "Success updating record"}

        # Act
        with app.test_request_context(method="POST", json=self.json_input):
            actual_response = update_annotation_record()

            # Assert
            assert expected_response == actual_response
            mock_get_record.assert_called_with(
                self.annotation_table_name, self.annotation_table_fields, self.condition
            )
            mock_update_field.assert_not_called()

    @patch("src.modules.annotation_table.get_record_field_from_table")
    @patch("src.modules.annotation_table.update_field")
    def test_update_field_error(self, mock_update_field, mock_get_record):
        # Arrange
        mock_get_record.return_value = self.mock_get_records_response
        self.json_input["user-name"] = "new-name"
        mock_update_field.return_value = {
            "statusCode": 500,
            "body": "Error with updating record",
        }
        expected_response = {"statusCode": 500, "body": "Error with updating record"}

        # Act
        with app.test_request_context(method="POST", json=self.json_input):
            actual_response = update_annotation_record()

            # Assert
            assert expected_response == actual_response
            mock_get_record.assert_called_with(
                self.annotation_table_name, self.annotation_table_fields, self.condition
            )
            mock_update_field.assert_called_with(
                self.annotation_table_name, "username", "new-name", self.condition
            )

    @patch("src.modules.annotation_table.get_record_field_from_table")
    @patch("src.modules.annotation_table.update_field")
    def test_success_update_record(self, mock_update_field, mock_get_record):
        # Arrange
        mock_get_record.return_value = self.mock_get_records_response
        self.json_input["user-name"] = "new-name"
        mock_update_field.return_value = {"statusCode": 200, "body": "Success"}
        expected_response = {"statusCode": 200, "body": "Success updating record"}

        # Act
        with app.test_request_context(method="POST", json=self.json_input):
            actual_response = update_annotation_record()

            # Assert
            assert expected_response == actual_response
            mock_get_record.assert_called_with(
                self.annotation_table_name, self.annotation_table_fields, self.condition
            )
            mock_update_field.assert_called_with(
                self.annotation_table_name, "username", "new-name", self.condition
            )


class TestDeleteAnnotationRecord:
    valid_json = {"annotation-id": "fake-id"}

    def test_invalid_input(self):
        # Arrange
        invalid_input = {}
        expected_response = {
            "statusCode": 400,
            "body": "Missing or incorrect JSON attributes. Error related to extracting key value: 'annotation-id'",
        }

        # Act
        with app.test_request_context(method="POST", json=invalid_input):
            actual_response = delete_annotation_record()

            # Assert
            assert expected_response == actual_response

    @patch("src.modules.annotation_table.delete_record")
    def test_exception_thrown(self, mock_delete_record):
        # Arrange
        mock_delete_record.side_effect = Exception("test-error")
        expected_response = {"statusCode": 400, "body": "Error: test-error"}

        # Act
        with app.test_request_context(method="POST", json=self.valid_json):
            actual_response = delete_annotation_record()

            # Assert
            assert expected_response == actual_response

    @patch("src.modules.annotation_table.delete_record")
    def test_successful_deletion(self, mock_delete_record):
        # Arrange
        mock_delete_record.return_value = {"statusCode": 200, "body": "Success"}
        expected_response = {"statusCode": 200, "body": "Success"}

        # Act
        with app.test_request_context(method="POST", json=self.valid_json):
            actual_response = delete_annotation_record()

            # Assert
            assert expected_response == actual_response
