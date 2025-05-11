import pytest
import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from main import app, convertIncidentToResponse
from db import get_db, Factory, Incident, Base, ThreatType, WorkType
from model import IncidentBase, IncidentResponse, FactoryResponse

# Create test database
@pytest.fixture(scope='session')
def db_engine():
  SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
  engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
  try:
    yield engine
  finally:
    engine.dispose()
    if os.path.exists("test.db"):
      os.remove("test.db")

@pytest.fixture(scope='session')
def db_session_factory(db_engine):
  return sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

@pytest.fixture(scope="session")
def setupTables(db_engine):
  # Create tables once for the entire test session
  Base.metadata.create_all(bind=db_engine)
  yield
  # Drop tables after all tests are done
  Base.metadata.drop_all(bind=db_engine)

@pytest.fixture(scope="function")
def testDb(setupTables, db_session_factory):
  # Create a new session for each test
  with db_session_factory() as session:
    # Override the dependency
    app.dependency_overrides[get_db] = lambda: session
    yield session

    # Clean up after each test by truncating all tables
    # This is faster than dropping and recreating tables
    for table in reversed(Base.metadata.sorted_tables):
      session.execute(table.delete())
    session.commit()

    # Clear the dependency override
    app.dependency_overrides.clear()

# Create test client
client = TestClient(app)

# Test data fixtures
@pytest.fixture()
def createFactory(testDb) -> Factory:
  factory = Factory(name="Test Factory")
  testDb.add(factory)
  testDb.commit()
  testDb.refresh(factory)

  return factory

@pytest.fixture()
def createThreatType(testDb) -> ThreatType:
  threatType = ThreatType(name="Test Threat Type")
  testDb.add(threatType)
  testDb.commit()
  testDb.refresh(threatType)
  return threatType

@pytest.fixture()
def createWorkType(testDb) -> WorkType:
  workType = WorkType(name="Test Work Type")
  testDb.add(workType)
  testDb.commit()
  testDb.refresh(workType)
  return workType

@pytest.fixture()
def createIncident(testDb, createFactory, createThreatType, createWorkType) -> Incident:
  incident = Incident(
    threatType_id=createThreatType.id,
    threatLevel=1,
    workType_id=createWorkType.id,
    description="Test Description",
    date=datetime.now(),
    factory_id=createFactory.id
  )
  testDb.add(incident)
  testDb.commit()
  testDb.refresh(incident)

  return incident

def testFactoryModel(testDb, createFactory):
  # Test factory creation
  assert createFactory.id is not None
  assert createFactory.name == "Test Factory"

  # Test factory retrieval
  retrievedFactory = testDb.query(Factory).filter(Factory.id == createFactory.id).first()
  assert retrievedFactory is not None
  assert retrievedFactory.name == createFactory.name

def testIncidentBaseToModel():
  dateUsed = datetime.now()
  incidentBase = IncidentBase(
    threatType_id=1,
    threatLevel=1,
    workType_id=1,
    description="Test Description",
    date=dateUsed,
    factory_id=0
  )
  incident = Incident(**incidentBase.model_dump())
  assert incident.threatType_id == 1
  assert incident.threatLevel == 1
  assert incident.workType_id == 1
  assert incident.description == "Test Description"
  assert incident.factory_id == 0
  assert incident.date == dateUsed

def testIncidentModel(testDb, createIncident, createFactory):
  # Test incident creation
  assert createIncident.id is not None
  assert createIncident.threatType_id == 1
  assert createIncident.threatLevel == 1
  assert createIncident.workType_id == 1
  assert createIncident.description == "Test Description"
  assert createIncident.factory_id == createFactory.id

  # Test incident retrieval
  retrievedIncident = testDb.query(Incident).filter(Incident.id == createIncident.id).first()
  assert retrievedIncident is not None
  assert retrievedIncident.threatType_id == createIncident.threatType_id
  assert retrievedIncident.threatLevel == createIncident.threatLevel
  assert retrievedIncident.workType_id == createIncident.workType_id
  assert retrievedIncident.description == createIncident.description
  assert retrievedIncident.factory_id == createFactory.id

# Pydantic model tests
def testFactoryResponseModel(createFactory):
  factoryResponse = FactoryResponse.model_validate(createFactory)
  assert factoryResponse.id == createFactory.id
  assert factoryResponse.name == createFactory.name

def testIncidentResponseModel(testDb, createFactory, createIncident, createThreatType, createWorkType):
  incidentResponse = convertIncidentToResponse(createIncident, testDb)
  assert incidentResponse.id == createIncident.id
  assert incidentResponse.threatType.id == createIncident.threatType_id
  assert incidentResponse.threatType.name == createThreatType.name
  assert incidentResponse.threatLevel == createIncident.threatLevel
  assert incidentResponse.workType.id == createIncident.workType_id
  assert incidentResponse.workType.name == createWorkType.name
  assert incidentResponse.description == createIncident.description
  assert incidentResponse.date == createIncident.date
  assert incidentResponse.factory.id == createIncident.factory_id
  assert isinstance(incidentResponse.check_responses, dict)

# API endpoint tests
def testGetFactories(testDb, createFactory):
  response = client.get("/factories")
  assert response.status_code == 200
  data = response.json()
  assert "factories" in data
  assert len(data["factories"]) >= 1
  assert any(factory["id"] == createFactory.id for factory in data["factories"])

def testGetFactory(testDb, createFactory):
  response = client.get(f"/factories/{createFactory.id}")
  assert response.status_code == 200
  data = response.json()
  assert data["id"] == createFactory.id
  assert data["name"] == createFactory.name

def testGetFactoryNotFound(testDb):
  response = client.get("/factories/9999")
  assert response.status_code == 404

def testGetIncidents(testDb, createIncident):
  response = client.get("/incidents")
  assert response.status_code == 200
  data = response.json()
  assert "incidents" in data
  assert len(data["incidents"]) >= 1
  assert any(incident["id"] == createIncident.id for incident in data["incidents"])

def testGetIncident(testDb, createIncident):
  response = client.get(f"/incidents/{createIncident.id}")
  assert response.status_code == 200
  data = response.json()
  assert data["id"] == createIncident.id
  assert data["description"] == createIncident.description
  assert data["factory"]["id"] == createIncident.factory_id
  assert "threatType" in data
  assert "workType" in data

def testGetIncidentNotFound(testDb):
  response = client.get("/incidents/9999")
  assert response.status_code == 404

def testGetIncidentsByFactory(testDb, createIncident, createFactory):
  response = client.get(f"/incidents/factory/{createFactory.id}")
  assert response.status_code == 200
  data = response.json()
  assert "incidents" in data
  assert len(data["incidents"]) >= 1
  assert all(incident["factory"]["id"] == createFactory.id for incident in data["incidents"])

def testGetIncidentsByFactoryNotFound(testDb):
  response = client.get("/incidents/factory/9999")
  assert response.status_code == 404

def testAddIncident(testDb, createFactory, createThreatType, createWorkType):
  incidentData = {
    "threatType_id": createThreatType.id,
    "threatLevel": 1,
    "workType_id": createWorkType.id,
    "description": "New Test Description",
    "date": datetime.now().isoformat(),
    "factory_id": createFactory.id
  }
  response = client.post("/incidents", json=incidentData)
  assert response.status_code == 200
  data = response.json()
  assert data["description"] == incidentData["description"]
  assert data["factory"]["id"] == incidentData["factory_id"]
  assert data["threatType"]["id"] == incidentData["threatType_id"]
  assert data["workType"]["id"] == incidentData["workType_id"]

def testAddIncidentInvalidFactory(testDb, createThreatType, createWorkType):
  incidentData = {
    "threatType_id": createThreatType.id,
    "threatLevel": 1,
    "workType_id": createWorkType.id,
    "description": "New Test Description",
    "date": datetime.now().isoformat(),
    "factory_id": 9999
  }
  response = client.post("/incidents", json=incidentData)
  assert response.status_code == 404
