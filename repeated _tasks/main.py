from fastapi import FastAPI
from contextlib import asynccontextmanager

from events import load_data,clear_data,test_print

@asynccontextmanager
async def lifespan(app: FastAPI):
    await load_data()
    test_print()
    await clear_data()
    yield

app = FastAPI(lifespan = lifespan)


