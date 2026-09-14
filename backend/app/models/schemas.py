from pydantic import BaseModel, ConfigDict, Field 
from typing import List, Optional 
from datetime import datetime 
from enum import Enum 
# --- VIDEO MODELS --- 
class OscarInfo(BaseModel): 
    category: str 
    year: int 
    won: bool 
# --- VIDEO CREATE MODEL --- 
class VideoCreate(BaseModel): 
    title: str 
    alternative_titles: Optional[List[str]] = [] 
    genre: str 
    release_year: int 
    duration_minutes: int 
    actors: List[str] 
    oscar_info: Optional[List[OscarInfo]] = [] 
    dvd_unit_cost_bs: float = Field(..., gt=0) 
    total_copies_acquired: int = Field(default=1, ge=1) 
# --- COPY MODELS (OCC) --- 
class CopyStatus(str, Enum): 
    AVAILABLE = "available" 
    RENTED = "rented" 
    RETIRED = "retired" 
# --- COPY RESPONSE MODELS --- 
class CopyResponse(BaseModel): 
    model_config = ConfigDict(populate_by_name=True) 
    copy_id: str 
    video_id: str 
    video_title: str 
    status: CopyStatus 
    condition: str = "good" 
    seq_no: Optional[int] = Field(None, alias="_seq_no") 
    primary_term: Optional[int] = Field(None, alias="_primary_term") 
# --- CLIENT MODELS (GEO_POINT) --- 
class GeoLocation(BaseModel): 
    lat: float = Field(..., ge=-90.0, le=90.0) 
    lon: float = Field(..., ge=-180.0, le=180.0) 
# --- CLIENT CREATE MODEL --- 
class ClientCreate(BaseModel): 
    full_name: str 
    ci_nit: str 
    phone: str 
    email: str # Reemplazado EmailStr por str para evitar dependencia de email-validator 
    location: GeoLocation 
    address_description: str 
# --- LOAN MODELS --- 
class LoanItem(BaseModel): 
    copy_id: str 
    video_id: str 
    video_title: str 
    daily_rate_bs: float 
# --- LOAN CREATE REQUEST MODEL --- 
class LoanCreateRequest(BaseModel): 
    client_id: str 
    copy_ids: List[str] = Field(..., min_length=1) 
    rental_days: int = Field(..., ge=1, le=5)