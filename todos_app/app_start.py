import uvicorn

# cli 실행 : uv run uvicorn main:app [--port=8000] --reload

if __name__ == "__main__":
  uvicorn.run('main:app',
              host='127.0.0.1', port=8000, reload=True,
              reload_excludes=["*.sqlite3", "*.sqlite3-journal"])