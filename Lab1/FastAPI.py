# -------------------------------------------------------- FastAPI ---------------------------------------------------------- #
'''
fast api is a modern web framework for building APIs
'''
from fastapi import FastAPI, HTTPException


# Create an app
app = FastAPI()

# define a path for HTTP Get method
@app.get("/")
def root():
    return {"Hello": "World"}

items = []


# function to post an item
@app.post("items")
def create_item(item: str):
    items.append(item)
    return item


#function to return specifc item
@app.get("items/{item_id}")
def get_item(item_id: int) -> str:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found") # return a response with status code 404

#function to return   
@app.get("/items/")
def list_items(limit: int = 10):
    return items[0:limit]
