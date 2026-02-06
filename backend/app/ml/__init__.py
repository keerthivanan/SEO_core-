"""
Titan ML 2.0 - Advanced Deep Learning Module
============================================

This module contains production-grade ML components:
1. SEO Embeddings (Transformer)
2. Quality Scorer (DistilBERT)
3. RL Agent (DQN)
4. Link Predictor (GNN)

All components gracefully fallback to lightweight mode if dependencies missing.
"""

import logging

logger = logging.getLogger(__name__)

# Check for heavy ML dependencies
try:
    import torch
    TORCH_AVAILABLE = True
    logger.info("PyTorch available - Titan ML 2.0 enabled")
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch not installed - using lightweight ML mode")

try:
    from transformers import AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# Export availability flags
TITAN_ML_AVAILABLE = TORCH_AVAILABLE and TRANSFORMERS_AVAILABLE
__all__ = ['TORCH_AVAILABLE', 'TRANSFORMERS_AVAILABLE', 'TITAN_ML_AVAILABLE']
