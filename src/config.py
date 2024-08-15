import os

DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = "annotationtaskdb"

EMPLOYEE_TABLE_NAME = "employee"
EMPLOYEE_TABLE_ATTRIBUTES = ["username", "firstname", "secondname", "team", "admin", "password"]
