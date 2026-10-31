from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://127.0.0.1:5500"]
)


@app.get("/") 
def get_result():
    return{"Course": "CSC 406", "Score": "86"}