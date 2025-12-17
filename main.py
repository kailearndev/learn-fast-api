from fastapi import FastAPI
from modules.calculator.controller import router

app = FastAPI()
app.include_router(router, prefix="/calculator")
