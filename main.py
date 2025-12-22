from dotenv import load_dotenv
load_dotenv()   


from core.middleware.auth import AuthMiddleware 

from fastapi import FastAPI

from modules.post.routes import router as post_router
from modules.auth.controller import router as auth_router

from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import HTTPBearer

import uvicorn

import os
security = HTTPBearer()
app = FastAPI(title="FastAPI with Supabase Example")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
   )
app.add_middleware(AuthMiddleware)
app.include_router(post_router)
app.include_router(auth_router)

app.get("/health")
def health_check():
    return {"staus": "ok", "message": "Service is running"}


# 6. Entry point để chạy ứng dụng (Không reload)
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV") == "development"  # Đã tắt reload theo yêu cầu của bạn
    )


    