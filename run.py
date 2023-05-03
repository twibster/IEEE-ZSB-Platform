import time

start = time.time()

from backend.routes import app

if __name__ == "__main__":
    import uvicorn
    print(f"Startup took {time.time()-start} seconds")
    uvicorn.run("run:app", reload=True)
