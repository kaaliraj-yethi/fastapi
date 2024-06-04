from fastapi import FastAPI , HTTPException
from exceptions import NotFoundException
app = FastAPI()

items = {"foo": "this is foo","voo":"this is voo"}

@app.get("/items/{item_id}")
async def get_item(item_id : str):
    if item_id not in items:
        raise HTTPException (status_code = 404,detail = "Item not found")
    return items[item_id]


@app.get("/items/{item_id}")
async def get_item(item_id : str):
    if item_id not in items:
        raise NotFoundException(detail = "Item not found")
    return items[item_id] 