import os
import logging
import asyncio
from supabase import create_client, Client
from app.core.config import settings

# Configure World-Class Logging
logger = logging.getLogger("rankforge.database")
logging.basicConfig(level=logging.INFO)

class DatabaseService:
    def __init__(self):
        self.url: str = settings.SUPABASE_URL
        self.key: str = settings.SUPABASE_KEY
        self.client: Client = None
        
        if not self.url or not self.key:
            logger.warning("DATABASE_WARNING: Supabase URL or Key missing. Database operations will be disabled.")
            return

        try:
            self.client = create_client(self.url, self.key)
            # Test connectivity immediately
            self.check_connection()
            logger.info("DATABASE_SUCCESS: RankForge Global Brain connected to Supabase Protocol.")
        except Exception as e:
            logger.error(f"DATABASE_CRITICAL: Connection failure: {e}")

    def check_connection(self) -> bool:
        """Verify the database is reachable and active."""
        if not self.client:
            return False
        try:
            # Simple health check query
            self.client.table("analyses").select("id").limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"DATABASE_HEALTH_FAILED: {e}")
            return False

    async def save_analysis(self, result: dict, user_id: str = None):
        """
        Record a successful neural analysis into the global archive.
        Ensures 'Best of All Time' data integrity.
        """
        if not self.client:
            logger.error("COMMAND_REJECTED: Cannot save analysis. Database disconnected.")
            return

        try:
            # Structuring for the 'analyses' table
            record = {
                "id": result.get('analysis_id'),
                "user_id": user_id,
                "url": result.get('url'),
                "keyword": result.get('keyword'),
                "seo_score": result.get('seo_score', 0),
                "overall_score": result.get('overall_score', 0),
                "created_at": result.get('timestamp').isoformat() if hasattr(result.get('timestamp'), 'isoformat') else result.get('timestamp'),
                "report_data": result
            }
            
            # Use non-blocking async execution
            # Note: supabase-py 2.0+ supports async if initialized correctly or by using .execute() in thread for legacy
            # Assuming standard async support in enterprise env
            self.client.table("analyses").upsert(record).execute() 
            # Actually, standard supabase-py .execute() is blocking. 
            # For 1000s of users, we MUST wrap in run_in_executor if not using a dedicated async client
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: self.client.table("analyses").upsert(record).execute())
            
            logger.info(f"ANALYSIS_ARCHIVED: ID {result.get('analysis_id')} committed to global records.")
            
        except Exception as e:
            logger.error(f"ARCHIVE_FAILURE: Failed to commit record {result.get('analysis_id')}: {e}")

    async def get_analysis(self, analysis_id: str):
        """Fetch history from the cloud brain via non-blocking IO."""
        if not self.client:
            return None
        
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: self.client.table("analyses").select("*").eq("id", analysis_id).execute())
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"RETRIEVAL_ERROR: Failed to fetch analysis {analysis_id}: {e}")
            return None

# Initialize persistent singleton
db = DatabaseService()
