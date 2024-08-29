from flask import request

from .api_response import response_format
from .database_transactions import (
    get_record_field_from_table,
    add_to_table,
    update_field,
    delete_record,
)
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
            request_data["tags"],
        ]

        # Add record to database
        response = add_to_table(
            ANNOTATION_TABLE_NAME, ANNOTATION_TABLE_ATTRIBUTES, attribute_value_list
        )
        return response
    except KeyError as error:
        return response_format(
            400,
            f"Missing or incorrect JSON attributes. Error related to extracting key value: {error}",
        )
    except Exception as error:
        return response_format(400, f"Error: {error}")


def update_annotation_record():
    try:
        request_data = request.get_json()
        new_field_values = [
            request_data["user-name"],
            request_data["annotation-status"],
            request_data["original-data"],
            request_data["annotated-data"],
            request_data["tags"],
        ]
        condition = f'WHERE annotationid = {request_data["annotation-id"]}'

        # get the original record to check against
        original_field_values = get_record_field_from_table(
            ANNOTATION_TABLE_NAME,
            ",".join(ANNOTATION_TABLE_ATTRIBUTES),  # getting all fields except the id
            condition,
        )
        if original_field_values["statusCode"] != 200:  # return error
            return original_field_values

        original_field_values = original_field_values["body"][
            0
        ]  # extract all the records

        # check diff between original and new field values
        for i in range(len(new_field_values)):
            if new_field_values[i] != original_field_values[i]:
                # update the record with the new field values
                response = update_field(
                    ANNOTATION_TABLE_NAME,
                    ANNOTATION_TABLE_ATTRIBUTES[i],
                    new_field_values[i],
                    condition,
                )
                if response["statusCode"] != 200:  # return error
                    return response

        return response_format(200, "Success updating record")
    except KeyError as error:
        return response_format(
            400,
            f"Missing or incorrect JSON attributes. Error related to extracting key value: {error}",
        )
    except Exception as error:
        return response_format(400, f"Error: {error}")


def delete_annotation_record():
    try:
        request_data = request.get_json()
        annotation_id = request_data["annotation-id"]

        response = delete_record(
            ANNOTATION_TABLE_NAME, f"WHERE annotationid = {annotation_id}"
        )

        return response
    except KeyError as error:
        return response_format(
            400,
            f"Missing or incorrect JSON attributes. Error related to extracting key value: {error}",
        )
    except Exception as error:
        return response_format(400, f"Error: {error}")
