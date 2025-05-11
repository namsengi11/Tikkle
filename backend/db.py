import json

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, Session, declarative_base

DATABASE_URL = "sqlite:///../database.db"

# # Check if database exists
# if not os.path.exists("database.db"):
#     raise FileNotFoundError("database.db not found")

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
    threatType_id = Column(Integer, ForeignKey("threat_types.id"))
    threatLevel = Column(Integer)
    workType_id = Column(Integer, ForeignKey("work_types.id"))
    description = Column(String)
    date = Column(DateTime)
    factory_id = Column(Integer, ForeignKey("factories.id"))

class ThreatType(Base):
    __tablename__ = "threat_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

class WorkType(Base):
    __tablename__ = "work_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

class CheckQuestion(Base):
    __tablename__ = "check_questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(String)

class CheckResponse(Base):
    __tablename__ = "check_responses"
    question_id = Column(Integer, ForeignKey("check_questions.id"), primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), primary_key=True, index=True)
    response = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def populateWithLocalData(localFileName: str, tableName: str, model, candidateKey: str):
    data = json.load(open("resources/" + localFileName, "r", encoding="utf-8"))[tableName]
    with Session(engine) as session:
        for item in data:
            # Check if item already exists
            itemExists = session.query(model).filter(getattr(model, candidateKey) == item[candidateKey]).first()
            if not itemExists:
                # Item doesn't exist, add it
                newItem = model(**item)
                session.add(newItem)
                print(f"Added {tableName}: {item[candidateKey]}")
            else:
                # Item already exists, skip
                print(f"{tableName} {item[candidateKey]} already exists, skipping")
        session.commit()

populateWithLocalData("factory.json", "factories", Factory, "name")
populateWithLocalData("threatType.json", "threatTypes", ThreatType, "name")
populateWithLocalData("workType.json", "workTypes", WorkType, "name")
populateWithLocalData("checkQuestion.json", "checkQuestions", CheckQuestion, "question")