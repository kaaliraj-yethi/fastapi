from fastapi import FastAPI
from contextlib import asyncontextmanager


#load up the data into as the app starts

async def load_data():
    print("loaded data into db")


#load the ml model
async def my_model(x: float):
    return x*2

#shutdown lifespan event
#clear db
async def clear_db():
    print("cleared db")

ml_models = {}

@asyncontextmanager
async def lifespan(app: FastAPI):
    #startup
    await load_data()
    ml_models("my_model") = my_model

    yield

    #shutdown events
    ml_models.clear()
    await clear_db()

app = FastAPI(lifespan = lifespan)

@app.get("./predict")
async def predict(x: float):
    result =  await ml_models("my_model")(x)
    return {"result": result}



