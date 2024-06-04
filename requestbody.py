from fastapi import FastAPI
from pydantic import BaseModel

class Item (BaseModel):
    name : str
    description: str or None = None
    price : float
    tax: float or None = None

app = FastAPI()

@app.post("/items")
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price +item.tax
        item_dict.update ({"price_with_tax": price_with_tax})
    return item_dict
