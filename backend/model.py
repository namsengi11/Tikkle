from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Literal, Dict


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


## Risk assessment 관련 로직
class BasicInformation(BaseModel):
    date: datetime
    name: str
    factory: str
    image: str
    description: str


class AccidentPossibility(BaseModel):
    risk_score: int
    risk_level: Literal["Low", "Medium", "High"]
    predicted_probability: float


class MicroAccidentSeverity(BaseModel):
    probabilities: Dict[str, float]
    most_likely_time: str


class RiskAssessmentRequest(BaseModel):
    날짜: datetime
    이름: str
    발생공장: str
    사진: str
    설명: str
    중업종: str
    대업종: str
    발생형태: str
    규모: str
    성별: str
    연령: str
    근무기간: str
    작업종류: str
    보호구착용: Literal["y", "n"]
    유사사고경험: Literal["y", "n"]
    안전감독자: Literal["y", "n"]
    위험정도: float
    Q10_6_1: int
    Q3_1_2: int
    Q15_8: int
    SQ3_1: int
    Q24_1: int


class RiskAssessmentResponse(BaseModel):
    basic_information: BasicInformation
    accident_possibility: AccidentPossibility
    micro_accident_severity: MicroAccidentSeverity
