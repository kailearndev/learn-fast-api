from dotenv import load_dotenv 
load_dotenv()   
from fastapi import FastAPI
from modules.post.controller import router

app = FastAPI(title="FastAPI with Supabase Example")
app.include_router(router, prefix="/posts", tags=["posts"])