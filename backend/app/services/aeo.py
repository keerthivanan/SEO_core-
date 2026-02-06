import os
import json
import logging

# Configure logging for error visibility
logger = logging.getLogger(__name__)

# Graceful import of OpenAI
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI = None

class AEOAnalyzer:
    def __init__(self):
        self.openai_client = None
        api_key = os.getenv('OPENAI_API_KEY')
        if OPENAI_AVAILABLE and api_key:
            try:
                self.openai_client = AsyncOpenAI(api_key=api_key)
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI client: {e}")
    
    async def analyze_aeo(self, page_data: dict, keyword: str, serp_data: dict) -> dict:
        """Complete Answer Engine Optimization analysis"""
        
        aeo_score = 0
        
        # 1. Check for featured snippet opportunity
        snippet_analysis = await self._check_featured_snippet(keyword, serp_data)
        
        # 2. Analyze PAA (People Also Ask) optimization
        paa_analysis = await self._analyze_paa_optimization(page_data, keyword)
        
        # 3. Check FAQ schema
        faq_analysis = await self._check_faq_schema(page_data)
        
        # 4. Analyze answer formatting
        format_analysis = await self._check_answer_formatting(page_data, keyword)
        
        # 5. Check structured data completeness
        schema_analysis = await self._analyze_schema_completeness(page_data)
        
        # Calculate AEO score
        aeo_score = (
            snippet_analysis['score'] * 0.30 +
            paa_analysis['score'] * 0.25 +
            faq_analysis['score'] * 0.20 +
            format_analysis['score'] * 0.15 +
            schema_analysis['score'] * 0.10
        )
        
        return {
            'aeo_score': int(aeo_score),
            'featured_snippet': snippet_analysis,
            'paa_optimization': paa_analysis,
            'faq_schema': faq_analysis,
            'answer_formatting': format_analysis,
            'schema_completeness': schema_analysis,
            'recommendations': await self._generate_aeo_recommendations(
                snippet_analysis,
                paa_analysis,
                faq_analysis,
                format_analysis,
                keyword
            )
        }
    
    async def _check_featured_snippet(self, keyword: str, serp_data: dict) -> dict:
        """Check if featured snippet exists and if we can win it"""
        
        has_snippet = False
        snippet_type = None
        current_snippet_url = None
        
        # Handle case where serp_data might be None or missing keys
        if not serp_data:
            return {'score': 0, 'has_snippet': False, 'opportunity': False}

        for result in serp_data.get('organic', []):
            if result.get('snippet_highlighted_words'):
                has_snippet = True
                snippet_type = 'paragraph'
                current_snippet_url = result.get('link')
                break
        
        # Check for other snippet types
        if serp_data.get('answerBox'):
            has_snippet = True
            snippet_type = serp_data['answerBox'].get('snippetType', 'paragraph')
        
        return {
            'score': 0 if not has_snippet else 50,  # Opportunity exists
            'has_snippet': has_snippet,
            'snippet_type': snippet_type,
            'current_holder': current_snippet_url,
            'opportunity': has_snippet,  # If snippet exists, we can try to win it
            'difficulty': 'medium' if has_snippet else 'low'
        }
    
    async def _analyze_paa_optimization(self, page_data: dict, keyword: str) -> dict:
        """Analyze People Also Ask optimization with IMPROVED matching logic"""
        
        # Get PAA questions from AI
        prompt = f"""
        For the keyword "{keyword}", list the top 10 "People Also Ask" questions 
        that commonly appear in Google search results.
        
        Return as JSON array: {{"questions": ["question 1", "question 2", ...]}}
        """
        
        paa_questions = []
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an SEO expert."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            paa_questions = json.loads(response.choices[0].message.content).get('questions', [])
        except Exception as e:
            logger.error(f"AEO PAA Analysis AI failed: {e}. Falling back to heuristic mode.")
            # Deterministic fallback based on keyword modifiers
            paa_questions = [
                f"How to optimize for {keyword}?",
                f"What is {keyword}?",
                f"Is {keyword} effective for SEO?",
                f"Best practices for {keyword}"
            ]

        
        # IMPROVED MATCHING: Require 60% of significant words to match
        text_content = page_data.get('text', '') or page_data.get('body_text', '')
        page_text_lower = text_content.lower()
        answered_count = 0
        
        stop_words = {'what', 'is', 'the', 'a', 'an', 'how', 'do', 'does', 'why', 'when', 'where', 'can', 'i', 'you', 'to', 'for', 'of', 'in', 'on', 'it'}
        
        for question in paa_questions:
            # Extract significant words (remove stop words)
            question_words = [w.lower().strip('?.,') for w in question.split() if w.lower().strip('?.,') not in stop_words]
            
            if not question_words:
                continue
            
            # Count how many significant words appear in content
            matches = sum(1 for word in question_words if word in page_text_lower)
            match_ratio = matches / len(question_words)
            
            # Require 60% match for "answered"
            if match_ratio >= 0.6:
                answered_count += 1
        
        coverage = (answered_count / len(paa_questions)) * 100 if paa_questions else 0
        
        return {
            'score': int(coverage),
            'total_paa_questions': len(paa_questions),
            'answered_on_page': answered_count,
            'coverage_percentage': coverage,
            'paa_questions': paa_questions,
            'missing_questions': [q for q in paa_questions if not self._question_is_answered(q, page_text_lower, stop_words)]
        }
    
    def _question_is_answered(self, question: str, page_text: str, stop_words: set) -> bool:
        """Helper to check if a question is answered on the page"""
        question_words = [w.lower().strip('?.,') for w in question.split() if w.lower().strip('?.,') not in stop_words]
        if not question_words:
            return False
        matches = sum(1 for word in question_words if word in page_text)
        return (matches / len(question_words)) >= 0.6
    
    async def _check_faq_schema(self, page_data: dict) -> dict:
        """Check for FAQ schema markup"""
        schemas = page_data.get('schema', [])
        
        has_faq_schema = False
        if isinstance(schemas, list):
            has_faq_schema = any(
                isinstance(s, dict) and s.get('@type') == 'FAQPage' 
                for s in schemas
            )
        
        score = 0
        question_count = 0

        if has_faq_schema:
            try:
                faq_schema = next(s for s in schemas if isinstance(s, dict) and s.get('@type') == 'FAQPage')
                question_count = len(faq_schema.get('mainEntity', []))
                score = min(100, question_count * 10)  # 10 points per question, max 100
            except:
                pass
        
        return {
            'score': score,
            'has_faq_schema': has_faq_schema,
            'question_count': question_count,
            'schema_valid': has_faq_schema
        }
    
    async def _check_answer_formatting(self, page_data: dict, keyword: str) -> dict:
        """Check if answers are formatted for snippets"""
        
        score = 0
        
        has_direct_answers = False
        has_lists = False
        has_tables = False
        
        # Check H2/H3 for questions
        all_headers = page_data.get('h2', []) + page_data.get('h3', [])
        question_headers = [h for h in all_headers if '?' in h or h.lower().startswith(('what', 'how', 'why', 'when', 'where'))]
        
        if question_headers:
            has_direct_answers = True
            score += 40
        
        text_content = page_data.get('text', '') or page_data.get('body_text', '')
        html_content = page_data.get('html', '')

        # Check for lists (numbered or bulleted)
        if '1.' in text_content or '•' in text_content or '<ol' in html_content:
            has_lists = True
            score += 30
        
        # Check for tables
        if '<table' in html_content:
            has_tables = True
            score += 30
        
        return {
            'score': score,
            'has_question_headers': len(question_headers),
            'has_direct_answers': has_direct_answers,
            'has_lists': has_lists,
            'has_tables': has_tables,
            'question_headers': question_headers[:5]  # First 5
        }
    
    async def _analyze_schema_completeness(self, page_data: dict) -> dict:
        """Analyze completeness of structured data"""
        
        schemas = page_data.get('schema', [])
        if not isinstance(schemas, list): schemas = []

        # Essential schema types for AEO
        essential_types = ['Article', 'FAQPage', 'HowTo', 'Product', 'Organization']
        
        present_types = []
        for s in schemas:
            if isinstance(s, dict):
                t = s.get('@type')
                if t: present_types.append(t)

        missing_types = [t for t in essential_types if t not in present_types]
        
        completeness = 0
        if present_types:
            completeness = (len(set(present_types).intersection(essential_types)) / len(essential_types)) * 100
            if completeness == 0 and present_types: completeness = 20  # At least some schema


        return {
            'score': int(completeness),
            'total_schemas': len(schemas),
            'schema_types': present_types,
            'missing_essential': missing_types,
            'completeness': completeness
        }
    
    async def _generate_aeo_recommendations(
        self, 
        snippet_analysis: dict,
        paa_analysis: dict,
        faq_analysis: dict,
        format_analysis: dict,
        keyword: str
    ) -> dict:
        """Generate AI-powered AEO recommendations"""
        
        prompt = f"""
        Generate featured snippet-optimized content for the keyword: "{keyword}"
        
        Current status:
        - Featured snippet exists: {snippet_analysis['has_snippet']}
        - PAA coverage: {paa_analysis['coverage_percentage']:.0f}%
        - FAQ schema: {faq_analysis['has_faq_schema']}
        
        Generate in JSON format:
        {{
          "snippet_optimized_answer": "40-60 word direct answer to '{keyword}'",
          "faq_schema": {{
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
              {{
                "@type": "Question",
                "name": "Question 1?",
                "acceptedAnswer": {{
                  "@type": "Answer",
                  "text": "40-60 word answer"
                }}
              }}
            ]
          }},
          "content_structure": [
            "H2: What is [keyword]?",
            "Direct answer (40-60 words)",
            "H2: How does [keyword] work?",
            "Numbered list (5-7 steps)",
            "H2: Frequently Asked Questions",
            "10 Q&A pairs"
          ]
        }}
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert in Answer Engine Optimization."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"AEO Recommendation generation failed: {e}")
            return {"error": str(e), "failed": True}

aeo_analyzer = AEOAnalyzer()
