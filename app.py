from fastapi import FastAPI
from enums import Vehicle

app = FastAPI()


@app.get("/")
def hey():
    return "hey"


@app.get("/num")
def num():
    return{"result" : 2}    


#path parameters
# https://www.abc.com/user/alex  
# 
# 
@app.get("/vehicle/{vehicle_num}")
def get_vehicle_num(vehicle_num : int):
    return {"vehicle_name": vehicle_num}

@app.get("/vehicle/{vehicle_name}")
def get_vehicle_name(vehicle_name : str):
    return {"vehicle_name": vehicle_name}


@app.get("/vehicle/{my_vehicle}")
def get_my_vehicle():
    return {"vehicle": "myvehicle"}


@app.get("/vehicle2/{vehicle}")
def get_vehicle2(vehicle:Vehicle):
    if (vehicle is Vehicle.truck):
        return{"vehicle":"truck"}

    elif (vehicle == Vehicle.cycle.value):
        return{"vehicle":"cycle"}   
    else:
        return{"vehicle" : "car"}     


random_list = [
    {"abc": "def"},
    {"def": "ghi"},
    {"ghi" : "jkl"},
    {"jkl" :"mno"}
]

@app.get("/query")
def query(skip:int,limit:int):
    return random_list[skip : skip + limit]


@app.get("/queryuser")
def queryuser(name: str or None = None):
    res = {"user_id" : "1"}
    if name is not None:
        res.update({"name": name})

    return res   



@app.get("/user/{user_id}")
def get_user(user_id : int,name : str or None):
    res = {"user_id" : user_id}
    if name is not None:
        res.update({"name": name})
    return res   