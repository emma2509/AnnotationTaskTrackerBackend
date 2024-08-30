## AnnotationTaskTrackerBackend

This project uses the [Flask](https://flask.palletsprojects.com/en/3.0.x/) framework to create different API routes.

### Install dependencies
Run `pip install -r requirements.txt`

### Run locally
1. To connect to database you will need to go to Render and get the database external URL. This will be in this format `postgresql://USER:PASSWORD@EXTERNAL_HOST:PORT/DATABASE`
2. Extract the `USER` name and `PASSWORD` and set this as your env variables (`export DB_USER="" && export DB_PASSWORD="" && export DB_HOST=""`)
3. Run `python src/app.py` or `flask --app src/app run` or `gunicorn src.app:app`
4. Open the URL returned.

### Run unit tests
Render build will fail if unit tests are failing.

To run unit tests locally run `pytest test`

### Calling API routes
You can call the API routes by using `curl` commands.

Below is an example command you can use to call an API route, replace the values in the `[]` with the API call values.

`curl -X [POST/GET] -H 'Content-Type: application/json' -d '[JSON data]' [API-URL]`
