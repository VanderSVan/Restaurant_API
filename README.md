```commandline
alembic init migrations
```

```commandline
alembic revision --autogenerate -m "first_migration"
```

```commandline
alembic upgrade head
```

```commandline
py -m src.db -h
```

```commandline
uvicorn src.api.app:app --reload
```

![Flask](https://img.shields.io/badge/SQLAlchemy-red?style=for-the-badge)

