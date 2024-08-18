import psycopg2
from .database_transactions import get_field_from_table
from ..config import ANNOTATION_TABLE_NAME
from .api_response import response_format


def get_all_annotations():
    try:
        annotation_records = get_field_from_table(ANNOTATION_TABLE_NAME, "*", "")
        if not annotation_records:
            return response_format(500, "Error: no records found")
        return response_format(200, annotation_records)
    except psycopg2.Error as error:
        return response_format(500, f'Error with reading from the database: {error}')
    except Exception as error:
        return response_format(500, f'Error: {error}')
