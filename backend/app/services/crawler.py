import asyncio
import json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import httpx
from app.models.analysis import AnalysisResult
from fastapi import HTTPException
import urllib.robotparser

class RobotsChecker:
    def __init__(self):
        self.cache = {}
    
    async def can_fetch(self, url: str, user_agent: str = "RankForgeBot") -> bool:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        if robots_url in self.cache:
            rp = self.cache[robots_url]
        else:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots_url)
            try:
                rp.read()
                self.cache[robots_url] = rp
            except:
                return True
        
        return rp.can_fetch(user_agent, url)

robots_checker = RobotsChecker()

class AdvancedCrawler:
    def __init__(self):
        self.playwright = None
        self.browser = None
    
    async def initialize(self):
        """Ensure the browser engine is active with optimized enterprise flags."""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-gpu',
                    '--disable-dev-shm-usage',
                    '--single-process' # Save memory for 1000s of users
                ]
            )
    
    async def create_isolated_context(self):
        """Creates a fresh, isolated browsing environment for a specific scan."""
        await self.initialize()
        return await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True
        )
    
    async def _extract_sitemap(self, url: str) -> bool:
        """Check for sitemap.xml in common locations"""
        parsed = urlparse(url)
        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.head(sitemap_url)
                return response.status_code == 200
        except:
            return False

    async def crawl_page(self, url: str) -> dict:
        if not await robots_checker.can_fetch(url):
            raise HTTPException(status_code=403, detail="Crawling blocked by robots.txt")
        
        # Scale Optimized: Use fresh context per request
        context = await self.create_isolated_context()
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2) # Wait for dynamic content
            
            # Check for sitemap (Critical Enterprise Signal)
            has_sitemap = await self._extract_sitemap(url)
            
            html = await page.content()

            metrics = await page.evaluate("""
                () => {
                    const timing = performance.timing;
                    return {
                        loadTime: timing.loadEventEnd - timing.navigationStart,
                        domReady: timing.domContentLoadedEventEnd - timing.navigationStart,
                        firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0
                    };
                }
            """)
            
            soup = BeautifulSoup(html, 'html.parser')
            
            page_text = soup.get_text()
            
            data = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'meta_description': self._get_meta(soup, 'description'),
                'meta_keywords': self._get_meta(soup, 'keywords'),
                'canonical': self._get_canonical(soup),
                'hreflang': self._get_hreflang(soup),
                'og_data': self._get_og_data(soup),
                'h1': [h.get_text().strip() for h in soup.find_all('h1')],
                'h2': [h.get_text().strip() for h in soup.find_all('h2')],
                'h3': [h.get_text().strip() for h in soup.find_all('h3')],
                'body_text': page_text,
                'text': page_text,
                'word_count': len(page_text.split()),
                'images': self._analyze_images(soup),
                'links': self._analyze_links(soup, url),
                'schema': self._extract_schemas(soup),
                'performance': metrics,
                'has_sitemap': has_sitemap,
                'html': html
            }

            return data
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                detailed_fix = "Target site is slow or uses anti-bot shielding. SOLUTION: Run again or use 'Stealth Mode' proxy."
            elif "403" in error_msg or "access denied" in error_msg.lower():
                detailed_fix = "Site is protected by Cloudflare or WAF. SOLUTION: Verify URL or contact support for Pro Scraper."
            else:
                detailed_fix = f"Unexpected crawl failure: {error_msg}. SOLUTION: Ensure the URL is public and accessible."
            
            print(f"Crawl Error: {e}")
            raise HTTPException(status_code=500, detail=detailed_fix)
        finally:
            await page.close()
            await context.close()

    def _get_meta(self, soup, name):
        meta = soup.find('meta', attrs={'name': name}) or \
               soup.find('meta', attrs={'property': name}) or \
               soup.find('meta', attrs={'property': f'og:{name}'})
        return meta.get('content', '') if meta else ''

    def _get_canonical(self, soup):
        link = soup.find('link', rel='canonical')
        return link.get('href', '') if link else ''

    def _get_hreflang(self, soup):
        links = soup.find_all('link', rel='alternate', hreflang=True)
        return {l.get('hreflang'): l.get('href') for l in links}

    def _get_og_data(self, soup):
        data = {}
        for meta in soup.find_all('meta', property=True):
            prop = meta.get('property')
            if prop.startswith('og:') or prop.startswith('twitter:'):
                data[prop] = meta.get('content', '')
        return data

    def _analyze_images(self, soup):
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'has_alt': bool(img.get('alt'))
            })
        return {
            'total': len(images),
            'without_alt': len([i for i in images if not i['has_alt']]),
            'details': images[:10]
        }

    def _extract_schemas(self, soup) -> list:
        """Extract all JSON-LD schemas from the page"""
        schemas = []
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                content = script.string
                if content:
                    parsed = json.loads(content)
                    # Handle @graph structure
                    if isinstance(parsed, dict) and '@graph' in parsed:
                        schemas.extend(parsed['@graph'])
                    elif isinstance(parsed, list):
                        schemas.extend(parsed)
                    else:
                        schemas.append(parsed)
            except json.JSONDecodeError:
                continue  # Skip malformed JSON-LD
        return schemas

    def _analyze_links(self, soup, base_url):
        internal = []
        external = []
        domain = urlparse(base_url).netloc
        
        for link in soup.find_all('a', href=True):
            href = urljoin(base_url, link['href'])
            if urlparse(href).netloc == domain:
                internal.append(href)
            else:
                external.append(href)
                
        return {
            'internal_count': len(internal),
            'external_count': len(external),
            'internal': internal[:20],
            'external': external[:20]
        }
    
    async def cleanup(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

crawler = AdvancedCrawler()
