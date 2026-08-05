from fastapi import FastAPI
from app.exceptions.exception_handlers import register_exception_handlers
from app.router.authentication_router import authentication_router

app = FastAPI(
    title="FastAPI Authentication",
    version="1.0.0" 
)

register_exception_handlers(app)

@app.get('/health')
def health_check():
    return {"status": "ok"}

app.include_router(authentication_router)
