from dotenv import load_dotenv
from fastapi.responses import JSONResponse
load_dotenv()   


from core.middleware.auth import AuthMiddleware 

from fastapi import FastAPI, HTTPException, Request

from modules.post.routes import router as post_router
from modules.auth.controller import router as auth_router
from modules.tags.routes import router as tags_router

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
app.include_router(tags_router)  # Thêm dòng này để bao gồm router từ modules/tags/routes.py
app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"staus": "ok", "message": "Service is running"}

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Hàm này sẽ chặn tất cả HTTPException.
    Thay vì trả về {"detail": ...}, nó sẽ trả về trực tiếp nội dung trong exc.detail
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail  # Trả về thẳng object, không bọc trong "detail" nữa
    )
# 6. Entry point để chạy ứng dụng (Không reload)
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV") != "development"  # Đã tắt reload theo yêu cầu của bạn
    )


    