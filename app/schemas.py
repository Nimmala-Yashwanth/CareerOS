from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Status = Literal['saved', 'applied', 'assessment', 'interview', 'offer', 'rejected']
class Register(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=10, max_length=128)
class Login(Register):
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
class ApplicationIn(BaseModel):
    company: str = Field(min_length=1, max_length=150)
    role: str = Field(min_length=1, max_length=150)
    status: Status = 'applied'
    location: str = Field(default='', max_length=150)
    job_url: str = Field(default='', max_length=1000)
    description: str = Field(default='', max_length=30000)
    notes: str = Field(default='', max_length=10000)
class ApplicationPatch(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=150)
    role: str | None = Field(default=None, min_length=1, max_length=150)
    status: Status | None = None
    location: str | None = Field(default=None, max_length=150)
    job_url: str | None = Field(default=None, max_length=1000)
    description: str | None = Field(default=None, max_length=30000)
    notes: str | None = Field(default=None, max_length=10000)
class ApplicationOut(ApplicationIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
class SkillsIn(BaseModel):
    skills: list[str] = Field(max_length=100)
class MatchIn(BaseModel):
    job_description: str = Field(min_length=20, max_length=30000)
