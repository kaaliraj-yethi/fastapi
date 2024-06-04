from fastapi import FastAPI
from pydantic import BaseModel

class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description : str or None = None
    price: float
    tax: float
    tags: set[str] = set()
    image: list[Image] or None=None


app = FastAPI()
@app.post("/item")
def create_item(item: Item):
    return item