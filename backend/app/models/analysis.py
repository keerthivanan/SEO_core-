from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime

class AnalysisRequest(BaseModel):
    url: str # HttpUrl can be strict, using str for flexibility with frontends sans protocol
    target_keyword: str
    user_id: Optional[str] = "guest"
    country_code: str = "us"
    language: str = "en"

class BlogRequest(BaseModel):
    keyword: str
    topic: Optional[str] = None
    target_audience: Optional[str] = "General"

class SchemaRequest(BaseModel):
    url: str
    page_data: Dict[str, Any]

class AnalysisResult(BaseModel):
    analysis_id: str
    url: str
    keyword: str
    seo_score: int
    aeo_score: int = 0
    geo_score: int = 0
    overall_score: int = 0
    optimization_priority: str = "Pending"
    issues: List[Dict[str, Any]]
    opportunities: List[Dict[str, Any]]
    competitor_data: Dict[str, Any]
    ai_recommendations: Dict[str, Any]
    aeo_analysis: Dict[str, Any] = {}
    geo_analysis: Dict[str, Any] = {}
    estimated_ranking: str
    traffic_potential: Dict[str, Any]
    action_plan: Dict[str, List[str]]
    critical_issues: List[Dict[str, Any]]
    processing_time: float
    timestamp: datetime
