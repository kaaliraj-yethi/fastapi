from fastapi import APIRouter

router = APIRouter(prefix= "/items",tags= ["items"])

@router.get("/{items_id}")
async def get_user(item_id: int):
    res = {"item_id": item_id}
    return res
