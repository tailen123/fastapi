from pydantic import BaseModel, validator, Field, confloat


class ResultBase(BaseModel):
    id: int
    text: str
    text_zh: str
    result_id: int
    is_del: bool
    source: str
    message_id: int


class Result(ResultBase):
    score: int = Field(..., ge=0, le=2)

    class Config:
        from_attributes = True


class Result_list(BaseModel):
    results: list[Result]


class Acc(BaseModel):
    message_id: int
    source: str
    todonums: int
    onenums: int
    twonums: int
    total: int


class Hard(BaseModel):
    message_id: int
    todonums: int
    onenums: int
    twonums: int
    total: int
    reason_type: int
    source: str


class InputDiff(BaseModel):
    diff_level: float = Field(ge=0.0, le=1.0)
