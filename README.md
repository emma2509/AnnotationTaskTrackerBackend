## AnnotationTaskTrackerBackend

This project uses the [Flask](https://flask.palletsprojects.com/en/3.0.x/) framework to create different API routes.

### Initial Set up

#### Set up env

Create virtual env: `python -m venv nameofvenv`

Activate env: `source .nameofvenv/bin/activate`

#### Run builder
Run `pip install pybuilder`

Then run builder: `pyb`

This will install all required dependencies, run linter and unit tests.

### Running locally
1. To connect to database you will need to go to Render and get the database external URL. This will be in this format `postgresql://USER:PASSWORD@EXTERNAL_HOST:PORT/DATABASE`
   1. You can also connect to your database via the CLI with the following command: `psql -h <db-address> -d <db-name> -U <username> -W`
2. Extract the `USER` name and `PASSWORD` and set this as your env variables (`export DB_USER="" && export DB_PASSWORD="" && export DB_HOST=""`)
3. Run `python src/app.py` or `flask --app src/app run` or `gunicorn src.app:app` to run the API locally. The URL for the local API will be returned.

### Running unit tests
Render build will fail if unit tests are failing.

To run unit tests locally run `pytest test/modules`

### Running security tests
1. Set DB env variables.
2. Set env variables for an existing regular user (command: `export TEST_ACCOUNT_USERNAME={account-username} && export TEST_ACCOUNT_PASSWORD={account-password}`)
3. Run tests using the following command: `pytest test/security`

### Calling API routes
You can call the API routes by using `curl` commands.

Below is an example command you can use to call an API route, replace the `[]` variable with the API call values.

`curl -X [POST/GET] -H '{"Content-Type": "application/json","requester-user-name":"[username]","requester-password":"[password]"}' -d '[input]' [API-URL/ROUTE]`

API routes:
* log_in
   * Route type: POST
   * Input format: empty (`{}`)
   * Output: authentication status and authorisation level.
* add_user
   * Route type: POST
   * Input format: `{"user-name": "string", "first-name": "string", "last-name": "string", "team": "string", "admin": boolean, "password": "string"}`
   * Output: api call and action status.
* add_annotation
   * Route type: POST
   * Input format: `{"user-name": "string", "annotation-status": "string: Not started, In progress, Completed", "orginal-data": "string", "annotated-data": "string", "tags": "string list, strings seperated by commas"}`
   * Output: api call and action status.
* update_annotation
   * Route type: POST
   * Input format: `{"annotation-id": "string number", "user-name": "string", "annotation-status": "string: Not started, In progress, Completed", "orginal-data": "string", "annotated-data": "string", "tags": "string list, strings seperated by commas"}`
   * Output: api call and action status.
* delete_annotation
   * Route type: POST
   * Input format: `{"annotation-id": "string number"}`
   * Output: api call and action status.
* get_users
   * Route type: GET
   * Input format: -
   * Output: list of all user details
* get_annotation
   * Route type: GET
   * Input format: -
   * Output: list of all annotation tasks



### Lint code
[Ruff](https://github.com/astral-sh/ruff?tab=readme-ov-file) is used as a linter and formater.

Run linter: `ruff check`

Run formatter: `ruff format`
