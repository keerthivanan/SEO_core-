from app.core.config import settings
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
import json
import logging


logger = logging.getLogger(__name__)

class AIOptimizer:
    def __init__(self):
        self.anthropic_client = None
        self.openai_client = None
        
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            
        if not self.anthropic_client and not self.openai_client:
            logger.warning("⚠️ No AI API Keys found (Anthropic or OpenAI). AI features will be disabled.")
    
    async def optimize_content(self, page_data: dict, keyword: str, gaps: dict = None) -> dict:
        """Use AI to generate optimized content (Hybrid Engine)"""
        if not self.anthropic_client and not self.openai_client:
            return {"error": "AI API Key missing. Please add OPENAI_API_KEY or ANTHROPIC_API_KEY to .env"}
        
        gap_context = []
        if gaps:
            if 'priority_fixes' in gaps:
                 gap_context = gaps['priority_fixes']
            elif isinstance(gaps, list):
                 gap_context = gaps
            else:
                 gap_context = gaps

        prompt = f"""
You are a world-class SEO expert. Analyze this webpage and generate optimized content.

Target Keyword: {keyword}
Current Title: {page_data.get('title', 'None')}
Current Meta: {page_data.get('meta_description', 'None')}
Current H1: {page_data.get('h1', ['None'])[0] if page_data.get('h1') else 'None'}
Word Count: {page_data.get('word_count', 0)}

Identified Gaps:
{json.dumps(gap_context, indent=2, default=str)}

Generate SEO-optimized content in JSON format:
{{
  "optimized_title": "Perfect SEO title (50-60 chars, includes keyword)",
  "optimized_meta": "Compelling meta description (150-160 chars, includes keyword, has CTA)",
  "optimized_h1": "Perfect H1 (includes keyword naturally)",
  "content_outline": [
    "Introduction paragraph suggestion",
    "H2: Main Section 1 title",
    "H2: Main Section 2 title",
    "H2: FAQ section",
    "Conclusion paragraph suggestion"
  ],
  "keyword_strategy": {{
    "primary": "{keyword}",
    "secondary": ["related keyword 1", "related keyword 2", "related keyword 3"],
    "lsi_keywords": ["LSI 1", "LSI 2", "LSI 3", "LSI 4", "LSI 5"]
  }},
  "image_suggestions": [
    {{"alt": "Alt text suggestion 1", "purpose": "Hero image"}},
    {{"alt": "Alt text suggestion 2", "purpose": "Supporting visual"}}
  ],
  "schema_markup": {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Article headline",
    "description": "Article description"
  }}
}}

Make it world-class, conversion-optimized, and ready to rank #1.
Return ONLY valid JSON, no markdown, no explanation.
"""
        return await self._call_ai(prompt)

    async def generate_blog_post(self, keyword: str, topic: str = None) -> dict:
        """Generate a viral blog post structure for traffic injection."""
        if not self.anthropic_client and not self.openai_client:
            return {"error": "AI API Key missing"}
        
        prompt = f"""
You are a viral content strategist. Create a "Traffic Magnet" blog post outline for the keyword: "{keyword}".

Target Audience: High-intent buyers.
Tone: Authoritative, Data-Driven, slightly contrarian.

Output JSON:
{{
    "title": "Viral Clickbait Title (but honest)",
    "slug": "url-slug-optimized",
    "meta_description": "High CTR meta description",
    "hook": "First paragraph that hooks the reader instantly",
    "outline": [
        {{ "heading": "H2 Section Title", "key_points": ["point 1", "point 2"] }},
        {{ "heading": "H2 Section Title", "key_points": ["data point", "argument"] }}
    ],
    "faq": [
        {{ "question": "Common user question?", "answer": "Direct answer" }}
    ]
}}
"""
        return await self._call_ai(prompt)

    async def _call_ai(self, prompt: str) -> dict:
        """Internal helper to call either Anthropic or OpenAI based on availability"""
        try:
            # Prefer Anthropic if available (Titan ML Default)
            if self.anthropic_client:
                response = await self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
            # Fallback to OpenAI
            else:
                response = await self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"} if "JSON" in prompt else None
                )
                content = response.choices[0].message.content

            # Cleanup response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            return json.loads(content)
        except Exception as e:
            logger.error(f"AI Call Failed: {e}")
            return {"error": str(e)}

ai_optimizer = AIOptimizer()
