from fastapi import APIRouter
from app.models.analysis import AnalysisRequest
from app.services.pipeline import AnalysisPipeline

router = APIRouter()

@router.post("/analyze")
async def start_analysis(request: AnalysisRequest):
    """Start a new analysis via POST (Alternative to WebSocket)"""
    pipeline = AnalysisPipeline(request)
    return await pipeline.run()
