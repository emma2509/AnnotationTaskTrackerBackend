from unittest.mock import patch
from src.modules.annotation_table import get_all_annotations


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
