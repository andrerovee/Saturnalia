from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from .models.items_models import Items
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .db import BaseDb, engine, get_db

BaseDb.metadata.create_all(bind=engine)

class Item(BaseModel):
    name: str
    price: float
    color: str | None = None

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    color: str | None = None

app = FastAPI()

origins = [
    "http://localhost:5173" #frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"], #Permette tutti gli HTTP methods
    allow_headers=["*"], #Permette gli headers
)

@app.get("/items")
async def read_items(db : Session = Depends(get_db)):
    items = db.query(Items).all()
    return items

@app.get("/items/{item_id}")
async def read_item(item_id: int, db : Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item

@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item : Item, db : Session = Depends(get_db)):
    item = Items(**item.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    itemino = db.query(Items).filter(Items.id == item_id).first()

    if not itemino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(itemino, key, value)

    db.commit()
    db.refresh(itemino)

    return itemino

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    db.delete(item)
    db.commit()