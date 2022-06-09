# This is where we define our API, we create a function per relevant endpoint.

import os

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# We create an instance of FastAPI
app = FastAPI()

# Dependency
def get_db():
    """
    This function ensures that we close the DB session after we finish our work.
    See: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "DIGIT!"}

@app.get("/player/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    """
    :param player_id: The player identifier which operates as the DB PK
    :param db: A database connection to perform the relevants query
    :returns: JSON blob with all relevant data
        {
          "name": "test",
          "id": 36,
          "gold": 456
        }    
    """
    db_player = crud.get_player(db, player_id=player_id)
    # Handling player not found exception nicely
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@app.post("/player/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    """
    :param player_id: A dictionary with relevant player data
    {
        "name": "test",
        "gold": 456
    }
    :param db: A database connection to perform the relevants query
    :returns: JSON blob with all relevant data
        {
          "name": "test",
          "id": 36,
          "gold": 456
        }    
    """
    db_player = crud.get_player_info_by_name(db, player_name=player.name)
    # Handling player already registered exception nicely
    if db_player:
        raise HTTPException(status_code=404, detail="Player already registered")
    return crud.create_player(db=db, player=player)