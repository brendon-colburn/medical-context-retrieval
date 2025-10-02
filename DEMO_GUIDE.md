# Healthcare Showcase Demo Guide

## 🎯 Quick Setup for Showcase Room

### One-Time Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify `.env` file exists with credentials**

3. **Pre-warm the cache:**
   - Open `demo.ipynb` in Jupyter and run all cells once
   - This builds the index (saves ~5 minutes on first demo load)

### Daily Startup

```bash
./launch_demo.sh
```

Or manually:
```bash
voila demo.ipynb --port=8866 --template=lab
```

The demo will be accessible at: `http://localhost:8866`

---

## 🎬 Demo Script (5 minutes)

### Opening (30 seconds)
> "This is our medical guideline retrieval system. It searches across trusted sources like the National Cancer Institute, USPSTF, and NHLBI to find accurate medical information using advanced AI."

### Demo Flow (4 minutes)

**1. Start with an easy win:**
- Click "Example 1" or type: *"What are the current USPSTF recommendations for breast cancer screening?"*
- Click **Search Guidelines**
- **Key talking points:**
  - ✅ Results appear in seconds
  - ✅ Color-coded confidence scores (green = high relevance)
  - ✅ Source citations for verification
  - ✅ Context headers show where info comes from

**2. Show variety:**
- Try Example 2: *"What are the treatment options for pediatric Hodgkin lymphoma?"*
- **Key talking points:**
  - ✅ Handles both screening and treatment queries
  - ✅ Multiple result cards ranked by relevance
  - ✅ Real medical guideline text (not made up)

**3. Interactive element:**
- Ask the visitor: *"Do you have a medical topic you'd like to explore?"*
- Type their query or suggest: *"What are the risk factors for cardiovascular disease?"*

**4. Highlight the innovation:**
- Scroll to **Performance Highlights** section
- **Key talking points:**
  - ✅ Our contextual header system improves accuracy by X%
  - ✅ Better than generic ChatGPT for medical queries
  - ✅ Built in-house with full control over data and logic

### Closing (30 seconds)
> "This system demonstrates how we can build specialized AI for healthcare that's more accurate than commercial alternatives, keeps data under our control, and can be customized for specific clinical workflows."

---

## 🗣️ Key Talking Points

### For Healthcare Executives
- **Cost savings**: No expensive SaaS subscriptions
- **Data control**: Your data never leaves your environment
- **Customization**: Tailor to your specific guidelines and workflows
- **Compliance**: Full audit trail and source citations

### For Clinical Stakeholders
- **Trusted sources**: Only authoritative guidelines (NCI, USPSTF, NHLBI)
- **Transparent**: Every answer shows its source
- **Fast**: Sub-second responses for clinical decision support
- **Comprehensive**: Searches thousands of guideline pages instantly

### For Technical Audiences
- **RAG architecture**: Vector embeddings + FAISS search
- **Context enhancement**: Proprietary header generation improves retrieval
- **Measurable**: Quantified performance metrics vs. baseline
- **Modular**: Clean Python codebase, easy to extend

---

## ❓ Common Questions & Answers

**Q: How current is the data?**
> A: The system scrapes from authoritative sources. We can schedule automatic updates or trigger manual refreshes when guidelines change.

**Q: Can it answer any medical question?**
> A: It searches the guidelines we've loaded (cancer, screening, cardiovascular). We can add more sources based on your needs.

**Q: Is this ready for production?**
> A: This is a proof-of-concept. Production deployment would add authentication, logging, compliance features, and integration with your EHR system.

**Q: How does it compare to ChatGPT/Copilot?**
> A: Generic LLMs can hallucinate medical information. Our system only retrieves actual guideline text and cites sources. Plus, you control the data.

**Q: What about patient privacy?**
> A: This demo searches guidelines, not patient data. For patient queries, we'd implement HIPAA-compliant infrastructure with proper access controls.

**Q: How long did this take to build?**
> A: The core system was built in about a week. Production hardening typically takes 2-4 additional weeks.

---

## 🔧 Troubleshooting

### Demo won't start
```bash
# Check if port is already in use
lsof -i :8866

# Try a different port
voila demo.ipynb --port=8877 --template=lab
```

### "Loading medical knowledge base" takes forever
- First load builds the index (~5 minutes)
- Pre-warm by running all cells in Jupyter once
- Check cache/ directory has files

### Search returns errors
- Verify `.env` has correct Azure OpenAI credentials
- Check Azure OpenAI quota/rate limits
- Look for error messages in terminal

### Results look weird
- Clear browser cache
- Restart Voilà server
- Check `voila_config/static/custom.css` loaded

---

## 📊 Metrics to Highlight

Load from `artifacts/header_impact_evaluation.json`:
- **Improvement**: X% accuracy boost from contextual headers
- **Speed**: Sub-second query response time
- **Coverage**: X,XXX medical guideline sections indexed
- **Sources**: 3 authoritative medical organizations

---

## 🎨 Customization for Your Organization

### Add Your Logo
Edit `voila_config/static/custom.css` and add:
```css
body::before {
    content: url('/path/to/logo.png');
    display: block;
    text-align: center;
}
```

### Change Color Scheme
Edit CSS variables in `custom.css`:
```css
:root {
    --primary-color: #YOUR_BRAND_COLOR;
}
```

### Add More Example Queries
Edit `examples/sample_queries.json` with domain-specific examples.

---

## 📱 For Kiosk/Touchscreen Deployment

```bash
# Full-screen kiosk mode
voila demo.ipynb \
    --port=8866 \
    --no-browser \
    --template=lab \
    --VoilaConfiguration.file_whitelist="['.*']"
```

Then set your browser to kiosk mode:
- **Chrome**: `chromium-browser --kiosk http://localhost:8866`
- **Firefox**: Press F11 for fullscreen

---

**Last Updated**: 2025-10-02
**Demo Version**: 1.0.0
