import urllib.robotparser
from urllib.parse import urlparse

class RobotsChecker:
    def __init__(self):
        self.cache = {}
    
    async def can_fetch(self, url: str, user_agent: str = "RankForgeBot") -> bool:
        """Check if we're allowed to crawl this URL"""
        
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        # Check cache
        if robots_url in self.cache:
            rp = self.cache[robots_url]
        else:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots_url)
            try:
                rp.read()
                self.cache[robots_url] = rp
            except:
                # If no robots.txt, allow
                return True
        
        return rp.can_fetch(user_agent, url)

# Singleton instance
robots_checker = RobotsChecker()
