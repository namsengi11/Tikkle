import uvicorn
import json
import logging
import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, status, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from db import get_db, save_risk_assessment
from db import (
    Incident,
    Factory,
    ThreatType,
    WorkType,
    CheckQuestion,
    CheckResponse,
    AgeRange,
    WorkExperienceRange,
    IndustryTypeLarge,
    IndustryTypeMedium,
    WorkforceSizeRange,
    Worker,
)
from model import (
    IncidentBase,
    IncidentResponse,
    FactoryResponse,
    IncidentResponses,
    FactoryResponses,
    ThreatTypeResponse,
    ThreatTypeResponses,
    WorkTypeResponse,
    WorkTypeResponses,
    CheckQuestionResponse,
    CheckQuestionResponses,
    AgeRangeResponse,
    WorkExperienceRangeResponse,
    IndustryTypeLargeResponse,
    IndustryTypeMediumResponse,
    AgeRangeResponses,
    WorkExperienceRangeResponses,
    IndustryTypeLargeResponses,
    IndustryTypeMediumResponses,
    WorkforceSizeRangeResponse,
    WorkerResponse,
    WorkerResponses,
    WorkforceSizeRangeResponses,
    WorkerInput,
    RiskAssessmentRequest,
    RiskAssessmentResponse,
)
from predict import predict_full_risk_assessment
from logging_middleware import LoggingMiddleware

app = FastAPI(root_path="/api")

logger = logging.getLogger("fastapi")
# Add the middleware to the app
app.add_middleware(LoggingMiddleware)

# Only allow requests from the local host (proxied by nginx)
origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:5173",  # dev frontend
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

varNameToModel = {
    "incident": Incident,
    "factory": Factory,
    "threatType": ThreatType,
    "workType": WorkType,
    "checkQuestion": CheckQuestion,
    "ageRange": AgeRange,
    "workExperienceRange": WorkExperienceRange,
    "industryTypeLarge": IndustryTypeLarge,
    "industryTypeMedium": IndustryTypeMedium,
    "workforceSizeRange": WorkforceSizeRange,
    "worker": Worker,
}

varNameToResponseModel = {
    "incident": IncidentResponse,
    "factory": FactoryResponse,
    "threatType": ThreatTypeResponse,
    "workType": WorkTypeResponse,
    "checkQuestion": CheckQuestionResponse,
    "ageRange": AgeRangeResponse,
    "workExperienceRange": WorkExperienceRangeResponse,
    "industryTypeLarge": IndustryTypeLargeResponse,
    "industryTypeMedium": IndustryTypeMediumResponse,
    "workforceSizeRange": WorkforceSizeRangeResponse,
    "worker": WorkerResponse,
}


def convertDBModelintoResponseModel(
    dbModel, db: Session, additionalAttributes: dict = {}
) -> BaseModel:
    model = varNameToModel[dbModel.typeToString()]
    dbModelDict = dbModel.__dict__.copy()
    dbModelDict.pop("_sa_instance_state")
    modelDict = dbModelDict.copy()
    for key, value in dbModelDict.items():
        if key.endswith("_id"):
            model = varNameToModel[key.replace("_id", "")]
            object = db.query(model).filter(model.id == value).first()
            if object is None:
                logger.error(
                    f"{datetime.now()}: {key.replace('_id', '')} of id {value} not found"
                )
                raise HTTPException(
                    status_code=404, detail=f"{key.replace('_id', '')} not found"
                )
            else:
                modelDict[key.replace("_id", "")] = convertDBModelintoResponseModel(
                    object, db
                )
                modelDict.pop(key)
    modelDict.update(additionalAttributes)
    responseModel = varNameToResponseModel[dbModel.typeToString()]
    return responseModel.model_validate(modelDict)


def convertIncidentToResponse(incident: Incident, db: Session) -> IncidentResponse:
    # get check responses for response
    checkResponses = (
        db.query(CheckResponse).filter(CheckResponse.incident_id == incident.id).all()
    )
    checkResponsesDict = dict()
    for checkResponse in checkResponses:
        checkQuestion = (
            db.query(CheckQuestion)
            .filter(CheckQuestion.id == checkResponse.question_id)
            .first()
        )
        checkResponsesDict[CheckQuestionResponse.model_validate(checkQuestion)] = (
            checkResponse.response
        )
    return convertDBModelintoResponseModel(
        incident, db, additionalAttributes={"check_responses": checkResponsesDict}
    )


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
    factoryResponses = []
    for factory in factories:
        try:
            factoryResponse = convertDBModelintoResponseModel(factory, db)
            factoryResponses.append(factoryResponse)
        except HTTPException as e:
            logger.error(
                f"{datetime.now()}: Error processing factory {factory.id}: {e.detail}"
            )
            # Skip this factory but continue processing others
    return FactoryResponses(factories=factoryResponses)


@app.get("/factories/{factory_id}", response_model=FactoryResponse)
def getFactory(factory_id: int, db: Session = Depends(get_db)):
    factory = db.query(Factory).filter(Factory.id == factory_id).first()
    if factory is None:
        raise HTTPException(status_code=404, detail="Factory not found")

    return convertDBModelintoResponseModel(factory, db)


@app.get("/threatTypes", response_model=ThreatTypeResponses)
def getThreatTypes(db: Session = Depends(get_db)):
    threatTypes = db.query(ThreatType).all()
    return ThreatTypeResponses(
        threatTypes=[
            ThreatTypeResponse.model_validate(threatType) for threatType in threatTypes
        ]
    )


@app.get("/workTypes", response_model=WorkTypeResponses)
def getWorkTypes(db: Session = Depends(get_db)):
    workTypes = db.query(WorkType).all()
    return WorkTypeResponses(
        workTypes=[WorkTypeResponse.model_validate(workType) for workType in workTypes]
    )


@app.get("/checks", response_model=CheckQuestionResponses)
def getCheckQuestions(db: Session = Depends(get_db)):
    checkQuestions = db.query(CheckQuestion).all()
    return CheckQuestionResponses(
        checks=[
            CheckQuestionResponse.model_validate(checkQuestion)
            for checkQuestion in checkQuestions
        ]
    )


@app.get("/workers", response_model=WorkerResponses)
def getWorkers(db: Session = Depends(get_db)):
    workers = db.query(Worker).all()
    workers = [convertDBModelintoResponseModel(worker, db) for worker in workers]
    return WorkerResponses(workers=workers)


@app.post("/workers", response_model=WorkerResponse)
def addWorker(worker: WorkerInput, db: Session = Depends(get_db)):
    new_Worker = Worker(**worker.model_dump())
    db.add(new_Worker)
    db.commit()
    db.refresh(new_Worker)
    return convertDBModelintoResponseModel(new_Worker, db)


@app.get("/industryTypes/large", response_model=IndustryTypeLargeResponses)
def getIndustryTypesLarge(db: Session = Depends(get_db)):
    industryTypesLarge = db.query(IndustryTypeLarge).all()
    industryTypesLarge = [
        convertDBModelintoResponseModel(industryTypeLarge, db)
        for industryTypeLarge in industryTypesLarge
    ]
    return IndustryTypeLargeResponses(industryTypeLarge=industryTypesLarge)


@app.get("/industryTypes/medium", response_model=IndustryTypeMediumResponses)
def getIndustryTypesMedium(db: Session = Depends(get_db)):
    industryTypesMedium = db.query(IndustryTypeMedium).all()
    industryTypesMedium = [
        convertDBModelintoResponseModel(industryTypeMedium, db)
        for industryTypeMedium in industryTypesMedium
    ]
    return IndustryTypeMediumResponses(industryTypeMedium=industryTypesMedium)


@app.get("/workforceSizeRanges", response_model=WorkforceSizeRangeResponses)
def getWorkforceSizeRanges(db: Session = Depends(get_db)):
    workforceSizeRanges = db.query(WorkforceSizeRange).all()
    workforceSizeRanges = [
        convertDBModelintoResponseModel(workforceSizeRange, db)
        for workforceSizeRange in workforceSizeRanges
    ]
    return WorkforceSizeRangeResponses(workforceSizeRanges=workforceSizeRanges)


@app.get("/ageRanges", response_model=AgeRangeResponses)
def getAgeRanges(db: Session = Depends(get_db)):
    ageRanges = db.query(AgeRange).all()
    ageRanges = [
        convertDBModelintoResponseModel(ageRange, db) for ageRange in ageRanges
    ]
    return AgeRangeResponses(ageRanges=ageRanges)


@app.get("/workExperienceRanges", response_model=WorkExperienceRangeResponses)
def getWorkExperienceRanges(db: Session = Depends(get_db)):
    workExperienceRanges = db.query(WorkExperienceRange).all()
    workExperienceRanges = [
        convertDBModelintoResponseModel(workExperienceRange, db)
        for workExperienceRange in workExperienceRanges
    ]
    return WorkExperienceRangeResponses(workExperienceRanges=workExperienceRanges)


# Risk assessment Post 리퀘스트 api
@app.post(
    "/risk-assessment",
    response_model=RiskAssessmentResponse,
)
def risk_assessment(payload: RiskAssessmentRequest = Body(...), db=Depends(get_db)):
    try:
        data_dict = payload.model_dump()
        input_json_str = json.dumps(data_dict, ensure_ascii=False, default=str)
        result = predict_full_risk_assessment(input_json_str)
        record = save_risk_assessment(db, result)
        return record.to_dict()
    except Exception as e:
        logger.error(f"RiskAssessment error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
