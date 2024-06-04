from fastapi import FastAPI,Query,Path
from typing import Annotated,List,Optional

app = FastAPI()

@app.get("/items/{item_id}")
def get_items(
    item_id: Annotated[int,Path(gt=10,le=100)],
    q:Annotated[List[str] or None,Query(min_length = 3,max_length = 10)] = None):

    res =  {"item_id": item_id , "items": [{"item" : "ball"}]}
    if q:
        res.update ({"item" : q})
    return res





