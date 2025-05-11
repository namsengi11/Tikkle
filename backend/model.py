from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class WorkforceSizeRangeResponse(BaseModel):
  id: int
  range: str

  class Config:
    from_attributes = True

class WorkforceSizeRangeResponses(BaseModel):
  workforceSizeRanges: List[WorkforceSizeRangeResponse]

class FactoryResponse(BaseModel):
  id: int
  name: str
  workforceSizeRange: WorkforceSizeRangeResponse

  class Config:
    from_attributes = True

class FactoryResponses(BaseModel):
  factories: List[FactoryResponse]

class AgeRangeResponse(BaseModel):
  id: int
  range: str

  class Config:
    from_attributes = True

class AgeRangeResponses(BaseModel):
  ageRanges: List[AgeRangeResponse]

class WorkExperienceRangeResponse(BaseModel):
  id: int
  range: str

  class Config:
    from_attributes = True

class WorkExperienceRangeResponses(BaseModel):
  workExperienceRanges: List[WorkExperienceRangeResponse]

class WorkerInput(BaseModel):
  name: str
  ageRange_id: int
  sex: str
  workExperienceRange_id: int

class WorkerResponse(BaseModel):
  id: int
  name: str
  ageRange: AgeRangeResponse
  sex: str
  workExperienceRange: WorkExperienceRangeResponse

  class Config:
    from_attributes = True

class WorkerResponses(BaseModel):
  workers: List[WorkerResponse]

class IndustryTypeLargeResponse(BaseModel):
  id: int
  name: str

  class Config:
    from_attributes = True

class IndustryTypeLargeResponses(BaseModel):
  industryTypeLarge: List[IndustryTypeLargeResponse]

class IndustryTypeMediumResponse(BaseModel):
  id: int
  name: str

  class Config:
    from_attributes = True

class IndustryTypeMediumResponses(BaseModel):
  industryTypeMedium: List[IndustryTypeMediumResponse]

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
  worker_id: int
  industryTypeLarge_id: int
  industryTypeMedium_id: int
  threatType_id: int
  threatLevel: int
  workType_id: int
  description: str
  date: datetime
  factory_id: int

class IncidentInput(IncidentBase):
  check_responses: dict[int, bool]

class IncidentResponse(BaseModel):
  id: int
  worker: WorkerResponse
  industryTypeLarge: IndustryTypeLargeResponse
  industryTypeMedium: IndustryTypeMediumResponse
  threatType: ThreatTypeResponse
  threatLevel: int
  workType: WorkTypeResponse
  description: str
  date: datetime
  factory: FactoryResponse
  check_responses: dict[CheckQuestionResponse, str]

class IncidentResponses(BaseModel):
  incidents: List[IncidentResponse]



