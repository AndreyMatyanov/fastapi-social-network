## Инструкция

1. Clone this project.

2. Start a new Virtualenv, activate it and type in console this command:
```
pip install -r requirements.txt
```

3. Set up PostgreSQL dababase and set its URL in `config/local.env` and `alembic.ini`.

4. Run migrations. Just type in console this command:
```
alembic upgrade head
```

5. Run the API by typing in console this command:
```
uvicorn app.main:app --env-file config/local.env
```

## Tests

1. Set up PostgreSQL database and set URL in `tests/pytest.ini`
2. Run tests. Enter in console this command:
```
pytest -c tests/pytest.ini
```

## Technologies

Backend: FastAPI v0.71, SQLAlchemy v1.4.22. 

Database: PostgreSQL.