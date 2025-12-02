from fastapi import APIRouter

router = APIRouter()

@router.get("/scrape")
def scrape_example():
    return {"status": "Spider would run here"}
