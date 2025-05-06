import uvicorn
import json

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from db import get_db
from sqlalchemy.orm import Session
from typing import List

from model import IncidentBase, FactoryBase, IncidentDBModel, IncidentResponse, FactoryResponse, IncidentResponses, FactoryResponses
from db import Incident, Factory

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
  "http://127.0.0.1:5174",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

def convertIncidentToResponse(incident: Incident, db: Session) -> IncidentResponse:
  incident = IncidentDBModel.model_validate(incident)
  incidentDict = incident.model_dump()
  incidentDict["factory"] = db.query(Factory).filter(Factory.id == incident.factory_id).first()
  return IncidentResponse.model_validate(incidentDict)

@app.get("/incidents", response_model=IncidentResponses)
def getIncidents(db: Session = Depends(get_db)):
  incidents = db.query(Incident).all()
  incidents = [convertIncidentToResponse(incident, db) for incident in incidents]
  return IncidentResponses(incidents=incidents)

@app.post("/incidents", response_model=IncidentResponse)
def addIncident(incident: IncidentBase, db: Session = Depends(get_db)):
  factory = db.query(Factory).filter(Factory.id == incident.factory_id).first()
  if factory is None:
    raise HTTPException(status_code=404, detail="Factory not found")

  new_incident = Incident(**incident.model_dump())
  db.add(new_incident)
  db.commit()
  db.refresh(new_incident)
  return convertIncidentToResponse(new_incident, db)

@app.get("/incidents/{incident_id}", response_model=IncidentResponse)
def getIncident(incident_id: int, db: Session = Depends(get_db)):
  incident = db.query(Incident).filter(Incident.id == incident_id).first()
  if incident is None:
    raise HTTPException(status_code=404, detail="Incident not found")
  return convertIncidentToResponse(incident, db)

@app.get("/incidents/factory/{factory_id}", response_model=IncidentResponses)
def getIncidentsByFactory(factory_id: int, db: Session = Depends(get_db)):
  # Check if the factory exists
  factory = db.query(Factory).filter(Factory.id == factory_id).first()
  if factory is None:
    raise HTTPException(status_code=404, detail="Factory not found")

  incidents = db.query(Incident).filter(Incident.factory_id == factory_id).all()
  incidents = [convertIncidentToResponse(incident, db) for incident in incidents]
  return IncidentResponses(incidents=incidents)

@app.get("/factories", response_model=FactoryResponses)
def getFactories(db: Session = Depends(get_db)):
  factories = db.query(Factory).all()
  return FactoryResponses(factories=[FactoryResponse.model_validate(factory) for factory in factories])

@app.get("/factories/{factory_id}", response_model=FactoryResponse)
def getFactory(factory_id: int, db: Session = Depends(get_db)):
  factory = db.query(Factory).filter(Factory.id == factory_id).first()
  if factory is None:
    raise HTTPException(status_code=404, detail="Factory not found")

  return FactoryResponse.model_validate(factory)

if __name__ == "__main__":
  uvicorn.run(app, host="127.0.0.1", port=8000)