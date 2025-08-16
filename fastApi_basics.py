from fastapi import FastAPI
from enum import Enum
app = FastAPI()

class AvailableCuisines(str, Enum):
    Indian = "Indian"
    American = "American"
    Italian = "Italian"
food_items = {
    'Indian' : ["Samosa","Dosa"],
    'American' : ["Hot Dog", "Apple Pie"],
    'Italian' : ["Ravioli","Pizza"]
 }

valid_cuisines = food_items.keys()


@app.get("/get_items/{cuisine}")
async def get_items(cuisine: AvailableCuisines):
    return food_items.get(cuisine)

coupon_code = {
    1: '10%',
    2: '20%',
    3: '30%'
}

@app.get("/get_coupon/{code}")
async def get_items(code: int):
    return {'discount_amount': coupon_code.get(code)}
