from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define a model for the item
class Item(BaseModel):
    id: int
    name: str

# In-memory "database"
items = [
    {"id": 1, "name": "Item One"},
    {"id": 2, "name": "Item Two"}
]

# GET endpoint to retrieve all items
@app.get("/items", response_model=List[Item])
def read_items():
    return items

# POST endpoint to create a new item
@app.post("/items", response_model=Item)
def create_item(item: Item):
    if any(i['id'] == item.id for i in items):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item.dict())
    return item

# PUT endpoint to update an existing item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    for idx, existing_item in enumerate(items):
        if existing_item['id'] == item_id:
            items[idx].update(item.dict())
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE endpoint to delete an item
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    for idx, existing_item in enumerate(items):
        if existing_item['id'] == item_id:
            items.pop(idx)
            return existing_item
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

