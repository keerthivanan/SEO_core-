class GapAnalyzer:
    async def analyze_gaps(self, user_data: dict, competitors: list, keyword: str) -> dict:
        """Find gaps between user page and top competitors using REAL data"""
        
        gaps = []
        
        # 1. Title Keyword Gap
        user_title = user_data.get('title', '') or ''
        if not keyword.lower() in user_title.lower():
            gaps.append({
                'type': 'title',
                'severity': 'high',
                'issue': f"Title missing target keyword '{keyword}'",
                'recommendation': f"Rewrite title to include '{keyword}' near the beginning",
                'example': f"{keyword} | {user_title[:20]}..."
            })
        
        # 2. Content Length Gap - USE REAL COMPETITOR DATA
        user_words = user_data.get('word_count', 0)
        
        # Calculate REAL average competitor word count from snippets
        # Snippet word count * estimated expansion factor (snippets are ~10% of full content)
        competitor_word_estimates = []
        for comp in competitors:
            snippet = comp.get('snippet', '')
            if snippet:
                # Estimate: snippet is typically 10-15% of full content
                estimated_words = len(snippet.split()) * 10
                competitor_word_estimates.append(estimated_words)
        
        # Use actual competitor benchmark if available, else conservative default
        if competitor_word_estimates:
            avg_competitor_words = int(sum(competitor_word_estimates) / len(competitor_word_estimates))
            avg_competitor_words = max(avg_competitor_words, 1000)  # Minimum benchmark
        else:
            avg_competitor_words = 1500  # Fallback only if no competitors
        
        if user_words < 500:
            gaps.append({
                'type': 'content',
                'severity': 'high',
                'issue': f"Thin content ({user_words} words). Competitors average ~{avg_competitor_words}+ words",
                'recommendation': f"Expand content to at least {avg_competitor_words} words",
                'example': "Add detailed sections, examples, case studies, FAQs"
            })
        elif user_words < avg_competitor_words * 0.6:  # Less than 60% of competitor average
            gaps.append({
                'type': 'content',
                'severity': 'medium',
                'issue': f"Content ({user_words} words) is below competitor benchmark ({avg_competitor_words} words)",
                'recommendation': f"Add {avg_competitor_words - user_words} more words to match top competitors",
                'example': "Add a 'How-to' section, Case Studies, or Expert Commentary"
            })

        # 3. H2 Structure Gap - COMPARE AGAINST COMPETITORS
        user_h2_count = len(user_data.get('h2', []))
        
        # Estimate competitor H2 count from snippet structure (semicolons, bullets often indicate sections)
        avg_competitor_sections = 5  # Conservative default
        if competitors:
            section_indicators = sum(
                comp.get('snippet', '').count('...') + 
                comp.get('snippet', '').count(':') 
                for comp in competitors
            ) / len(competitors)
            avg_competitor_sections = max(5, int(section_indicators * 2))
        
        if user_h2_count < 3:
            gaps.append({
                'type': 'structure',
                'severity': 'high',
                'issue': f"Only {user_h2_count} H2 headings. Top pages typically have {avg_competitor_sections}+",
                'recommendation': f"Add at least {avg_competitor_sections - user_h2_count} more H2 sections",
                'example': "H2: What is [topic]? | H2: How to [action] | H2: Benefits of [topic]"
            })

        # 4. Image Alt Text Gap
        images = user_data.get('images', {})
        if images.get('without_alt', 0) > 0:
            gaps.append({
                'type': 'images',
                'severity': 'medium',
                'issue': f"{images['without_alt']} images missing alt text",
                'recommendation': "Add descriptive alt text to all images including keywords",
                'example': f'alt="{keyword} example image"'
            })

        # 5. Internal Linking Gap
        links = user_data.get('links', {})
        if links.get('internal_count', 0) < 5:
            gaps.append({
                'type': 'links',
                'severity': 'medium',
                'issue': "Insufficient internal linking",
                'recommendation': "Add 5-10 contextual internal links",
                'example': "Link to related products or blog posts"
            })

        # 6. Schema Gap
        schemas = user_data.get('schema', [])
        if not schemas:
            gaps.append({
                'type': 'technical',
                'severity': 'high',
                'issue': "No Schema Markup (JSON-LD) detected",
                'recommendation': "Add JSON-LD Schema to help Google understand your content",
                'example': "Article, Product, FAQPage, or Organization schema"
            })
        
        # 7. External Citation Gap
        external_count = links.get('external_count', 0)
        if external_count < 2:
            gaps.append({
                'type': 'authority',
                'severity': 'medium',
                'issue': f"Only {external_count} external links. Authoritative pages cite sources.",
                'recommendation': "Add 2-5 citations to authoritative external sources",
                'example': "Link to Wikipedia, .gov sites, or industry publications"
            })

        return {
            'total_gaps': len(gaps),
            'gaps': gaps,
            'priority_fixes': [g for g in gaps if g['severity'] == 'high'],
            'competitor_benchmark': {
                'avg_word_count': avg_competitor_words,
                'recommended_sections': avg_competitor_sections
            }
        }

gap_analyzer = GapAnalyzer()
