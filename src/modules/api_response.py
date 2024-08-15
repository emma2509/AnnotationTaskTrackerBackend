def response_format(status_code, body):
    response = {
        "statusCode": status_code,
        "body": body,
    }
    return response
