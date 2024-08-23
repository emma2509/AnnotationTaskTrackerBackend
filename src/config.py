import os

DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = "annotationtaskdb"

EMPLOYEE_TABLE_NAME = "employee"
EMPLOYEE_TABLE_ATTRIBUTES = ["username", "firstname", "lastname", "team", "admin", "password"]

ANNOTATION_TABLE_NAME = "annotation"
ANNOTATION_TABLE_ATTRIBUTES = ["username", "annotationstatus", "originaldata", "annotateddata", "tags"]
