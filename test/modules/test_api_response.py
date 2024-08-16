from src.modules.api_response import response_format


def test_api_response():
    # Arrange
    status_code = 200
    body = "message body"
    expected_response_format = {
        "statusCode": status_code,
        "body": body,
    }

    # Act
    actual_response_format = response_format(status_code, body)

    # Assert
    assert expected_response_format == actual_response_format
