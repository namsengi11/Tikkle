import json

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, inspect, CheckConstraint, text, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy import event

DATABASE_URL = "sqlite:///../database.db"

engine = create_engine(
  DATABASE_URL,
  connect_args={"check_same_thread": False}
)

# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def setForeignKeyConstraint(dbapi_connection, connection_record):
  cursor = dbapi_connection.cursor()
  cursor.execute("PRAGMA foreign_keys=ON")
  cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Factory(Base):
    __tablename__ = "factory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    workforceSizeRange_id = Column(Integer, ForeignKey("workforce_size_range.id"))

    def typeToString(self):
        return "factory"

class Worker(Base):
    __tablename__ = "worker"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    ageRange_id = Column(Integer, ForeignKey("age_range.id"))
    sex = Column(String)
    workExperienceRange_id = Column(Integer, ForeignKey("work_experience_range.id"))

    __table_args__ = (
        CheckConstraint("sex in ('남', '여')", name="check_sex_values"),
    )

    def typeToString(self):
        return "worker"

class Incident(Base):
    __tablename__ = "incident"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    worker_id = Column(Integer, ForeignKey("worker.id"))
    industryTypeLarge_id = Column(Integer, ForeignKey("industry_type_large.id"))
    industryTypeMedium_id = Column(Integer, ForeignKey("industry_type_medium.id"))
    threatType_id = Column(Integer, ForeignKey("threat_type.id"))
    threatLevel = Column(Integer)
    workType_id = Column(Integer, ForeignKey("work_type.id"))
    description = Column(String)
    date = Column(DateTime)
    factory_id = Column(Integer, ForeignKey("factory.id"))

    def typeToString(self):
        return "incident"

class ThreatType(Base):
    __tablename__ = "threat_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

    def typeToString(self):
        return "threatType"

class WorkType(Base):
    __tablename__ = "work_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

    def typeToString(self):
        return "workType"

class CheckQuestion(Base):
    __tablename__ = "check_question"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(String)

    def typeToString(self):
        return "checkQuestion"

class CheckResponse(Base):
    __tablename__ = "check_response"
    question_id = Column(Integer, ForeignKey("check_question.id"), primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incident.id"), primary_key=True, index=True)
    response = Column(Boolean)

    def typeToString(self):
        return "checkResponse"

class IndustryTypeLarge(Base):
    __tablename__ = "industry_type_large"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

    def typeToString(self):
        return "industryTypeLarge"

class IndustryTypeMedium(Base):
    __tablename__ = "industry_type_medium"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

    def typeToString(self):
        return "industryTypeMedium"

class WorkforceSizeRange(Base):
    __tablename__ = "workforce_size_range"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    range = Column(String)

    def typeToString(self):
        return "workforceSizeRange"

class AgeRange(Base):
    __tablename__ = "age_range"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    range = Column(String)

    def typeToString(self):
        return "ageRange"

class WorkExperienceRange(Base):
    __tablename__ = "work_experience_range"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    range = Column(String)

    def typeToString(self):
        return "workExperienceRange"

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ensureSchemaMatches():
  """
  Ensures that the database schema matches the SQLAlchemy models.
  Adds missing columns with NULL default values for existing entries.
  """
  inspector = inspect(engine)

  # Get all model classes defined in this module
  modelClasses = [
    cls for cls in Base.__subclasses__()
    if cls.__module__ == __name__
  ]

  for modelClass in modelClasses:
    tableName = modelClass.__tablename__
    print(f"Checking schema for table: {tableName}")

    # Get existing columns in the database
    existingColumns = {col['name'] for col in inspector.get_columns(tableName)}

    # Get columns defined in the model
    modelColumns = {column.key: column for column in modelClass.__table__.columns}

    # Find missing columns
    missingColumns = set(modelColumns.keys()) - existingColumns

    if missingColumns:
      print(f"Missing columns in {tableName}: {missingColumns}")

      # Add missing columns with NULL default
      with engine.connect() as connection:
        for colName in missingColumns:
          column = modelColumns[colName]
          colType = column.type.compile(engine.dialect)

          # Create ALTER TABLE statement
          alterStatement = f"ALTER TABLE {tableName} ADD COLUMN {colName} {colType}"

          if hasattr(column, 'foreign_keys') and column.foreign_keys:
            fk = list(column.foreign_keys)[0]
            alterStatement += f" REFERENCES {fk.column.table.name}({fk.column.name})"

          try:
            # Use text() to convert string to executable SQL expression
            connection.execute(text(alterStatement))
            connection.commit()
            print(f"Added column {colName} to {tableName}")
          except Exception as e:
            print(f"Error adding column {colName} to {tableName}: {e}")
    else:
      print(f"Table {tableName} schema is up to date")

# Call the function to ensure schema matches
ensureSchemaMatches()

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

# Repopulate constants with local data
# Warning: This will delete all existing 'constant' data in the database
populateWithLocalData("workforceSizeRange.json", "workforce_size_range", WorkforceSizeRange, "range")
populateWithLocalData("factory.json", "factory", Factory, "name")
populateWithLocalData("threatType.json", "threat_type", ThreatType, "name")
populateWithLocalData("workType.json", "work_type", WorkType, "name")
populateWithLocalData("checkQuestion.json", "check_question", CheckQuestion, "question")
populateWithLocalData("ageRange.json", "age_range", AgeRange, "range")
populateWithLocalData("workExperienceRange.json", "work_experience_range", WorkExperienceRange, "range")
populateWithLocalData("industryTypeLarge.json", "industry_type_large", IndustryTypeLarge, "name")
populateWithLocalData("industryTypeMedium.json", "industry_type_medium", IndustryTypeMedium, "name")


