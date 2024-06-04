#Events
# 1 . To load data into db every 3 seconds.
# 2. To clear data from db every 5 seconds


from fastapi_utilities import repeat_every,repeat_at

@repeat_every(seconds = 3)
async def load_data():
    print("Started loading data")
    await asyncio.sleep(1)
    print("Data is loaded")

@repeat_every(seconds =5)
async def clear_data():
    print("Clearing data")
    await asyncio.sleep(1)
    print("Data cleared")


@repeat_at(cron = "* * * * *")
def test_print():
    print("test2")

    
