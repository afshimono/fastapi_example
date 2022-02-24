# Timezone REST API

### Description

A simple REST API to store timezone differences in hours in Postgres, secured by password and JWT.

### Running the code

This project has a docker-file that can be used to run it with the Postgres dependency.

Only requirement is to copy the file `sample.env` and replace the values with your own, and save it as `.env` in the root folder.

If you don't want to customize anything, the default value for `DATABASE_URL` must be `postgrescompose:5432`.

When docker-compose runs, it will share its values with the application.
To create the 2 tables in the Database and an initial admin, run the script located in `scripts/create_tables.py`.
There is a saved postman collection located in `tests/postman_collection`.

Application is available in `localhost:8000`.
Swagger docs can be found in `localhost:8000/docs`


### Resources

* [Toptal FastAPI Tutorial](https://www.toptal.com/python/build-high-performing-apps-with-the-python-fastapi-framework)
* [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
* [SQL Alchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
* [Timezone on Wikipedia](https://en.wikipedia.org/wiki/Time_zone)
* [List of TZ Database Timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
