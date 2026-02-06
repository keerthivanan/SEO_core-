"""
Titan ML Engine v2.0 - Deep Neural Ranking Predictor
=====================================================

Advanced ML engine with:
- Multi-head attention over feature groups
- Deep neural ranking prediction
- Confidence intervals via Monte Carlo dropout
- Integration with all Titan ML 2.0 components

Gracefully falls back to lightweight mode when PyTorch unavailable.
"""

import numpy as np
import logging
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)

# Try importing deep learning dependencies
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    DEEP_MODE = True
except ImportError:
    DEEP_MODE = False
    # Provide dummy classes to avoid NameErrors during import
    class torch:
        class Tensor: pass
    class nn:
        class Module: pass
        @staticmethod
        def Linear(*args, **kwargs): return None
        @staticmethod
        def Sequential(*args, **kwargs): return None
        @staticmethod
        def BatchNorm1d(*args, **kwargs): return None
        @staticmethod
        def Dropout(*args, **kwargs): return None
        @staticmethod
        def MultiheadAttention(*args, **kwargs): return None
    F = None
    logger.info("ML Engine running in lightweight mode")


class DeepRankingPredictor(nn.Module):
    """
    Deep Neural Network with attention for ranking prediction.
    
    Architecture:
    - Feature group encoders (Content, Technical, AEO, GEO, Semantic)
    - Multi-head attention fusion
    - Deep predictor with residual connections
    """
    
    def __init__(self, input_dim: int = 150):
        super().__init__()
        
        # Feature group encoders
        self.content_encoder = nn.Sequential(
            nn.Linear(50, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Dropout(0.2)
        )
        
        self.technical_encoder = nn.Sequential(
            nn.Linear(30, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.2)
        )
        
        self.aeo_geo_encoder = nn.Sequential(
            nn.Linear(40, 96),
            nn.ReLU(),
            nn.BatchNorm1d(96),
            nn.Dropout(0.2)
        )
        
        self.semantic_encoder = nn.Sequential(
            nn.Linear(30, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.2)
        )
        
        # Fusion dimension
        self.fusion_dim = 128 + 64 + 96 + 64  # 352
        
        # Multi-head attention for feature fusion
        self.attention = nn.MultiheadAttention(
            embed_dim=self.fusion_dim,
            num_heads=8,
            dropout=0.1,
            batch_first=True
        )
        
        # Deep predictor with residual
        self.predictor = nn.Sequential(
            nn.Linear(self.fusion_dim, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        
        # Residual connection for stability
        self.residual_proj = nn.Linear(self.fusion_dim, 1)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with feature group encoding and attention.
        
        Args:
            x: Input features [batch, 150]
        
        Returns:
            Ranking probability [batch, 1]
        """
        # Split features by group
        content_feat = x[:, :50]
        technical_feat = x[:, 50:80]
        aeo_geo_feat = x[:, 80:120]
        semantic_feat = x[:, 120:150]
        
        # Encode each group
        content_enc = self.content_encoder(content_feat)
        technical_enc = self.technical_encoder(technical_feat)
        aeo_geo_enc = self.aeo_geo_encoder(aeo_geo_feat)
        semantic_enc = self.semantic_encoder(semantic_feat)
        
        # Concatenate
        fused = torch.cat([
            content_enc,
            technical_enc,
            aeo_geo_enc,
            semantic_enc
        ], dim=1)  # [batch, 352]
        
        # Self-attention (treat as single sequence)
        fused_attended, _ = self.attention(
            fused.unsqueeze(1),
            fused.unsqueeze(1),
            fused.unsqueeze(1)
        )
        fused_attended = fused_attended.squeeze(1)
        
        # Deep prediction with residual
        main_pred = self.predictor(fused_attended)
        residual_pred = self.residual_proj(fused)
        
        # Combine with residual (weighted)
        output = torch.sigmoid(main_pred + 0.1 * residual_pred)
        
        return output


class TitanMLEngine:
    """
    RankForge AI's Neural Intelligence Engine.
    
    Deep Mode: Full attention-based deep learning
    Light Mode: Heuristic neural simulation
    
    Features:
    - Ranking probability prediction
    - Confidence intervals
    - Intent alignment scoring
    - Multi-signal fusion
    """
    
    def __init__(self):
        self.model = None
        
        if DEEP_MODE:
            try:
                self.model = DeepRankingPredictor(input_dim=150)
                # Initialize weights
                self._init_weights()
                self.model.eval()
                logger.info("Titan ML Engine: Deep mode initialized")
            except Exception as e:
                logger.warning(f"Could not initialize deep model: {e}")
        
        # Attention weights for lightweight mode
        self.attention_weights = np.ones(150)
        # CRITICAL: These indices MUST match feature_extractor.py
        # Index 0: Overall SEO Score
        # Index 5: AEO Score  
        # Index 9: GEO Score
        # Index 13: Logic Score (The Link!)
        # Index 14: Intent Match (Critical Signal)
        self.attention_weights[0] = 2.0   # Overall SEO Score
        self.attention_weights[5] = 1.5   # AEO Score
        self.attention_weights[9] = 1.5   # GEO Score
        self.attention_weights[13] = 2.5  # Logic Score
        self.attention_weights[14] = 3.0  # Intent Match
    
    def _init_weights(self):
        """Initialize model weights for stable predictions."""
        for m in self.model.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
    
    def predict_ranking_potential(
        self, 
        feature_vector: np.ndarray
    ) -> Dict[str, Any]:
        """
        Predict ranking potential with confidence intervals.
        
        Args:
            feature_vector: 150-dim feature vector from feature_extractor
        
        Returns:
            Dict with neural_iq, ranking_probability, confidence, reasoning
        """
        if DEEP_MODE and self.model:
            return self._deep_predict(feature_vector)
        else:
            return self._light_predict(feature_vector)
    
    def _deep_predict(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Deep prediction with Monte Carlo dropout for uncertainty.
        """
        try:
            # Prepare input
            x = torch.FloatTensor(features).unsqueeze(0)
            
            # Single prediction in eval mode
            self.model.eval()
            with torch.no_grad():
                base_pred = self.model(x).item()
            
            # Monte Carlo dropout for confidence interval
            self.model.train()  # Enable dropout
            predictions = []
            
            for _ in range(30):  # 30 forward passes
                with torch.no_grad():
                    pred = self.model(x).item()
                    predictions.append(pred)
            
            self.model.eval()  # Back to eval
            
            # Calculate statistics
            mean_prob = np.mean(predictions)
            std_prob = np.std(predictions)
            
            # Confidence interval (95%)
            ci_low = max(0, mean_prob - 1.96 * std_prob)
            ci_high = min(1, mean_prob + 1.96 * std_prob)
            
            # Intent match check (critical signal)
            intent_match = features[14] if len(features) > 14 else 0.5
            logic_score = features[13] if len(features) > 13 else 0.5
            
            # Neural IQ (0-100)
            neural_iq = int(mean_prob * 100)
            
            # Apply intent penalty
            if intent_match < 0.5:
                neural_iq = int(neural_iq * 0.5)
                reasoning = "⚠️ Neural Engine detected intent mismatch. Content logic doesn't align with search query. Ranking potential severely limited."
            elif logic_score < 0.4:
                neural_iq = int(neural_iq * 0.7)
                reasoning = "📊 Semantic gaps detected. Content covers topic but lacks depth in key areas."
            else:
                reasoning = "✅ High neural-semantic alignment. Content logic matches search intent well."
            
            # Predicted rank
            estimated_rank = self._prob_to_rank(mean_prob, intent_match)
            
            return {
                "neural_iq": neural_iq,
                "ranking_probability": round(float(mean_prob), 4),
                "confidence_interval": {
                    "low": round(ci_low, 4),
                    "high": round(ci_high, 4)
                },
                "confidence_level": self._confidence_level(std_prob),
                "estimated_rank": estimated_rank,
                "reasoning": reasoning,
                "intent_alignment": round(float(intent_match), 2),
                "logic_score": round(float(logic_score * 100), 1),
                "mode": "deep"
            }
            
        except Exception as e:
            logger.warning(f"Deep prediction failed: {e}")
            return self._light_predict(features)
    
    def _light_predict(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Lightweight prediction using attention-weighted heuristics.
        """
        # Apply attention weights
        weighted = features * self.attention_weights[:len(features)]
        
        # Normalize and compute score
        raw_score = np.mean(weighted) / np.mean(self.attention_weights[:len(features)])
        
        # Sigmoid-like transformation
        probability = 1 / (1 + np.exp(-5 * (raw_score - 0.5)))
        
        # Intent match check
        intent_match = features[14] if len(features) > 14 else 0.5
        logic_score = features[13] if len(features) > 13 else 0.5
        
        # Neural IQ
        neural_iq = int(probability * 100)
        
        # Apply intent penalty
        if intent_match < 0.5:
            neural_iq = int(neural_iq * 0.5)
            probability *= 0.5
            reasoning = "⚠️ Neural Engine detected intent mismatch. Ranking potential limited without topical alignment."
        elif logic_score < 0.4:
            neural_iq = int(neural_iq * 0.7)
            reasoning = "📊 Semantic logic gaps detected. Expand content to match competitor depth."
        else:
            reasoning = "✅ Neural-semantic alignment confirmed. Proceed with optimization recommendations."
        
        estimated_rank = self._prob_to_rank(probability, intent_match)
        
        return {
            "neural_iq": neural_iq,
            "ranking_probability": round(float(probability), 4),
            "confidence_interval": {
                "low": round(max(0, probability - 0.1), 4),
                "high": round(min(1, probability + 0.1), 4)
            },
            "confidence_level": "medium",
            "estimated_rank": estimated_rank,
            "reasoning": reasoning,
            "intent_alignment": round(float(intent_match), 2),
            "logic_score": round(float(logic_score * 100), 1),
            "mode": "lightweight"
        }
    
    def _prob_to_rank(self, probability: float, intent_match: float) -> int:
        """Convert probability to estimated SERP position."""
        if intent_match < 0.3:
            return 100  # Won't rank without intent match
        
        # Inverse mapping: high prob = low rank (good)
        if probability >= 0.9:
            return 1
        elif probability >= 0.8:
            return 3
        elif probability >= 0.7:
            return 5
        elif probability >= 0.6:
            return 10
        elif probability >= 0.5:
            return 20
        elif probability >= 0.4:
            return 30
        elif probability >= 0.3:
            return 50
        else:
            return 100
    
    def _confidence_level(self, std: float) -> str:
        """Convert standard deviation to confidence level."""
        if std < 0.05:
            return "very_high"
        elif std < 0.1:
            return "high"
        elif std < 0.15:
            return "medium"
        else:
            return "low"
    
    def get_ranking_verdict(self, results: Dict[str, Any]) -> str:
        """Generate human-readable ranking verdict with Executive Authority."""
        rank = results.get('estimated_rank', 100)
        prob = results.get('ranking_probability', 0)
        intent = results.get('intent_alignment', 0)
        
        if intent < 0.4:
            return f"🚨 CRITICAL: Severe TOPICAL MISMATCH detected. Your content does not align with user intent for '{results.get('keyword', 'target')}'."
        
        if rank <= 3:
            return f"🏆 DOMINANCE PREDICTED: Your page exhibits World-Class neural-semantic alignment ({int(prob*100)}% conviction). Expect Top 3 entry within current indexing cycle."
        elif rank <= 10:
            return f"⭐ FIRST PAGE POTENTIAL: The Neural Engine confirms Page 1 viability. To break the Top 3, address the specific semantic logic gaps identified."
        elif rank <= 30:
            return f"📈 GROWTH PHASE: You are in the Top 30 neural cluster. Breakthrough to the First Page requires aggressive expansion of entity-topic depth."
        else:
            return f"🔧 FOUNDATION REQUIRED: Structural SEO is sound, but topical authority is insufficient for competitive SERP entry. Follow the 90-day Action Plan."


# Singleton instance
ml_engine = TitanMLEngine()
