# analytics-microservice

## Setup

### Install prerequisites

```shell
pip install -r requirements.txt
```

### Set environment variables

Create a .env file in the root directory and add the following variables:

```shell
DB_CONNECTION_STRING=mysql+pymysql://username:password@hostname:port/database_name
```

### Run the app

```shell
uvicorn src.main:app --reload
```

By default, it runs on http://127.0.0.1:8000 and you will see the response:

```json
{
  "message": "The analytics service is running."
}
```

### Run tests

#### All tests

```shell
pytest
```

#### A specific test

```shell
pytest -k <test_file_or_function>
```

For example, `pytest -k test_main`

