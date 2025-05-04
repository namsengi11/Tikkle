import uvicorn

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Set
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware

class Incident(BaseModel):
  id: int
  title: str
  description: str
  date: datetime
  factory_id: int

class newIncident(BaseModel):
  title: str
  description: str
  date: datetime
  factory_id: int

class Incidents(BaseModel):
  incidents: List[Incident]

class Factory(BaseModel):
  id: int
  name: str

class Factories(BaseModel):
  factories: List[Factory]

app = FastAPI()

# allowedIps: Set[str] = {
#   "127.0.0.1",
# }

# # Custom middleware for IP restriction
# class IpRestrictionMiddleware(BaseHTTPMiddleware):
#   async def dispatch(self, request: Request, call_next):
#     clientIp = request.client.host
#     if clientIp not in allowedIps:
#       return JSONResponse(
#         status_code=status.HTTP_403_FORBIDDEN,
#         content={"detail": "Access forbidden. Your IP is not allowed."}
#       )
#     return await call_next(request)

# # Add the IP restriction middleware
# app.add_middleware(IpRestrictionMiddleware)

origins = [
  "http://127.0.0.1:5173",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

memory = []
factories = Factories(factories=[Factory(id=0, name="공장1"), Factory(id=1, name="공장2")])

@app.get("/incidents", response_model=Incidents)
def get_incidents():
  return Incidents(incidents=memory)

@app.post("/incidents", response_model=Incident)
def add_incident(incident: newIncident):
  # Assign an id to the incident
  new_incident = Incident(id=len(memory) + 1, **incident.model_dump())
  memory.append(new_incident)
  return new_incident

@app.get("/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: int):
  return memory[incident_id]

@app.get("/incidents/factory/{factory_id}", response_model=Incidents)
def get_incidents_by_factory(factory_id: int):
  print(memory)
  return Incidents(incidents=[incident for incident in memory if incident.factory_id == factory_id])

@app.get("/factories", response_model=Factories)
def get_factories():
  return factories

@app.get("/factories/{factory_id}", response_model=Factory)
def get_factory(factory_id: int):
  return factories.factories[factory_id]

if __name__ == "__main__":
  uvicorn.run(app, host="127.0.0.1", port=8000)