from .database_transactions import get_field_from_table
from ..config import ANNOTATION_TABLE_NAME


def get_all_annotations():
    # return get_field_from_table(ANNOTATION_TABLE_NAME, "*", "")
    return get_field_from_table("test_employee", "*", "")
