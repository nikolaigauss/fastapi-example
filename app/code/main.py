# This is where we define our API, we create a function per relevant endpoint.

import os
from tkinter import dnd
import redis

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# We create an instance of FastAPI
app = FastAPI()

# We initialize redis
redis = redis.Redis(
    host= os.environ.get("REDIS_HOST"),
    port= os.environ.get("REDIS_PORT"))

# Yield dependency
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

## This might seem pointless as we're making a connection to the DB to retrieve user data even if the gold value is cached
## Because the player_id is the PK and we need the name of the player from Postgres, we need to query the DB no matter what
## Application logic should ensure that, should a key is stored in Redis, it has to be retrieved to allieviate pressure on the DB.

    cached_gold = redis.get(player_id)

    if cached_gold:
        # If the player_id is cached, this means that there was a request at least less than 30 seconds ago, hence we're using the cached value
        db_player = crud.get_player(db, player_id=player_id)
        db_player.gold = cached_gold
        print("Cached gold from Redis")
        return db_player

    # Up to this point redis can't find a cached key hence we fall back to the DB.
    db_player = crud.get_player(db, player_id=player_id)
    # Handling player not found exception nicely
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found.")
    redis.set(player_id, db_player.gold, ex=30)
    print("Writting redis Cache")
    return db_player

def validate_input(player: schemas.PlayerCreate):
    """
    This function will validate if the input values are correct based on the specs.
    :player schema: A player object with the input values to validate
    :returns: Boolean value based on validation success or failure
    """
    max_gold = 1000000000

    if len(player.name) > 20:
        return False
    if player.gold > max_gold:
        return False
    return True

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
        raise HTTPException(status_code=404, detail="Player already registered.")

    if validate_input(player):
        return crud.create_player(db=db, player=player)
    else:
        raise HTTPException(status_code=422, detail="Input error in fields, validate your input.")
    