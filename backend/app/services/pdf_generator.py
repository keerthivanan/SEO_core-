from playwright.async_api import async_playwright
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '../templates')
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class PDFGenerator:
    async def generate_report(self, analysis_data: dict) -> bytes:
        """
        Generates a professionally styled PDF report using Playwright.
        """
        # 1. Render HTML with Jinja2
        template = env.get_template('report.html')
        
        # Format data for template
        context = {
            'analysis': analysis_data,
            'semantic_score': analysis_data.get('semantic_score', 0),
            'date': datetime.now().strftime("%B %d, %Y")
        }
        
        html_content = template.render(context)
        
        # 2. Convert to PDF using Playwright (Headless Chrome)
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set content
            await page.set_content(html_content, wait_until='networkidle')
            
            # Generate PDF
            pdf_bytes = await page.pdf(
                format='A4',
                print_background=True,
                margin={'top': '0px', 'right': '0px', 'bottom': '0px', 'left': '0px'}
            )
            
            await browser.close()
            return pdf_bytes
