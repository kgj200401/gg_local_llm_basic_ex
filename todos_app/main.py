from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import os





#models.py에서 정의한 Todo클래스를 가져와서 DB에 연결하고, FastAPI를 이용하여 웹 애플리케이션을 구축하는 코드
import models
from database import engine, SessionLocal, Base


# FastAPI() 객체 생성
app = FastAPI()

# models에 정의한 모든 클래스, 연결한 DB엔진에 테이블로 생성
Base.metadata.create_all(bind=engine)


# DB 세션을 생성하고, 요청 처리가 끝나면 세션을 닫아주는 의존성 함수
# yield : FastAPI가 함수 실행을 일시 중지하고 DB 세션을 호출자에게 반환하도록 지시
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # 마지막에 무조건 닫음
        db.close()

abs_path = os.path.dirname(os.path.realpath(__file__))
# print(abs_path)
# html 템플릿 폴더를 지정하여 jinja템플릿 객체 생성
# templates = Jinja2Templates(directory="templates")
#templates 폴더 식별 객체 변수
templates = Jinja2Templates(directory=f"{abs_path}/templates")

# static 폴더(정적파일 폴더)를 app에 연결
# app.mount("/static", StaticFiles(directory=f"static"), name="static")
#static 폴더를 fastapi에서 인식할 수 있도록 마운트한다
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name="static")


#http://localhost:8000/
@app.get("/")
async def home(request: Request, db_ss: Session = Depends(get_db)):
    # db 객체 생성, 세션연결하기 <- 의존성 주입으로 처리
    # 테이블 조회
    todos = db_ss.query(models.Todo).order_by(models.Todo.id.desc()).all()

    print(type(todos))
    # db 조회한 결과를 출력함
    # for todo in todos:
    #     print(todo.id, todo.task, todo.completed)

    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context={ "todos": todos}
    )

@app.post("/add")
async def add(request: Request, 
              task: str = Form(...),
              db_ss: Session = Depends(get_db)):
    # 클라이언트에서 textarea에서 입력 데이터 넘어온것 확인
    print(task)
    # 클라이언트에서 넘어온 task를 Todo 객체로 생성
    todo = models.Todo(task=task)
    # 의존성 주입에서 처리함 Depends(get_db) : 엔진객체생성, 세션연결
    # db 테이블에 task 저장하기
    print(todo)
    db_ss.add(todo)
    # db에 실제 저장, commit
    db_ss.commit()
    # home 엔드포인트함수로 제어권을 넘김
    return RedirectResponse(url=app.url_path_for("home"),
                            status_code=status.HTTP_303_SEE_OTHER)

@app.get("/edit/{todo_id}")
async def edit(request: Request, todo_id: int, db_ss: Session = Depends(get_db)):
    todo = db_ss.get(models.Todo, todo_id)

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return templates.TemplateResponse(
        request=request,
        name = "edit.html",
        context = {"todo": todo}
    )

# todo 업데이터 처리
@app.post("/edit/{todo_id}")
async def update(request: Request, todo_id: int, task: str = Form(...), completed: bool = Form(False), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.task = task
    todo.completed = completed
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

# todo 삭제 처리
@app.post("/delete/{todo_id}")
async def delete(todo_id: int, db_ss: Session = Depends(get_db)):
    todo = db_ss.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_ss.delete(todo)
    db_ss.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
