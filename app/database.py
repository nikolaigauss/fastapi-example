# This is where we define our DB, most precisely the connection strings.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For simplicity postgres user is being utilized, suggested approach is using environment variables in the container.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@host.docker.internal/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Useful param to log all DB requests, would be nice handling with a debug flag.
    echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
