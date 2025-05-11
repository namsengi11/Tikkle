from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class FactoryResponse(BaseModel):
  id: int
  name: str

  class Config:
    from_attributes = True

class FactoryResponses(BaseModel):
  factories: List[FactoryResponse]

class ThreatTypeResponse(BaseModel):
  id: int
  name: str

  class Config:
    from_attributes = True

class ThreatTypeResponses(BaseModel):
  threatTypes: List[ThreatTypeResponse]

class WorkTypeResponse(BaseModel):
  id: int
  name: str

  class Config:
    from_attributes = True

class WorkTypeResponses(BaseModel):
  workTypes: List[WorkTypeResponse]

class CheckQuestionResponse(BaseModel):
  id: int
  question: str

  class Config:
    from_attributes = True

class CheckQuestionResponses(BaseModel):
  checks: List[CheckQuestionResponse]

class IncidentBase(BaseModel):
  threatType_id: int
  threatLevel: int
  workType_id: int
  description: str
  date: datetime
  factory_id: int

class IncidentInput(IncidentBase):
  check_responses: dict[int, bool]

class IncidentDBModel(IncidentBase):
  id: int

  class Config:
    from_attributes = True

class IncidentResponse(BaseModel):
  id: int
  threatType: ThreatTypeResponse
  threatLevel: int
  workType: WorkTypeResponse
  description: str
  date: datetime
  factory: FactoryResponse
  check_responses: dict[CheckQuestionResponse, str]

class IncidentResponses(BaseModel):
  incidents: List[IncidentResponse]



