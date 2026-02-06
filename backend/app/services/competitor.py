import httpx
from typing import List, Dict, Any
from app.core.config import settings
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class CompetitorService:
    """
    Service to analyze top competitors from Google SERP.
    Uses Serper.dev API for high-quality, real-time Google results.
    """
    
    SERPER_URL = "https://google.serper.dev/search"
    
    def __init__(self):
        self.api_key = settings.SERPER_API_KEY
    
    async def analyze_competitors(self, keyword: str, country: str = "us") -> Dict[str, Any]:
        """
        Get Top 10 competitors or fallback to simulated data if API key is missing.
        """
        if not self.api_key:
            logger.warning(f"SERPER_API_KEY missing. Generating Simulated Competitor Logic for: {keyword}")
            return self._generate_simulated_competitors(keyword)
            
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': keyword,
            'gl': country,
            'num': 10
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.SERPER_URL, headers=headers, json=payload, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                return self._parse_serp(data)
            except Exception as e:
                logger.error(f"Competitor Analysis Failed: {e}. Falling back to simulation.")
                return self._generate_simulated_competitors(keyword)

    def _generate_simulated_competitors(self, keyword: str) -> Dict[str, Any]:
        """
        Zero-Key Intelligence: Simulates the SERP landscape based on keyword logic.
        """
        kw_slug = keyword.lower().replace(" ", "-")
        simulated = [
            {"position": 1, "title": f"Top Guide: How to Master {keyword}", "url": f"https://expert-seo.com/guide/{kw_slug}", "snippet": f"The definitive guide to {keyword}. Learn the secrets of top-ranking pros.", "domain": "expert-seo.com"},
            {"position": 2, "title": f"{keyword} Best Practices for 2026", "url": f"https://marketing-pro.ai/blog/{kw_slug}-2026", "snippet": f"Updated for 2026: The latest strategies for dominating {keyword} search results.", "domain": "marketing-pro.ai"},
            {"position": 3, "title": f"Why {keyword} Matters for Your Business", "url": f"https://business-logic.com/why-{kw_slug}", "snippet": f"Discover the ROI of {keyword} and why you should start optimizing today.", "domain": "business-logic.com"}
        ]
        return {
            "total_results": "1,240,000 (Estimated)",
            "top_competitors": simulated,
            "analysis_summary": self._analyze_patterns(simulated),
            "is_simulated": True
        }
    
    def _parse_serp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        organic = data.get('organic', [])
        competitors = []
        
        for result in organic:
            try:
                competitors.append({
                    "position": result.get('position'),
                    "title": result.get('title'),
                    "url": result.get('link'),
                    "snippet": result.get('snippet'),
                    "domain": urlparse(result.get('link')).netloc
                })
            except:
                continue
                
        return {
            "total_results": data.get('searchInformation', {}).get('totalResults', 0),
            "top_competitors": competitors,
            "analysis_summary": self._analyze_patterns(competitors)
        }
        
    def _analyze_patterns(self, competitors: List[Dict]) -> Dict[str, Any]:
        """Analyze common patterns in top ranking titles."""
        return {
             "avg_title_length": int(sum(len(c['title']) for c in competitors) / len(competitors)) if competitors else 0,
             "common_domains": [c['domain'] for c in competitors[:3]]
        }

competitor_service = CompetitorService()
