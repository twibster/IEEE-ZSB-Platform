from backend.routes import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
