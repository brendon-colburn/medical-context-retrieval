# Demo Query Examples

This directory contains curated example queries designed to showcase the medical RAG system's capabilities during demonstrations.

## Query Categories

### 1. **Cancer Screening** (Easy)
Best for initial demos - straightforward questions with clear, authoritative answers.
- Breast cancer screening recommendations
- Colorectal cancer screening guidelines
- Mammogram age recommendations

### 2. **Cancer Treatment** (Medium)
Shows retrieval of detailed clinical protocols.
- Pediatric Hodgkin lymphoma treatment
- Chemotherapy side effects
- Treatment comparisons

### 3. **Cardiovascular Health** (Easy-Medium)
General health guidance from NHLBI sources.
- Risk factors for heart disease
- Lifestyle modifications
- Preventive care

### 4. **Chronic Disease Management** (Medium)
Complex, multi-source queries.
- Diabetes management
- Hypertension guidelines

### 5. **Preventive Care** (Easy-Medium)
Vaccination and screening recommendations.
- Adult vaccination schedules
- Age-specific preventive care

## Demo Strategy

### For Quick Demos (5-10 minutes)
Use these queries in order:
1. "What are the current USPSTF recommendations for breast cancer screening?"
2. "What are the treatment options for pediatric Hodgkin lymphoma?"
3. "At what age should I start getting mammograms?"

These demonstrate:
- Fast, accurate retrieval
- Multiple data sources
- Patient-friendly and clinical queries
- Clear source citations

### For Comprehensive Demos (20-30 minutes)
Show the full range:
1. Start with easy query (breast cancer screening)
2. Show complex query (treatment comparisons)
3. Demonstrate edge case handling (single word or out-of-scope)
4. Compare with/without contextual headers
5. Show performance metrics

### For Technical Audiences
Focus on:
- Vector similarity scores
- Retrieval accuracy metrics
- Header enhancement impact
- System architecture

## Query Files

- `sample_queries.json` - Structured query database with metadata
- Use this file to programmatically load demo queries

## Tips for Live Demos

1. **Pre-load the index** - Don't build it live (takes too long)
2. **Start with easy wins** - Build confidence with clear, strong results
3. **Show variety** - Mix screening, treatment, and prevention queries
4. **Highlight citations** - Emphasize source URLs for credibility
5. **Discuss scores** - Explain what confidence scores mean
6. **Compare systems** - If possible, show vs. generic ChatGPT/Copilot
