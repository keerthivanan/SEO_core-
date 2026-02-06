from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api import analyze, tools, rewrite, generate, reports
from app.core.config import settings
from app.services.database import db
from app.core.logging import setup_logging, set_request_id
from app.middleware.rate_limit import limiter, rate_limit_exceeded_handler, RateLimits
from app.middleware.security import SecurityMiddleware, RequestLoggingMiddleware
from app.models.analysis import AnalysisRequest
from app.services.pipeline import AnalysisPipeline
from slowapi.errors import RateLimitExceeded
import logging
import uvicorn

# Setup enterprise logging
setup_logging()
logger = logging.getLogger(__name__)

# Suppress noise for "World-Class Clean" terminal
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)


# FastAPI app with enterprise configuration
app = FastAPI(
    title=settings.PROJECT_NAME + " - Enterprise Edition",
    description="🏢 Enterprise-Grade Titan ML 2.10 Protocol - 12-Step Neural SEO Intelligence with Rate Limiting, Security Hardening, and Structured Logging",
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Titan ML 2.0 Feature Flag Logic
from app.ml import TITAN_ML_AVAILABLE

@app.on_event("startup")
async def startup_event():
    """
    Titan ML Mission Control - Startup Diagnostic
    Verifies all enterprise subsystems and keys on boot.
    """
    logger.info("🚀 TITAN ML MISSION CONTROL: INITIALIZING DIAGNOSTIC...")
    
    diagnostic = {
        "OPENAI_ENGINE": "✅ ACTIVE" if settings.OPENAI_API_KEY else "❌ MISSING",
        "ANTHROPIC_ENGINE": "✅ ACTIVE" if settings.ANTHROPIC_API_KEY else "⚠️ OPTIONAL (FALLBACK ACTIVE)",
        "SERP_ENGINE": "✅ ACTIVE" if settings.SERPER_API_KEY else "❌ MISSING",
        "PAGESPEED_ENGINE": "✅ ACTIVE" if settings.GOOGLE_API_KEY else "❌ MISSING",
        "DATABASE_CORE": "✅ CONNECTED" if db.check_connection() else "❌ DISCONNECTED",
        "VECTOR_ML": "✅ OPERATIONAL" if TITAN_ML_AVAILABLE else "⚠️ LIGHTWEIGHT MODE"
    }
    
    # Print a professional diagnostic table to console
    print("\n" + "="*50)
    print("      RANKFORGE AI - ENTERPRISE DIAGNOSTIC")
    print("="*50)
    for service, status in diagnostic.items():
        print(f"  {service:<20} {status}")
    print("="*50 + "\n")

    # Final logic check: Are critical components missing?
    critical_missing = [k for k, v in diagnostic.items() if "❌" in v]
    if critical_missing:
        logger.warning(f"🚨 CRITICAL COMPONENTS MISSING: {', '.join(critical_missing)}. Please check your .env file!")
    else:
        logger.info("✅ ALL SYSTEMS NOMINAL - TITAN ML 2.10 ONLINE")


# Add rate limiter state and exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Enterprise Security Middleware
app.add_middleware(SecurityMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# CORS Configuration
allowed_origins = [
    "http://localhost:3000",
    "https://*.vercel.app",
    "https://rankforge.ai",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Response-Time", "X-Request-ID"],
)

# Include API routers
app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(tools.router, prefix="/api", tags=["tools"])
app.include_router(rewrite.router, prefix="/api", tags=["rewrite"])
app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(reports.router, prefix="/api", tags=["reports"])

@app.get("/health", tags=["System"])
@limiter.limit(RateLimits.API_DEFAULT)
async def health_check(request: Request):
    """
    Enterprise health check endpoint
    Returns system status, database connectivity, and performance metrics
    """
    db_status = db.check_connection()
    req_id = set_request_id()
    
    logger.info("HEALTH_CHECK_REQUESTED", extra={"request_id": req_id})
    
    return {
        "status": "operational",
        "tier": "enterprise",
        "database": "connected" if db_status else "disconnected",
        "version": settings.VERSION,
        "engine": "Titan ML 2.10 Protocol Active",
        "features": {
            "rate_limiting": True,
            "security_headers": True,
            "structured_logging": True,
            "error_monitoring": True
        },
        "request_id": req_id
    }

@app.websocket("/ws/analyze")
async def analyze_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        
        if not data.get('url') or not data.get('target_keyword'):
             await websocket.send_json({"type": "error", "message": "Missing URL or Keyword"})
             return

        request = AnalysisRequest(**data)
        pipeline = AnalysisPipeline(request)
        results = await pipeline.run(websocket)
        await websocket.send_json({"type": "complete", "results": results})
        
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        await websocket.send_json({"type": "error", "message": str(e)})

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

