from unittest.mock import patch
from src.modules.annotation_table import get_all_annotations, add_annotation_task
from src.app import app


@patch('src.modules.annotation_table.get_record_field_from_table')
def test_get_all_annotations(mock_get_fields):
    # Arrange
    mock_get_fields.return_value = {"statusCode": 200, "body": "fields"}
    expected_response = {"statusCode": 200, "body": "fields"}

    # Act
    actual_response = get_all_annotations()

    # Assert
    assert expected_response == actual_response
    mock_get_fields.assert_called_with("annotation", "*", "")


class TestAddAnnotation:
    @patch('src.modules.annotation_table.add_to_table')
    def test_success_add_annotation(self, mock_add_record):
        # Arrange
        mock_add_record.return_value = {"statusCode": 200, "body": "Success"}
        expected_response = {"statusCode": 200, "body": "Success"}
        json_input = {
            "user-name": "fake-username",
            "annotation-status": "fake-status",
            "original-data": "fake-data",
            "annotated-data": "fake-data",
            "tags": "fake-tags"
        }

        # Act
        with app.test_request_context(method='POST', json=json_input):
            actual_response = add_annotation_task()

            # Assert
            assert expected_response == actual_response
            mock_add_record.assert_called_with(
                "annotation",
                ["username", "annotationstatus", "originaldata", "annotateddata", "tags"],
                ["fake-username", "fake-status", "fake-data", "fake-data", "fake-tags"]
            )

    @patch('src.modules.annotation_table.add_to_table')
    def test_fail_add_annotation(self, mock_add_record):
        # Arrange
        expected_response = {
            "statusCode": 400,
            "body": "Missing or incorrect JSON attributes. Error related to extracting key value: 'user-name'"
        }
        json_input = {}

        # Act
        with app.test_request_context(method='POST', json=json_input):
            actual_response = add_annotation_task()

            # Assert
            assert expected_response == actual_response
            mock_add_record.assert_not_called()

