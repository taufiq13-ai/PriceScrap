from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
import json 

class ProductCreate(BaseModel):
    url : str
    target_price : float
    description: str | None = None


router = APIRouter()

def process_scrapping(url:str):
    print(f"Scraping {url} in the background...")
    response : str
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://shopee.com.my/"
        }

        response = httpx.get(url, headers=headers, follow_redirects=True, timeout=30.0)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        #trynna debug lol
        page_title_tag = soup.find("title")
        actual_title = page_title_tag.get_text() if page_title_tag else "No Title Found"
        print(f"DEBUG: The page title we downloaded is: '{actual_title}'")

        script_tag = soup.find("script", type="application/ld+json")

        if script_tag:
            data = json.loads(script_tag.string)
            print("Product Data from JSON-LD:")
            print(json.dumps(data, indent=4))

            product_data = None
            if isinstance(data,dict) and data.get("@type") == "Product":
                product_data = data
            elif isinstance(data,list):
                for item in data:
                    if item.get("@type") == "Product":
                        product_data = item
                        break
            if product_data:
                page_title = product_data.get("name")

                offers = product_data.get("offers", {})
                price_text = offers.get("price")
                currency = offers.get("priceCurrency")

                print(f"successfully scaped {url}, page title: {page_title}")
                print(f"--------------------------------")
                print(f"Scraped Data:")
                print(f"Title: {page_title}")
                print(f"price: {currency} {price_text}")
                print(f"--------------------------------")

                return
        
        print("JSON data no found la, falling back to css ....")
    except Exception as e:
        print   (f"Error scraping {url}: {e}")

@router.get("/scrape")
def scrape_example():
    return {"status": "Spider would run here"}

@router.post("/products")
def create_product(product: ProductCreate, background_tasks: BackgroundTasks):
    print(product.url)
    background_tasks.add_task(process_scrapping, product.url)
    return {"status":"product fetched", 
    "url": product.url, 
    "price":product.target_price
    }
