import sys
import os
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
from jose import jwt

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from auth.auth_db import Base, User, get_db
from auth.auth_model import CreateUser, Token
from auth.auth import validateUsername, validatePassword, authenticateUser, createAccessToken, getCurrentUser, bcrypt_context
from main import app

# Setup test database
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
  TEST_DATABASE_URL,
  connect_args={"check_same_thread": False},
  poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the test database
Base.metadata.create_all(bind=engine)

# Create test client
client = TestClient(app)

# Fixtures
@pytest.fixture
def testDb():
  db = TestingSessionLocal()
  app.dependency_overrides[get_db] = lambda: db
  try:
    yield db
  finally:
    # Clear all users after each test
    db.query(User).delete()
    db.commit()
    count = db.query(User).count()
    print(f"Users remaining after cleanup: {count}")
    db.close()

@pytest.fixture
def testUser(testDb):
  hashedPassword = bcrypt_context.hash("Test1234!")
  user = User(username="testuser", hashed_password=hashedPassword)
  testDb.add(user)
  testDb.commit()
  testDb.refresh(user)
  return user

# Tests for user creation
def testCreateUserSuccess(testDb):
  before_count = testDb.query(User).count()
  print(f"Users before test: {before_count}")
  response = client.post(
    "/auth/user",
    json={"username": "newuser", "password": "Password123!"}
  )
  after_count = testDb.query(User).count()
  print(f"Users after test: {after_count}")
  print(response.json())
  assert response.status_code == 201

def testCreateUserInvalidUsername(testDb):
  # Too short
  response = client.post(
    "/auth/user",
    json={"username": "abc", "password": "Password123!"}
  )
  assert response.status_code == 400
  assert "at least 5 characters" in response.json()["detail"]

  # Invalid characters
  response = client.post(
    "/auth/user",
    json={"username": "user@name", "password": "Password123!"}
  )
  assert response.status_code == 400
  assert "only contain letters" in response.json()["detail"]

def testCreateUserDuplicate(testUser, testDb):
  response = client.post(
    "/auth/user",
    json={"username": "testuser", "password": "Password123!"}
  )
  assert response.status_code == 400
  assert "already exists" in response.json()["detail"]

def testCreateUserWeakPassword(testDb):
  # Too short
  response = client.post(
    "/auth/user",
    json={"username": "validuser", "password": "Pass1!"}
  )
  assert response.status_code == 400
  assert "at least 8 characters" in response.json()["detail"]

  # No uppercase
  response = client.post(
    "/auth/user",
    json={"username": "validuser", "password": "password123!"}
  )
  assert response.status_code == 400
  assert "uppercase letter" in response.json()["detail"]

  # No lowercase
  response = client.post(
    "/auth/user",
    json={"username": "validuser", "password": "PASSWORD123!"}
  )
  assert response.status_code == 400
  assert "lowercase letter" in response.json()["detail"]

  # No number
  response = client.post(
    "/auth/user",
    json={"username": "validuser", "password": "Password!"}
  )
  assert response.status_code == 400
  assert "one number" in response.json()["detail"]

  # No special character
  response = client.post(
    "/auth/user",
    json={"username": "validuser", "password": "Password123"}
  )
  assert response.status_code == 400
  assert "special character" in response.json()["detail"]

# Tests for authentication
def testAuthenticateUserSuccess(testUser, testDb):
  result = authenticateUser("testuser", "Test1234!", testDb)
  assert result is True

def testAuthenticateUserInvalidUsername(testUser, testDb):
  result = authenticateUser("wronguser", "Test1234!", testDb)
  assert result is False

def testAuthenticateUserInvalidPassword(testUser, testDb):
  result = authenticateUser("testuser", "WrongPass123!", testDb)
  assert result is False

# Tests for token generation and validation
@patch.dict(os.environ, {"AUTH_KEY": "testsecretkey", "ALGORITHM": "HS256", "ACCESS_TOKEN_EXPIRE_MINUTES": "30"})
def testCreateAccessToken():
  token = createAccessToken("testuser")
  decoded = jwt.decode(token, "testsecretkey", algorithms=["HS256"])
  assert decoded["sub"] == "testuser"
  # Check that expiration is roughly 30 minutes in the future
  expTime = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
  expectedExp = datetime.now(timezone.utc) + timedelta(minutes=30)
  assert abs((expTime - expectedExp).total_seconds()) < 10  # Allow small difference

@patch.dict(os.environ, {"AUTH_KEY": "testsecretkey", "ALGORITHM": "HS256"})
def testGetCurrentUserSuccess():
  # Create a valid token
  payload = {
    "sub": "testuser",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
  }
  token = jwt.encode(payload, "testsecretkey", algorithm="HS256")

  user = getCurrentUser(token)
  assert user["username"] == "testuser"

@patch.dict(os.environ, {"AUTH_KEY": "testsecretkey", "ALGORITHM": "HS256"})
def testGetCurrentUserInvalidToken():
  with pytest.raises(Exception) as excinfo:
    getCurrentUser("invalid.token.string")
  assert "Could not validate credentials" in str(excinfo.value)

# Tests for login endpoint
def testLoginSuccess(testUser):
  response = client.post(
    "/auth/token",
    data={"username": "testuser", "password": "Test1234!"}
  )
  assert response.status_code == 200
  assert "access_token" in response.json()
  assert response.json()["token_type"] == "Bearer"

def testLoginInvalidCredentials(testUser):
  response = client.post(
    "/auth/token",
    data={"username": "testuser", "password": "WrongPassword123!"}
  )
  assert response.status_code == 401
  assert "Invalid username or password" in response.json()["detail"]

# Tests for validation functions
def testValidateUsernameSuccess(testDb):
  assert validateUsername("validuser", testDb) is True

def testValidatePasswordSuccess(testDb):
  assert validatePassword("ValidPass123!", testDb) is True
