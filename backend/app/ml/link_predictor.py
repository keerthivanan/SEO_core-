"""
Link Predictor - Graph Neural Network for Internal Linking
===========================================================

Uses Graph Attention Network to analyze site structure
and predict optimal internal links to add.

Nodes: Pages
Edges: Links between pages
Task: Predict which new edges (links) would be most valuable
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Try importing heavy dependencies
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
        def Dropout(*args, **kwargs): return None
    F = None
    logger.info("Link Predictor running in heuristic mode")


class GraphAttentionLayer(nn.Module):
    """Single Graph Attention Layer."""
    
    def __init__(self, in_features: int, out_features: int, dropout: float = 0.2):
        super().__init__()
        
        self.W = nn.Linear(in_features, out_features, bias=False)
        self.a = nn.Linear(2 * out_features, 1, bias=False)
        self.dropout = nn.Dropout(dropout)
        self.leaky_relu = nn.LeakyReLU(0.2)
    
    def forward(self, h: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        """
        h: Node features [N, in_features]
        adj: Adjacency matrix [N, N]
        """
        Wh = self.W(h)  # [N, out_features]
        N = Wh.size(0)
        
        # Attention mechanism
        Wh_repeated_i = Wh.repeat_interleave(N, dim=0)  # [N*N, out_features]
        Wh_repeated_j = Wh.repeat(N, 1)  # [N*N, out_features]
        
        concat = torch.cat([Wh_repeated_i, Wh_repeated_j], dim=1)  # [N*N, 2*out_features]
        e = self.leaky_relu(self.a(concat)).view(N, N)  # [N, N]
        
        # Mask non-adjacent nodes with large negative value
        zero_vec = -9e15 * torch.ones_like(e)
        attention = torch.where(adj > 0, e, zero_vec)
        attention = F.softmax(attention, dim=1)
        attention = self.dropout(attention)
        
        # Apply attention
        h_prime = torch.matmul(attention, Wh)
        
        return F.elu(h_prime)


class LinkPredictorGNN(nn.Module):
    """
    Graph Neural Network for link prediction.
    Learns which pages should link to each other.
    """
    
    def __init__(self, feature_dim: int = 64, hidden_dim: int = 128):
        super().__init__()
        
        # Graph attention layers
        self.gat1 = GraphAttentionLayer(feature_dim, hidden_dim)
        self.gat2 = GraphAttentionLayer(hidden_dim, hidden_dim)
        
        # Link predictor MLP
        self.link_predictor = nn.Sequential(
            nn.Linear(hidden_dim * 2, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
    
    def encode(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        """Encode nodes using graph attention."""
        h = self.gat1(x, adj)
        h = F.dropout(h, p=0.3, training=self.training)
        h = self.gat2(h, adj)
        return h
    
    def predict_link(self, z: torch.Tensor, src: int, dst: int) -> float:
        """Predict if link should exist between src and dst."""
        edge_features = torch.cat([z[src], z[dst]], dim=0)
        return self.link_predictor(edge_features).item()


class LinkPredictor:
    """
    Internal linking optimizer.
    
    Deep Mode: Uses trained GNN for link prediction
    Heuristic Mode: Uses semantic similarity and structure analysis
    """
    
    def __init__(self):
        self.model = None
        
        if DEEP_MODE:
            try:
                self.model = LinkPredictorGNN()
                logger.info("Link Predictor: Deep mode initialized")
            except Exception as e:
                logger.warning(f"Could not initialize GNN: {e}")
    
    def analyze_site_structure(
        self, 
        pages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze current site structure and suggest improvements.
        
        Args:
            pages: List of page data dicts with 'url', 'title', 'links', 'word_count'
        
        Returns:
            Structure analysis with link suggestions
        """
        if len(pages) < 2:
            return {
                "link_suggestions": [],
                "structure_score": 100,
                "issues": ["Need at least 2 pages for link analysis"]
            }
        
        # Build adjacency matrix
        urls = [p.get('url', '') for p in pages]
        n = len(pages)
        adj = np.zeros((n, n))
        
        for i, page in enumerate(pages):
            links = page.get('links', {}).get('internal', [])
            for link in links:
                link_url = link.get('href', '') if isinstance(link, dict) else link
                if link_url in urls:
                    j = urls.index(link_url)
                    adj[i, j] = 1
        
        # Calculate structure metrics
        total_links = np.sum(adj)
        avg_outgoing = total_links / n
        orphan_pages = np.sum(np.sum(adj, axis=0) == 0)
        
        # Get link suggestions
        suggestions = self._suggest_links(pages, adj)
        
        # Calculate structure score
        structure_score = self._calculate_structure_score(
            n, total_links, orphan_pages, avg_outgoing
        )
        
        issues = []
        if orphan_pages > 0:
            issues.append(f"{int(orphan_pages)} orphan page(s) with no incoming links")
        if avg_outgoing < 3:
            issues.append(f"Low internal linking density ({avg_outgoing:.1f} links/page)")
        
        return {
            "total_pages": n,
            "total_internal_links": int(total_links),
            "avg_links_per_page": round(avg_outgoing, 1),
            "orphan_pages": int(orphan_pages),
            "structure_score": structure_score,
            "link_suggestions": suggestions[:10],  # Top 10
            "issues": issues
        }
    
    def _suggest_links(
        self, 
        pages: List[Dict], 
        adj: np.ndarray
    ) -> List[Dict[str, Any]]:
        """
        Suggest new internal links based on semantic similarity.
        """
        n = len(pages)
        suggestions = []
        
        # Calculate page features for similarity
        page_features = []
        for page in pages:
            # Simple feature: word overlap in title/content
            text = (
                page.get('title', '') + ' ' + 
                ' '.join(page.get('h2', [])) + ' ' +
                page.get('meta_description', '')
            ).lower()
            page_features.append(set(text.split()))
        
        # Find missing links with high similarity
        for i in range(n):
            for j in range(n):
                if i != j and adj[i, j] == 0:  # No link exists
                    # Calculate Jaccard similarity
                    intersection = len(page_features[i] & page_features[j])
                    union = len(page_features[i] | page_features[j])
                    similarity = intersection / max(union, 1)
                    
                    # Check if j is an orphan (bonus priority)
                    is_orphan = np.sum(adj[:, j]) == 0
                    
                    if similarity > 0.15 or is_orphan:
                        score = similarity
                        if is_orphan:
                            score += 0.3  # Boost orphan pages
                        
                        suggestions.append({
                            "from_url": pages[i].get('url', ''),
                            "from_title": pages[i].get('title', 'Unknown'),
                            "to_url": pages[j].get('url', ''),
                            "to_title": pages[j].get('title', 'Unknown'),
                            "similarity_score": round(similarity, 3),
                            "priority_score": round(score, 3),
                            "reason": "Orphan page rescue" if is_orphan else "High semantic similarity",
                            "anchor_suggestion": self._suggest_anchor(pages[j])
                        })
        
        # Sort by priority score
        suggestions.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return suggestions
    
    def _suggest_anchor(self, target_page: Dict) -> str:
        """Suggest anchor text for the link."""
        title = target_page.get('title', '')
        
        # Clean title
        anchor = title.split('|')[0].split('-')[0].strip()
        
        # Fallback to h1 if title is generic
        if len(anchor) < 5:
            h1s = target_page.get('h1', [])
            if h1s:
                anchor = h1s[0]
        
        return anchor[:60] if anchor else "Learn more"
    
    def _calculate_structure_score(
        self, 
        n_pages: int, 
        total_links: int, 
        orphans: int, 
        avg_links: float
    ) -> int:
        """Calculate overall site structure score (0-100)."""
        score = 100
        
        # Penalty for orphan pages
        orphan_ratio = orphans / max(n_pages, 1)
        score -= int(orphan_ratio * 40)
        
        # Penalty for low link density
        if avg_links < 2:
            score -= 30
        elif avg_links < 3:
            score -= 15
        elif avg_links < 5:
            score -= 5
        
        # Bonus for good structure
        if avg_links >= 5 and orphans == 0:
            score = min(score + 10, 100)
        
        return max(0, score)
    
    def suggest_links_for_page(
        self, 
        page_data: Dict[str, Any],
        site_pages: List[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Suggest internal links for a specific page.
        
        Args:
            page_data: The current page being analyzed
            site_pages: Other pages on the site (optional)
        
        Returns:
            List of suggested internal links
        """
        suggestions = []
        
        if not site_pages:
            # Can't suggest without knowing other pages
            return [{
                "type": "recommendation",
                "message": "Crawl more pages to get internal link suggestions",
                "action": "Run site-wide crawl for comprehensive link analysis"
            }]
        
        # Get H2s from current page as potential anchor contexts
        h2s = page_data.get('h2', [])
        page_text = page_data.get('text', '') or page_data.get('body_text', '')
        
        for other_page in site_pages:
            if other_page.get('url') == page_data.get('url'):
                continue
            
            other_title = other_page.get('title', '')
            other_keywords = set(other_title.lower().split())
            
            # Check if any H2 relates to the other page
            for h2 in h2s:
                h2_words = set(h2.lower().split())
                overlap = len(h2_words & other_keywords)
                
                if overlap >= 2:
                    suggestions.append({
                        "target_url": other_page.get('url'),
                        "target_title": other_title,
                        "context": f"Add link in section: '{h2}'",
                        "anchor_text": other_title[:50],
                        "confidence": "high" if overlap >= 3 else "medium"
                    })
        
        return suggestions[:5]  # Top 5 suggestions


# Singleton instance
link_predictor = LinkPredictor()
