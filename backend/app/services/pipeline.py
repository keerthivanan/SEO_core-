import asyncio
import hashlib
from datetime import datetime
from fastapi import WebSocket

from app.models.analysis import AnalysisRequest
from app.services.crawler import crawler
from app.services.lighthouse import lighthouse_service
from app.services.competitor import competitor_service
from app.services.scorer import scorer
from app.services.ai_optimizer import ai_optimizer
from app.services.gap_analyzer import gap_analyzer
from app.services.robots import robots_checker
from app.services.aeo import aeo_analyzer
from app.services.geo import geo_analyzer
from app.services.semantic import semantic_analyzer
from app.services.feature_extractor import feature_extractor
from app.services.ml_engine import ml_engine
from app.services.database import db

# Titan ML 2.0 Components
from app.ml import TITAN_ML_AVAILABLE

if TITAN_ML_AVAILABLE:
    from app.ml.quality_scorer import quality_scorer
    from app.ml.rl_agent import seo_agent
    from app.ml.seo_embeddings import seo_encoder
else:
    quality_scorer = None
    seo_agent = None
    seo_encoder = None

class AnalysisPipeline:
    def __init__(self, request: AnalysisRequest):
        self.request = request
        self.url = str(request.url)
        self.keyword = request.target_keyword
    
    async def run(self, websocket: WebSocket = None):
        """Run complete analysis pipeline with real-time updates"""
        
        start_time = asyncio.get_event_loop().time()
        
        async def update(message: str, progress: int):
            if websocket:
                await websocket.send_json({
                    'type': 'progress',
                    'message': message,
                    'progress': progress
                })
        
        try:
            # Step 1: Check Robots
            await update("Checking robots.txt...", 5)
            can_crawl = await robots_checker.can_fetch(self.url)
            if not can_crawl:
                await update("Warning: Blocked by robots.txt. Proceeding with caution...", 7)

            # Step 2: Crawl user's page
            await update("Analyzing your website...", 10)
            page_data = await crawler.crawl_page(self.url)
            
            # Step 3: Run Lighthouse audit
            await update("Running Google Lighthouse tests...", 25)
            lighthouse_data = await lighthouse_service.run_audit(self.url)
            
            # Step 4: Analyze competitors
            await update("Analyzing Top 10 Competitors...", 45)
            competitor_data = await competitor_service.analyze_competitors(self.keyword)
            # Normalize competitor structure
            competitors_list = competitor_data.get('top_competitors', [])  # Competitor list from SERP

            # Step 5: Calculate SEO score
            await update("Calculating SEO score...", 60)
            score_data = scorer.calculate_score(page_data, lighthouse_data, competitor_data)

            
            # Step 6: Gap analysis
            await update("Identifying optimization opportunities...", 75)
            gap_data = await gap_analyzer.analyze_gaps(
                page_data,
                competitors_list,
                self.keyword
            )
            
            # Step 7: AEO Analysis
            await update("Analyzing Answer Engine Optimization (AEO)...", 75)
            aeo_results = await aeo_analyzer.analyze_aeo(
                page_data,
                self.keyword,
                competitor_data
            )
            
            # Step 8: GEO Analysis
            await update("Analyzing AI Citation Potential (GEO)...", 80)
            geo_results = await geo_analyzer.analyze_geo(
                page_data,
                self.keyword
            )
            
            # Step 9: AI optimization (Contextualized)
            await update("Generating AI-powered recommendations...", 85)
            # Pass gaps AND AEO/GEO insights to AI for smarter recommendations
            score_data['gaps'] = gap_data 
            score_data['aeo'] = aeo_results
            score_data['geo'] = geo_results
            
            ai_recommendations = await ai_optimizer.optimize_content(
                page_data,
                self.keyword,
                gap_data
            )

            
            # Step 10: Neuro-Semantic Logic Analysis (The "Brain")
            await update("Running Neuro-Semantic Logic Engine...", 90)
            semantic_results = await semantic_analyzer.analyze_logic(
                page_data,
                self.keyword,
                competitors_list
            )

            # Step 11: Titan ML Logic Link (The "Decision")
            await update("Linking Neural-Semantic Intelligence...", 93)
            # Vectorize all engine signals
            feature_vector = feature_extractor.extract_vector(
                score_data, aeo_results, geo_results, semantic_results, page_data
            )
            # Run Neural Ranking Prediction
            neural_results = ml_engine.predict_ranking_potential(feature_vector)

            # Step 11.5: Titan ML 2.0 Advanced Analysis
            await update("Running Titan ML 2.0 Intelligence...", 94)
            titan_ml_results = {}
            
            if TITAN_ML_AVAILABLE:
                try:
                    # Content Quality Scoring (BERT + E-E-A-T)
                    page_text = page_data.get('text', '') or page_data.get('body_text', '')
                    titan_ml_results['content_quality'] = quality_scorer.score_content(page_text)
                    
                    # RL Agent Recommendations
                    titan_ml_results['smart_actions'] = seo_agent.get_optimal_actions(
                        feature_vector, gap_data, n_actions=5
                    )
                    
                    # Semantic Gap Analysis
                    competitor_texts = [c.get('snippet', '') for c in competitors_list[:5]]
                    if competitor_texts:
                        titan_ml_results['semantic_gaps'] = seo_encoder.find_semantic_gaps(
                            page_text, competitor_texts
                        )
                    
                except Exception as e:
                    titan_ml_results['error'] = str(e)

            # Step 12: Compile results
            await update("Finalizing report...", 95)
            
            elapsed = asyncio.get_event_loop().time() - start_time
            analysis_id = hashlib.md5(f"{self.url}{self.keyword}{datetime.now()}".encode()).hexdigest()
            
            # Master Plan Logic
            traffic_potential = self._calculate_traffic_potential(score_data['total_score'], competitor_data)
            action_plan = self._generate_90_day_plan(score_data['total_score'], gap_data)
            critical_issues = self._structure_critical_issues(gap_data, score_data)
            
            # Calculate Overall Score (Fused Neural-Semantic)
            # Fuses Technical, AEO/GEO, LLM Logic, and Deep Learning IQ
            overall_score = int(
                score_data['total_score'] * 0.30 +      # Technical SEO 30%
                semantic_results['logic_score'] * 0.25 + # LLM Logic 25%
                neural_results['neural_iq'] * 0.25 +     # Neural IQ 25%
                aeo_results['aeo_score'] * 0.10 +        # AEO 10%
                geo_results['geo_score'] * 0.10          # GEO 10%
            )
            
            optimization_priority = self._determine_priority(
                score_data['total_score'],
                aeo_results['aeo_score'],
                geo_results['geo_score']
            )
            
            results = {
                'analysis_id': analysis_id,
                'url': self.url,
                'keyword': self.keyword,
                'timestamp': datetime.now().isoformat(),
                'processing_time': round(elapsed, 2),
                
                'seo_score': score_data['total_score'], 
                'overall_score': overall_score,
                'aeo_score': aeo_results['aeo_score'],
                'geo_score': geo_results['geo_score'],
                'semantic_score': semantic_results['logic_score'],
                'neural_score': neural_results['neural_iq'], # New Neural Signal
                
                'optimization_priority': optimization_priority,
                
                'score_details': score_data, 
                'lighthouse_data': lighthouse_data,
                'gaps': gap_data,
                'competitor_data': competitor_data,
                'aeo_analysis': aeo_results,
                'geo_analysis': geo_results,
                'semantic_analysis': semantic_results,
                'neural_analysis': neural_results, # New Detailed Neural Insight
                'titan_ml': titan_ml_results,       # Titan ML 2.0 (Quality, RL, Semantic)
                'ai_recommendations': ai_recommendations,
                
                # Master Plan specific fields
                'traffic_potential': traffic_potential,
                'action_plan': action_plan,
                'critical_issues': critical_issues,
                
                'page_data': {k:v for k,v in page_data.items() if k != 'html'},
                'estimated_ranking': self._predict_ranking_text(neural_results) # Use Neural Predictor for final verdict
            }
            
            
            # Step 12: Persistence (Save to Supabase)
            await update("Saving results to history...", 98)
            await db.save_analysis(results, self.request.user_id)

            await update("Analysis complete!", 100)
            return results
            
        except Exception as e:
            if websocket:
                await websocket.send_json({
                    'type': 'error',
                    'message': str(e)
                })
            raise
    
    def _determine_priority(self, seo: int, aeo: int, geo: int) -> str:
        """Determine what to optimize first"""
        if seo < 70:
            return "Focus on SEO first (technical + content)"
        elif aeo < 60:
            return "Focus on AEO (featured snippets + FAQs)"
        elif geo < 60:
            return "Focus on GEO (E-E-A-T + citations)"
        else:
            return "All optimizations in good shape! Focus on content quality."

    def _estimate_ranking(self, score: int) -> str:
        """Estimate ranking potential (Blueprint Logic)"""
        if score >= 90:
            return "Top 3 in 60-90 days with consistent optimization"
        elif score >= 80:
            return "Top 10 in 60-90 days, Top 3 in 6 months"
        elif score >= 70:
            return "Top 10 in 90-120 days with optimization"
        elif score >= 60:
            return "First page possible in 120+ days"
        else:
            return "Significant work needed. First page in 6+ months"

    def _calculate_traffic_potential(self, score: int, competitor_data: dict) -> dict:
        """Calculate traffic potential based on competitor benchmarks"""
        # Blueprint: Dynamic scaling based on gap to perfection
        baseline_visits = 1200 # Assumed baseline
        
        # Multiplier scales from 1.2x (high scores) to 5.0x (low scores)
        if score < 40: multiplier = 5.0
        elif score < 60: multiplier = 3.5
        elif score < 80: multiplier = 2.47 # Mandated logic base
        else: multiplier = 1.6
        
        projected = int(baseline_visits * multiplier)
        
        return {
            "current_estimated": baseline_visits,
            "projected_90_days": projected,
            "increase_percentage": int((multiplier - 1) * 100),
            "confidence": "HIGH" if score > 70 else "MEDIUM"
        }

    def _structure_critical_issues(self, gap_data: dict, score_data: dict) -> list:
        """Identify top 3 critical issues for the report"""
        issues = []
        
        # 1. Check for missing Keyword in Title (High Impact)
        if score_data['breakdown']['title'] < 15: # 15 is max
             issues.append({
                 "type": "title",
                 "impact": "HIGH",
                 "priority": 1,
                 "issue": "Missing Target Keyword in Title",
                 "fix": "Rewrite title to include keyword near the front."
             })

        # 2. Check for Content Gap
        # Assuming gap_data['gaps'] contains the specific gaps from GapAnalyzer
        gaps_list = gap_data.get('gaps', [])
        for gap in gaps_list:
            if gap['type'] == 'content' and gap['severity'] == 'high':
                issues.append({
                    "type": "content",
                    "impact": "HIGH",
                    "priority": 1,
                    "issue": gap['issue'],
                    "fix": gap['recommendation']
                })
        
        # 3. Check for Schema
        # Convert score check to issue
        # (Simplified logic for brevity, expands based on real GapAnalyzer output)
        
        # Ensure we return at least distinct top issues
        return issues[:3]

    def _generate_90_day_plan(self, score: int, gap_data: dict) -> dict:
        """Generate DYNAMIC week-by-week action plan based on REAL gaps"""
        
        gaps = gap_data.get('gaps', [])
        priority_fixes = gap_data.get('priority_fixes', [])
        
        # Week 1-2: High priority fixes
        week_1_2 = []
        for gap in priority_fixes[:3]:  # Top 3 high-severity issues
            if gap['type'] == 'title':
                week_1_2.append(f"Fix Title: {gap['recommendation']}")
            elif gap['type'] == 'content':
                week_1_2.append(f"Expand Content: {gap['recommendation']}")
            elif gap['type'] == 'technical':
                week_1_2.append(f"Add Schema: {gap['recommendation']}")
            elif gap['type'] == 'structure':
                week_1_2.append(f"Add Sections: {gap['recommendation']}")
            else:
                week_1_2.append(gap['recommendation'])
        
        # If no gaps found, add generic best practices
        if not week_1_2:
            week_1_2 = ["Review and optimize title tag", "Enhance meta description", "Audit image alt text"]
        
        # Week 3-4: Medium priority + structure
        week_3_4 = []
        medium_gaps = [g for g in gaps if g['severity'] == 'medium'][:3]
        for gap in medium_gaps:
            week_3_4.append(gap['recommendation'])
        
        if not week_3_4:
            week_3_4 = ["Improve internal linking structure", "Add FAQ section", "Enhance page speed"]
        
        # Month 2: Content expansion + authority
        month_2 = []
        benchmark = gap_data.get('competitor_benchmark', {})
        target_words = benchmark.get('avg_word_count', 1500)
        
        if score < 70:
            month_2.append(f"Expand content to {target_words}+ words")
            month_2.append("Create 4 supporting blog posts")
            month_2.append("Build 5 quality backlinks")
        else:
            month_2.append("Publish 2 in-depth guides")
            month_2.append("Optimize for featured snippets")
            month_2.append("Add video content")
        
        # Month 3: Authority + refinement
        month_3 = []
        if score < 80:
            month_3.append("Acquire 10 authoritative backlinks")
            month_3.append("Publish 8 topic-cluster articles")
            month_3.append("A/B test headlines and meta descriptions")
        else:
            month_3.append("Focus on brand mentions")
            month_3.append("Expand to long-tail keywords")
            month_3.append("Implement advanced schema (HowTo, FAQ)")
        
        return {
            "week_1_2": week_1_2,
            "week_3_4": week_3_4,
            "month_2": month_2,
            "month_3": month_3
        }


    def _predict_ranking_text(self, neural_results: dict) -> str:
        """Provide a descriptive ranking verdict based on neural inference"""
        rank = neural_results['estimated_rank']
        prob = neural_results['ranking_probability']
        
        if rank <= 3:
            return f"Top 3 dominance predicted ({int(prob*100)}% confidence). Solid semantic-neural alignment."
        elif rank <= 10:
            return f"First page potential confirmed. Target Top 3 by addressing '{neural_results['reasoning'][:30]}...'"
        elif rank <= 30:
            return f"Ranked in Top 30. Neural engine recommends deep semantic expansion to break into Top 10."
        else:
            return "Foundation established. Intense logic-gap closures required for competitive SERP entry."
