from fastapi import APIRouter
from app.models.analysis import BlogRequest, SchemaRequest
from app.services.ai_optimizer import ai_optimizer

router = APIRouter()

@router.post("/generate-blog")
async def generate_blog(request: BlogRequest):
    """Generate a viral blog post outline."""
    return await ai_optimizer.generate_blog_post(request.keyword, request.topic)

@router.post("/generate-schema")
async def generate_schema(request: SchemaRequest):
    """Generate JSON-LD Schema markup."""
    return await ai_optimizer.generate_schema(request.page_data)
