import json

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Factory(Base):
    __tablename__ = "factories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    date = Column(DateTime)
    factory_id = Column(Integer, ForeignKey("factories.id"))

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Upload factories saved in local filesystem to db
factories = json.load(open("resources/factory.json", "r", encoding="utf-8"))["factories"]
with Session(engine) as session:
  for factory in factories:
      # Check if factory already exists
      factoryExists = session.query(Factory).filter(Factory.name == factory["name"]).first()
      if not factoryExists:
          # Factory doesn't exist, add it
          newFactory = Factory(name=factory["name"])
          session.add(newFactory)
          print(f"Added factory: {factory['name']}")
      else:
          # Factory already exists, skip
          print(f"Factory {factory['name']} already exists, skipping")
  session.commit()