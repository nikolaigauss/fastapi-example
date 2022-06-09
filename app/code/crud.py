# This is where we define the relevant CRUD tasks, in this case we only create and read.

from sqlalchemy.orm import Session

from . import models, schemas


def get_player(db: Session, player_id: int):
    """
    :param db: A database connection to perform the relevants query
    :param player_id: The player identifier which operates as the DB PK
    :returns: Query results returning a single player
    """
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def get_player_info_by_name(db: Session, player_name: str):
    """
    :param db: A database connection to perform the relevants query
    :param player_name: The player name
    :returns: Query results returning a single player
    """
    return db.query(models.Player).filter(models.Player.name == player_name).first()

def create_player(db: Session, player: schemas.PlayerCreate):
    """
    :param db: A database connection to perform the relevants query
    :param player: A Player schema, which is a JSON blob with the name and the amount of gold
    :returns: Query results returning a single player
    """
    db_player = models.Player(name=player.name, gold=player.gold)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player
