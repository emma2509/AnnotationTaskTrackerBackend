### AnnotationTaskTrackerBackend

### Install dependencies
Run `pip install -r requirements.txt`

#### Run locally
1. To connect to database you will need to go to Render and get the database external URL. This will be in this format `postgresql://USER:PASSWORD@EXTERNAL_HOST:PORT/DATABASE`
2. Extract the `USER` name and `PASSWORD` and set this as your env variables (`export DB_USER="" && export DB_PASSWORD="" && export DB_HOST=""`)
3. Run `python src/app.py` or `flask --app src/app run` or `gunicorn app:app`
4. Open the URL returned.
