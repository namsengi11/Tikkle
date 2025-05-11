import uvicorn
import json

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from model import IncidentBase, IncidentDBModel, IncidentResponse, FactoryResponse, IncidentResponses, FactoryResponses, ThreatTypeResponse, ThreatTypeResponses, WorkTypeResponse, WorkTypeResponses, CheckQuestionResponse, CheckQuestionResponses
from db import Incident, Factory, ThreatType, WorkType, CheckQuestion, CheckResponse
from logging_middleware import LoggingMiddleware

app = FastAPI(root_path="/api")

# Only allow requests from the local host (proxied by nginx)
origins = [
  "http://127.0.0.1",
  "http://127.0.0.1:5173", # dev frontend
  "http://127.0.0.1:5174",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Add the middleware to the app
app.add_middleware(LoggingMiddleware)

def convertIncidentToResponse(incident: Incident, db: Session) -> IncidentResponse:
  incident = IncidentDBModel.model_validate(incident)
  incidentDict = incident.model_dump()
  # get factory object for response
  incidentDict["factory"] = FactoryResponse.model_validate(db.query(Factory).filter(Factory.id == incident.factory_id).first())

  # get check responses for response
  checkResponses = db.query(CheckResponse).filter(CheckResponse.incident_id == incident.id).all()
  checkResponsesDict = dict()
  for checkResponse in checkResponses:
    checkQuestion = db.query(CheckQuestion).filter(CheckQuestion.id == checkResponse.question_id).first()
    checkResponsesDict[CheckQuestionResponse.model_validate(checkQuestion)] = checkResponse.response
  incidentDict["check_responses"] = checkResponsesDict

  # get threat type object for response
  incidentDict["threatType"] = ThreatTypeResponse.model_validate(db.query(ThreatType).filter(ThreatType.id == incident.threatType_id).first())

  # get work type object for response
  incidentDict["workType"] = WorkTypeResponse.model_validate(db.query(WorkType).filter(WorkType.id == incident.workType_id).first())

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

  new_Incident = Incident(**incident.model_dump())
  db.add(new_Incident)
  db.commit()
  db.refresh(new_Incident)
  return convertIncidentToResponse(new_Incident, db)

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

@app.get("/threatTypes", response_model=ThreatTypeResponses)
def getThreatTypes(db: Session = Depends(get_db)):
  threatTypes = db.query(ThreatType).all()
  return ThreatTypeResponses(threatTypes=[ThreatTypeResponse.model_validate(threatType) for threatType in threatTypes])

@app.get("/workTypes", response_model=WorkTypeResponses)
def getWorkTypes(db: Session = Depends(get_db)):
  workTypes = db.query(WorkType).all()
  return WorkTypeResponses(workTypes=[WorkTypeResponse.model_validate(workType) for workType in workTypes])

@app.get("/checks", response_model=CheckQuestionResponses)
def getCheckQuestions(db: Session = Depends(get_db)):
  checkQuestions = db.query(CheckQuestion).all()
  return CheckQuestionResponses(checks=[CheckQuestionResponse.model_validate(checkQuestion) for checkQuestion in checkQuestions])

if __name__ == "__main__":
  uvicorn.run(app, host="127.0.0.1", port=8000)