from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, inspect, CheckConstraint, text, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy import event

DATABASE_URL = "sqlite:///../user.db"

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

class User(Base):
  __tablename__ = "users"

  username = Column(String, primary_key=True)
  hashed_password = Column(String)

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