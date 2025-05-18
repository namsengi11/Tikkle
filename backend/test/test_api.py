import pytest
import os
import sys

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.main import app, convertIncidentToResponse, convertDBModelintoResponseModel
from backend.db import get_db, Factory, Incident, Base, ThreatType, WorkType, Worker, WorkforceSizeRange, AgeRange, WorkExperienceRange, IndustryTypeLarge, IndustryTypeMedium
from backend.model import IncidentBase, IncidentResponse, FactoryResponse

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
  try:
    Base.metadata.create_all(bind=db_engine)
    yield
  finally:
    # Drop tables after all tests are done
    Base.metadata.drop_all(bind=db_engine)

@pytest.fixture(scope="function")
def testDb(setupTables, db_session_factory):
  # Create a new session for each test
  with db_session_factory() as session:
    # Override the dependency
    app.dependency_overrides[get_db] = lambda: session
    try:
      yield session
    finally:
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
def createWorkforceSizeRange(testDb) -> WorkforceSizeRange:
  workforceSizeRange = WorkforceSizeRange(range="Test Workforce Size Range")
  testDb.add(workforceSizeRange)
  testDb.commit()
  testDb.refresh(workforceSizeRange)
  return workforceSizeRange

@pytest.fixture()
def createAgeRange(testDb) -> AgeRange:
  ageRange = AgeRange(range="Test Age Range")
  testDb.add(ageRange)
  testDb.commit()
  testDb.refresh(ageRange)
  return ageRange

@pytest.fixture()
def createWorkExperienceRange(testDb) -> WorkExperienceRange:
  workExperienceRange = WorkExperienceRange(range="Test Work Experience Range")
  testDb.add(workExperienceRange)
  testDb.commit()
  testDb.refresh(workExperienceRange)
  return workExperienceRange

@pytest.fixture()
def createIndustryTypeLarge(testDb) -> IndustryTypeLarge:
  industryTypeLarge = IndustryTypeLarge(name="Test Industry Type Large")
  testDb.add(industryTypeLarge)
  testDb.commit()
  testDb.refresh(industryTypeLarge)
  return industryTypeLarge

@pytest.fixture()
def createIndustryTypeMedium(testDb) -> IndustryTypeMedium:
  industryTypeMedium = IndustryTypeMedium(name="Test Industry Type Medium")
  testDb.add(industryTypeMedium)
  testDb.commit()
  testDb.refresh(industryTypeMedium)
  return industryTypeMedium

@pytest.fixture()
def createFactory(testDb, createWorkforceSizeRange) -> Factory:
  factory = Factory(
    name="Test Factory",
    workforceSizeRange_id=createWorkforceSizeRange.id
  )
  testDb.add(factory)
  testDb.commit()
  testDb.refresh(factory)

  return factory

@pytest.fixture()
def createWorker(testDb, createAgeRange, createWorkExperienceRange) -> Worker:
  worker = Worker(
    name="Test Worker",
    ageRange_id=createAgeRange.id,
    sex="남",
    workExperienceRange_id=createWorkExperienceRange.id
  )
  testDb.add(worker)
  testDb.commit()
  testDb.refresh(worker)

  return worker

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
def createIncident(testDb, createFactory, createThreatType, createWorkType, createIndustryTypeLarge, createIndustryTypeMedium, createWorker) -> Incident:
  incident = Incident(
    worker_id=createWorker.id,
    industryTypeLarge_id=createIndustryTypeLarge.id,
    industryTypeMedium_id=createIndustryTypeMedium.id,
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

def testIncidentBaseToModel(testDb, createIncident):
  dateUsed = datetime.now()
  incidentBase = IncidentBase(
    worker_id=1,
    industryTypeLarge_id=1,
    industryTypeMedium_id=1,
    threatType_id=1,
    threatLevel=1,
    workType_id=1,
    description="Test Description",
    date=dateUsed,
    factory_id=1
  )
  incident = Incident(**incidentBase.model_dump())
  assert incident.worker_id == 1
  assert incident.industryTypeLarge_id == 1
  assert incident.industryTypeMedium_id == 1
  assert incident.threatType_id == 1
  assert incident.threatLevel == 1
  assert incident.workType_id == 1
  assert incident.description == "Test Description"
  assert incident.factory_id == 1
  assert incident.date == dateUsed

def testIncidentModel(testDb, createIncident, createFactory):
  # Test incident creation
  assert createIncident.id is not None
  assert createIncident.threatType_id == 1
  assert createIncident.threatLevel == 1
  assert createIncident.workType_id == 1
  assert createIncident.description == "Test Description"
  assert createIncident.factory_id == 1

  # Test incident retrieval
  retrievedIncident = testDb.query(Incident).filter(Incident.id == createIncident.id).first()
  assert retrievedIncident is not None
  assert retrievedIncident.threatType_id == createIncident.threatType_id
  assert retrievedIncident.threatLevel == createIncident.threatLevel
  assert retrievedIncident.workType_id == createIncident.workType_id
  assert retrievedIncident.description == createIncident.description
  assert retrievedIncident.factory_id == createFactory.id

# Pydantic model tests
def testFactoryResponseModel(testDb, createFactory):
  factoryResponse = convertDBModelintoResponseModel(createFactory, testDb)
  assert factoryResponse.id == createFactory.id
  assert factoryResponse.name == createFactory.name
  assert factoryResponse.workforceSizeRange.id == createFactory.workforceSizeRange_id

def testIncidentResponseModel(testDb, createIncident):
  incidentResponse = convertIncidentToResponse(createIncident, testDb)
  assert incidentResponse.id == createIncident.id
  assert incidentResponse.threatType.id == createIncident.threatType_id
  assert incidentResponse.threatLevel == createIncident.threatLevel
  assert incidentResponse.workType.id == createIncident.workType_id
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
  assert data["workforceSizeRange"]["id"] == createFactory.workforceSizeRange_id

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
  assert data["worker"]["id"] == createIncident.worker_id
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

def testAddIncident(testDb, createIncident):
  incidentData = {
    "threatType_id": createIncident.threatType_id,
    "threatLevel": createIncident.threatLevel,
    "industryTypeLarge_id": createIncident.industryTypeLarge_id,
    "industryTypeMedium_id": createIncident.industryTypeMedium_id,
    "workType_id": createIncident.workType_id,
    "description": "New Test Description",
    "date": datetime.now().isoformat(),
    "factory_id": createIncident.factory_id,
    "worker_id": createIncident.worker_id
  }
  response = client.post("/incidents", json=incidentData)
  assert response.status_code == 200
  data = response.json()
  assert data["description"] == incidentData["description"]
  assert data["factory"]["id"] == incidentData["factory_id"]
  assert data["threatType"]["id"] == incidentData["threatType_id"]
  assert data["workType"]["id"] == incidentData["workType_id"]

def testAddIncidentInvalidFactory(testDb, createIncident):
  incidentData = {
    "threatType_id": createIncident.threatType_id,
    "threatLevel": createIncident.threatLevel,
    "industryTypeLarge_id": createIncident.industryTypeLarge_id,
    "industryTypeMedium_id": createIncident.industryTypeMedium_id,
    "workType_id": createIncident.workType_id,
    "description": "New Test Description",
    "date": datetime.now().isoformat(),
    "factory_id": 9999,
    "worker_id": createIncident.worker_id
  }
  response = client.post("/incidents", json=incidentData)
  assert response.status_code == 404
