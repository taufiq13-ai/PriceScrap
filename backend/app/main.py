from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(title="Price Comparison API")
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "FastAPI + Scrapy running!"}
