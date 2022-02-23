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

### Design


### Running the code



### TODO List

- [x] User auth and JWT use
- [ ] Timezone endpoints
- [x] Timezone DB
- [ ] Unittests
- [ ] Documentation
- [ ] Dockerization
- [ ] Init Scripts

### Resources

* [Toptal FastAPI Tutorial](https://www.toptal.com/python/build-high-performing-apps-with-the-python-fastapi-framework)
* [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
* [SQL Alchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
* [Timezone on Wikipedia](https://en.wikipedia.org/wiki/Time_zone)
* [List of TZ Database Timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
