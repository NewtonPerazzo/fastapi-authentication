from fastapi import FastAPI
from app.exceptions.exception_handlers import register_exception_handlers
from app.users.users_router import users_router
from app.authentication.authentication_router import authentication_router

app = FastAPI(
    title="FastAPI Authentication",
    version="1.0.0" 
)

register_exception_handlers(app)

@app.get('/health')
def health_check():
    return {"status": "ok"}

app.include_router(users_router)
app.include_router(authentication_router)
