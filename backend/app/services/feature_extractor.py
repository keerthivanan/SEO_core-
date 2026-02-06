import numpy as np

class FeatureExtractor:
    """
    The 'Sensory System' of RankForge.
    Vectorizes signals from SEO, AEO, GEO, and Semantic engines.
    Creates a 150-dimensional feature vector for the Neural Brain.
    """
    
    def extract_vector(self, seo: dict, aeo: dict, geo: dict, semantic: dict, page_data: dict) -> np.ndarray:
        """
        Fused feature extraction.
        Links categorical Semantic logic with technical SEO metrics.
        """
        features = []
        
        # 1. Foundation SEO (1-20)
        features.append(seo.get('total_score', 0) / 100)
        FEATURES_MAP = {
            'title': breakdown.get('title', 0),
            'content': breakdown.get('content', 0),
            'performance': breakdown.get('performance', 0),
            'technical': breakdown.get('tech_integrity', 0) or breakdown.get('technical', 0)
        }
        features.append(FEATURES_MAP['title'] / 100)
        features.append(FEATURES_MAP['content'] / 100)
        features.append(FEATURES_MAP['performance'] / 100)
        features.append(FEATURES_MAP['technical'] / 100)

        
        # 2. AEO Signals (21-40)
        features.append(aeo.get('aeo_score', 0) / 100)
        features.append(1.0 if aeo.get('featured_snippet', {}).get('has_snippet') else 0.0)
        features.append(aeo.get('paa_optimization', {}).get('coverage_percentage', 0) / 100)
        features.append(1.0 if aeo.get('faq_schema', {}).get('has_faq_schema') else 0.0)
        
        # 3. GEO Signals (41-60)
        features.append(geo.get('geo_score', 0) / 100)
        features.append(geo.get('eeat_signals', {}).get('score', 0) / 100)
        features.append(1.0 if geo.get('citation_worthiness', {}).get('citation_worthy') else 0.0)
        features.append(geo.get('ai_formatting', {}).get('score', 0) / 100)
        
        # 4. THE LINK: Semantic Logic Signals (61-80)
        # This is where the 'Logic' is linked.
        features.append(semantic.get('logic_score', 0) / 100)
        intent_match = 1.0 if semantic.get('intent_analysis', {}).get('match') else 0.0
        features.append(intent_match)
        
        # Encode Intent Types (Informational vs Transactional)
        intent_type = semantic.get('intent_analysis', {}).get('query_intent', '').lower()
        features.append(1.0 if 'transactional' in intent_type else 0.0)
        features.append(1.0 if 'informational' in intent_type else 0.0)
        
        features.append(len(semantic.get('entity_gaps', [])) / 10) # Logically missing entities

        # 5. Page Level Raw Stats (81-100)
        word_count = page_data.get('word_count') or 0
        features.append(min(word_count / 5000, 1.0))
        
        h2_tags = page_data.get('h2') or []
        features.append(len(h2_tags) / 20)
        
        images = page_data.get('images') or {}
        image_count = images.get('total', 0) if isinstance(images, dict) else 0
        features.append(image_count / 50)

        # Pad to 150 features with zeros if necessary (reserved for future DL growth)
        while len(features) < 150:
            features.append(0.0)
            
        return np.array(features[:150], dtype=np.float32)

feature_extractor = FeatureExtractor()
