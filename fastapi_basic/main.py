from fastapi import FastAPI

#FastAPI 객체 생성
app = FastAPI()

#http://localhost:8000/ 입력시 나오는 것.
@app.get("/")
async def root():
    data = "db에서 데이터 읽어오기"
    return {"message": data}

#http://localhost:8000/hello  입력시 나오는 것.
@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}

#http://localhost:8000/items/ 입력시 나오는 것.
@app.get("/items/")
async def read_item():
    item_id = 1
    q = "사과"
    return {"item_id": item_id, "q": q}


# http://localhost:8000/items/300?q=치킨  이런식으로 입력시 나오는 것. 지금 이 예시는 item_id는 300, q는 치킨임.
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    # 비즈니스 로직 처리
    print(f"item_id: {item_id}, q: {q}")

    return {"item_id": item_id, "q": q}


# @app.post("/user_info/{user_id}")
# def create_item(user_id: int, q: str = None):
#     # 비즈니스 로직 처리
#     print(f"user_id: {user_id}, q: {q}")

#     return {"user_id": user_id, "q": q}


from pydentic import BaseModel, HttpUrl
from typing import Optional


#DTP : 데이터 전송 객체
class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
   


@app.post("/user_info/")
def create_item(user: UserCreate):
    # 비즈니스 로직 처리
    print(f"user_id: {user_id}, q: {q}")

    return {"user_id": user_id, "q": q}
