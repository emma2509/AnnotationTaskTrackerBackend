from flask import request

from .api_response import response_format
from .database_transactions import get_record_field_from_table, add_to_table
from ..config import ANNOTATION_TABLE_NAME, ANNOTATION_TABLE_ATTRIBUTES


def get_all_annotations():
    return get_record_field_from_table(ANNOTATION_TABLE_NAME, "*", "")


def add_annotation_task():
    try:
        # Extract the values in the JSON request
        request_data = request.get_json()
        attribute_value_list = [
            request_data["user-name"],
            request_data["annotation-status"],
            request_data["original-data"],
            request_data["annotated-data"],
            request_data["tags"]
        ]

        # Add record to database
        response = add_to_table(ANNOTATION_TABLE_NAME, ANNOTATION_TABLE_ATTRIBUTES, attribute_value_list)
        return response
    except KeyError as error:
        return response_format(400,
                               f'Missing or incorrect JSON attributes. Error related to extracting key value: {error}')
