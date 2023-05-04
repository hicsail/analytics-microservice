# analytics-microservice

### Brief overview of the project:
This project is to build APIs for BU SAIL's analytical microservice. Due to privacy protection rule (HIPAA), BU SAIL is unable to use existing analytical services, so we are building APIs that are albe to store and retrieve information of users that interact with BU SAIL, and BU SAIL can deploy our APIs to their microservice to have their own analytical microservice. Because our APIs will manage the users data in BU SAIL's private database, so BU SAIL's  analytical microservice which runs our APIs will follow the privacy protection rule. 

### Technical architecture and explanation





### Issues of current project:


### Deployment:
https://github.com/hicsail/analytics-microservice/blob/main/DEPLOYMENT.md

### Detailed instructions on how to run our project:
### Setup
### HIGHLY recommand create a virtual environment first!
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

