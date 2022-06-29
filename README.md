## Manage Books

#### Prepare env file

```
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_password>
POSTGRES_SERVER=<db_server>
POSTGRES_PORT=<db_port>
POSTGRES_DB=<db>
SECRET_KEY=<secret_key>
TEST_POSTGRES_DB=<db_for_tests>
```

#### Build project:

- make build

#### Run project:

- make up

#### Run tests:

- docker-compose run web python -m pytest tests/

#### API endpoints
```angular2html
http://127.0.0.1:8000/books/
http://127.0.0.1:8000/books/:id
http://127.0.0.1:8000/users/
```