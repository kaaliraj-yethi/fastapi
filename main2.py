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
    return item