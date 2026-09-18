# models.py

from sqlalchemy import Column, Integer, Boolean, Text
from database import Base



#Todo라는 새 클래스를 만드는데 Base라는 클래스가 원래 가지고 있던 모든 기능/속성을 그대로 물려받은채로 시작한다는뜻
#database.py에서 
# from sqlalchemy.ext.declarative import declarative_base 이 코드랑
# Base = declarative_base() 이 코드가 있는데 
# declarative_base()가 만들어주는 Base는 SQLAlchemy 라이브러리 안에 특수 장치가 심어져 있다.
class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(Text)
    completed = Column(Boolean, default=False)
