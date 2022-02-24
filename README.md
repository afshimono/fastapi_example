# Timezone REST API

### Task Description

Write a REST API that shows time in different timezones

API Users must be able to create an account and log in.

All API calls must be authenticated.

When logged in, a user can see, edit and delete timezones he entered.

Implement 2 roles with different permission levels: a regular user would only be able to CRUD on their owned records, and an admin would be able to CRUD all users and all user records.

When a timezone is entered, each entry has a Name, Name of the city in timezone, the difference to GMT time.

The API must be able to return data in the JSON format.

In any case, you should be able to explain how a REST API works and demonstrate that by creating functional tests that use the REST Layer directly. Please be prepared to use REST clients like Postman, cURL, etc. for this purpose.
Write unit tests.

### Running the code

This project has a docker-file that can be used to run it with the Postgres dependency.

Only requirement is to copy the file `sample.env` and replace the values with your own, and save it as `.env` in the root folder.

If you don't want to customize anything, the default value for `DATABASE_URL` must be `postgrescompose:5432`.

When docker-compose runs, it will share its values with the application.
To create the 2 tables in the Database and an initial admin, run the script located in `scripts/create_tables.py`.
There is a saved postman collection located in `tests/postman_collection`.

Application is available in `localhost:8000`.
Swagger docs can be found in `localhost:8000/docs`


### TODO List

- [x] User auth and JWT use
- [x] Timezone endpoints
- [x] Timezone DB
- [x] Unittests
- [x] Documentation
- [x] Dockerization
- [x] Init Scripts

### Resources

* [Toptal FastAPI Tutorial](https://www.toptal.com/python/build-high-performing-apps-with-the-python-fastapi-framework)
* [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
* [SQL Alchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
* [Timezone on Wikipedia](https://en.wikipedia.org/wiki/Time_zone)
* [List of TZ Database Timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
