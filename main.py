from dotenv import load_dotenv
load_dotenv()   


from core.middleware.auth import AuthMiddleware 

from fastapi import FastAPI

from modules.post.routes import router as post_router


from fastapi.security import HTTPBearer
security = HTTPBearer()
app = FastAPI(title="FastAPI with Supabase Example")
app.add_middleware(AuthMiddleware)

app.include_router(post_router)
