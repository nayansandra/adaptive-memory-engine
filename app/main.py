from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def root():
    return {
        "message": "Hello Nayan!",
        "project": "Adaptive Memory Engine",
        "status": "Learning FastAPI 🚀"
        }