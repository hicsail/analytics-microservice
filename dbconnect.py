from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from mysql.connector import errorcode
import uvicorn

app = FastAPI()

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            user='root',
            password='cMgpBzyj3m2KX9OD35s2',
            host='containers-us-west-145.railway.app',
            port='5515',
            database='dev'
        )
        return connection
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise HTTPException(status_code=500, detail='Access denied: Invalid credentials.')
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            raise HTTPException(status_code=500, detail='Database does not exist.')
        else:
            raise HTTPException(status_code=500, detail='Failed to connect to MySQL database.')

test_connection = create_db_connection()
print(test_connection)


@app.get('/users/month_active/{month}')
def get_active_users(month: int):
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
       
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail='Failed to fetch active users from database.')
    finally:
        cursor.close()
        connection.close()





if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


