from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class FactoryBase(BaseModel):
  name: str

class FactoryResponse(FactoryBase):
  id: int

  class Config:
    from_attributes = True

class FactoryResponses(BaseModel):
  factories: List[FactoryResponse]

class IncidentBase(BaseModel):
  title: str
  description: str
  date: datetime
  factory_id: int

class IncidentDBModel(IncidentBase):
  id: int

  class Config:
    from_attributes = True

class IncidentResponse(IncidentDBModel):
  factory: FactoryResponse

class IncidentResponses(BaseModel):
  incidents: List[IncidentResponse]

