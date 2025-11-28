from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from .models.terreni_models import Terreni, Particelle
from sqlalchemy.orm import Session, joinedload
from fastapi.middleware.cors import CORSMiddleware
from typing  import List

from .db import BaseDb, engine, get_db

BaseDb.metadata.create_all(bind=engine)

class Particella(BaseModel):
    comune: str
    sezione: str | None = None
    foglio: int
    particella: int
    superficie_m2: float

    class Config:
        from_attributes = True

class Terreno(BaseModel):
    
    codice_nome: str
    comune: str
    area_coltivata_m2: float
    particelle: List[Particella] = []
    

    class Config:
        from_attributes = True


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"], #Permette tutti gli HTTP methods
    allow_headers=["*"], #Permette gli headers
)

@app.get("/terreni")
async def read_terreni(db: Session = Depends(get_db)):
    terreni = db.query(Terreni).options(joinedload(Terreni.particelle)).all()

    return terreni


@app.get("/terreni/{terreno_id}")
async def read_terreno(terreno_id: int, db : Session = Depends(get_db)):
    terreno = db.query(Terreni).filter(Terreni.id == terreno_id).first()
    if not terreno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Terreno non trovato",
        )
    return terreno


@app.post("/terreni", status_code=status.HTTP_201_CREATED)
def create_terreno(terreno: Terreno, db: Session = Depends(get_db)):
    #Creazione TERRENO
    nuovo_terreno = Terreni(
        codice_nome=terreno.codice_nome,
        comune=terreno.comune,
        area_coltivata_m2=terreno.area_coltivata_m2,
    )

    db.add(nuovo_terreno)
    db.commit()
    db.refresh(nuovo_terreno)

    #Creazione PARTICELLE collegate
    for p in terreno.particelle:
        nuova_particella = Particelle(
            terreno_id=nuovo_terreno.id,
            comune=p.comune,
            sezione=p.sezione,
            foglio=p.foglio,
            particella=p.particella,
            superficie_m2=p.superficie_m2
        )
        db.add(nuova_particella)

    db.commit()
    db.refresh(nuovo_terreno)
    return nuovo_terreno

@app.put("/terreni/{terreno_id}")
def update_terreno(terreno_id: int, terreno: Terreno, db: Session = Depends(get_db)):
    db_terreno = db.query(Terreni).filter(Terreni.id == terreno_id).first()
    if not db_terreno:
        raise HTTPException(status_code=404, detail="Terreno non trovato")

    # Aggiorna il terreno
    db_terreno.codice_nome = terreno.codice_nome
    db_terreno.comune = terreno.comune
    db_terreno.area_coltivata_m2 = terreno.area_coltivata_m2
   
    # Gestisci le particelle
    # Se l’ID della particella esiste, aggiorna, altrimenti crea
    existing_ids = {p.id for p in db_terreno.particelle}
    incoming_ids = set()

    for p in terreno.particelle:
        if hasattr(p, "id") and p.id in existing_ids:
            db_part = db.query(Particelle).filter(Particelle.id == p.id).first()
            db_part.comune = p.comune
            db_part.sezione = p.sezione
            db_part.foglio = p.foglio
            db_part.particella = p.particella
            db_part.superficie_m2 = p.superficie_m2
            incoming_ids.add(p.id)
        else:
            new_p = Particelle(
                terreno_id=terreno_id,
                comune=p.comune,
                sezione=p.sezione,
                foglio=p.foglio,
                particella=p.particella,
                superficie_m2=p.superficie_m2
            )
            db.add(new_p)

    # Cancella le particelle che non ci sono più
    for p in db_terreno.particelle:
        if p.id not in incoming_ids:
            db.delete(p)

    db.commit()
    db.refresh(db_terreno)
    return db_terreno

# --- DELETE TERRITORIO ---
@app.delete("/terreni/{terreno_id}", status_code=204)
def delete_terreno(terreno_id: int, db: Session = Depends(get_db)):
    terreno = db.query(Terreni).filter(Terreni.id == terreno_id).first()
    if not terreno:
        raise HTTPException(status_code=404, detail="Terreno non trovato")
    
    # Elimina tutte le particelle collegate
    db.query(Particelle).filter(Particelle.terreno_id == terreno.id).delete()
    
    # Elimina il terreno
    db.delete(terreno)
    db.commit()
    return
