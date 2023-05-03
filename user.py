from pydantic import BaseModel
import uuid
from main import *
from session import user_exists
from sqlalchemy.orm import declarative_base

Base = declarative_base()
from fastapi.testclient import TestClient

class InsertUserItem(BaseModel):
    userID: str


app = FastAPI(
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redocs",
    title="Core API",
    description="Analytical Microservice",
    version="1.0",
    openapi_url="/api/v2/openapi.json",
)


db_connection = create_db_connection()
Session = sessionmaker(bind=db_connection)
db_session = Session()


return_response_400 = {
    "missing_userID_field":"Missing field: userID",
    "userID_is_not_UUID": "Provided userID is not UUID",
    "user_exists_already": "User with the provided userID already exists"
}


return_response_200 = {
    "added_user":{"status code":200, "message":"Added user successfully"}
}

user_error_response = {
    200: {"description": "Added user successfully",
          "content": {"application/json": {"example": {"status code": 200, "message":"Added user successfully"}}}},
    411: {"status_code":411,"description": "missing userID"},
    412: {"status_code":412,"description": "userID is not an UUID"},
    413: {"status_code":413,"description": "User with the provided userID already exists"}
}

"""
Why use it:
    To insert a User with userID into the User database
"""
@app.post("/api/analysis/add-user/", responses=user_error_response)
async def record_user(item:InsertUserItem):
    try:
        if item.userID is None or item.userID == "":
            raise HTTPException(411, detail=user_error_response[411])
        if not is_valid_uuid(item.userID):
            raise HTTPException(412, detail=user_error_response[412])
        else:
            if user_exists(item.userID):
                print("user exists already")
                raise HTTPException(413, detail=user_error_response[413])
            else:
                new_user = UserTable(userID=item.userID)
                db_session.add(new_user)
                db_session.commit()
                return JSONResponse(status_code=200, content=return_response_200["added_user"])
    except Exception as e:
        db_session.rollback()
        raise e

def is_valid_uuid(uuid_string):
    try:
        uuid_obj = uuid.UUID(uuid_string)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_string


def delete_user_from_database(user_uuid):
    try:
        user = db_session.query(UserTable).filter_by(userID=user_uuid).first()
        db_session.delete(user)
        db_session.commit()
        db_session.close()
    except Exception as e:
        print(e)
        traceback.print_exc()
        db_session.rollback()


