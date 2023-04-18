
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import pymysql

Base = declarative_base()

class user(Base):
    __tablename__ = 'user'
    userID = Column(VARCHAR, primary_key=true)

def getEngine():
    return create_engine("mysql+pymysql://root:cMgpBzyj3m2KX9OD35s2@containers-us-west-145.railway.app:5515/dev")

def getUser(targetValue):
    engine = getEngine()
    Session = sessionmaker(bind=engine)
    session = Session()
    user_exists = session.query(user).filter_by(userID=targetValue).first() is not None
    return user_exists

print(getUser("59ee9a5e-cd2d-435b-a68c-"))


