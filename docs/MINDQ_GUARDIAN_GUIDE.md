# Mind-Q Guardian Adapter Guide

## Overview

The **Mind-Q Guardian Adapter** is a specialized extension of Guardian Enhanced v7, designed specifically for the Mind-Q V4.1 logistics data pipeline. It provides phase-aware context generation, pipeline structure mapping, and optimized LLM agent guidance for working with complex data engineering projects.

## Key Features

### 1. **Pipeline Spine Generation** 🧬
Automatically maps the entire Mind-Q pipeline structure:
- 21 sequential and optional phases
- Phase dependencies and flow edges
- KPI tracking (RTO%, SLA, COD, PSI, NZV)
- Phase grouping (data foundation, analytics, AI, BI)

### 2. **Phase Card Generation** 📊
Creates concise markdown "phase cards" for each pipeline stage:
- Goal and business impact
- Inputs and outputs
- Main code files (limited to 6 entries)
- Upstream/downstream dependencies
- KPI associations

### 3. **Context Optimization** 🎯
Generates LLM-friendly context strings:
- Spine context: Pipeline overview (< 1KB)
- Phase context: Detailed phase information
- Request-aware context: Auto-detects relevant phases from user queries

## Installation

The adapter is included in Guardian Enhanced v7:

```bash
# Clone Guardian-H
git clone https://github.com/Haithamhaj/guardian-h.git
cd guardian-h

# The adapter is at: src/guardian_mindq.py
```

## Usage

### Command Line Interface

#### 1. Build Pipeline Spine

```bash
python3 src/guardian_mindq.py /path/to/mind-q --build-spine
```

**Output:** `docs/mindq_spine.yaml` (< 10KB, LLM-safe)

**Content:**
```yaml
project: Mind-Q V4.1
type: logistics_data_pipeline
phases:
  - id: 01_ingestion
    name: Data Ingestion
    group: data_foundation
    optional: false
  - id: 02_quality
    name: Quality Checks
    ...
flows:
  - from: 01_ingestion
    to: 02_quality
    type: sequential
kpis:
  - name: RTO%
    description: Return to Origin percentage
    category: delivery
```

#### 2. Generate Phase Cards

```bash
# Generate all phase cards
python3 src/guardian_mindq.py /path/to/mind-q --generate-cards

# Generate specific phase card
python3 src/guardian_mindq.py /path/to/mind-q --phase 01_ingestion
```

**Output:** `docs/phases/{phase_id}.md`

**Example Card:**
```markdown
# Data Ingestion (01_ingestion)

**Group:** Data Foundation
**Optional:** No

## Goal
Ingest heterogeneous logistics data and normalize to unified format

## Business Impact
Guarantees trustworthy data foundation for all downstream analytics...

## Inputs
- Raw CSV/Parquet/Excel files
- SLA documents (optional)

## Outputs
- raw.parquet
- meta_ingestion.json
- missing_summary.json

## Main Code Files
- `phases/01_ingestion/impl.py`
- `phases/01_ingestion/config.yaml`

## Pipeline Position
**Downstream:** 02_quality
```

#### 3. Refresh All Artifacts

```bash
python3 src/guardian_mindq.py /path/to/mind-q --refresh-all
```

Generates:
- `docs/mindq_spine.yaml`
- `docs/phases/*.md` (15+ phase cards)

#### 4. Get Context for User Request

```bash
python3 src/guardian_mindq.py /path/to/mind-q --context "Fix the quality check issues"
```

**Output:** Relevant phase details automatically extracted

### Python API

```python
from src.guardian_mindq import MindQGuardianAdapter

# Initialize adapter
adapter = MindQGuardianAdapter("/path/to/mind-q")

# Build spine
spine = adapter.build_spine()
adapter.save_spine()  # Saves to docs/mindq_spine.yaml

# Generate phase card
card = adapter.generate_phase_card("01_ingestion")
adapter.save_phase_card("01_ingestion")  # Saves to docs/phases/

# Generate all cards
adapter.generate_all_phase_cards()

# Get optimized context for LLM agents
spine_context = adapter.get_spine_context()
phase_context = adapter.get_phase_context(["01_ingestion", "02_quality"])
smart_context = adapter.get_guardian_context_for_request("Help with ingestion phase")

# Refresh everything
results = adapter.refresh_all()
print(f"Generated: {len(results['phase_cards'])} phase cards")
```

## Integration with Guardian Enhanced

### Use with Guardian Enhanced Workflow

```python
from src.guardian_enhanced import GuardianEnhanced
from src.guardian_mindq import MindQGuardianAdapter

# Initialize both
guardian = GuardianEnhanced("/path/to/mind-q")
mindq_adapter = MindQGuardianAdapter("/path/to/mind-q")

# Refresh Mind-Q specific context
mindq_adapter.refresh_all()

# Run Guardian scan with Mind-Q awareness
guardian.scan()

# Get phase-specific context for AI agents
context = mindq_adapter.get_phase_context(["07_readiness", "08_insights"])

# Lock Mind-Q architectural decisions
guardian.lock_tech_decision(
    "Polars",
    "data_processing_library",
    "Mind-Q uses Polars for streaming analytics",
    status="PERMANENT"
)
```

## Architecture

### Pipeline Structure Recognition

The adapter recognizes Mind-Q's multi-phase structure:

```
Data Foundation (01-04)
├── 01_ingestion: Raw data normalization
├── 02_quality: Quality checks and validation
├── 03_schema: Schema validation and terminology
└── 04_profile: Data profiling

Advanced Analytics (05-07)
├── 05_missing: Missing value repair
├── 06_standardize: Standardization
├── 06_feature_eng: Feature engineering
└── 07_readiness: Readiness assessment

AI & Insights (7.5-8)
├── 07_5_feature_report: Feature reporting
├── 07_6_llm_summary: LLM summaries
├── 07_7_business_correlations: Business correlations
└── 08_insights: Insights generation

Business Intelligence (09-10)
├── 09_business_validation: Business validation
└── 10_bi: BI delivery
```

### Context Size Optimization

The adapter keeps context strings LLM-friendly:

| Artifact | Size | Purpose |
|----------|------|---------|
| `mindq_spine.yaml` | < 10KB | Full pipeline structure |
| Phase card | < 1KB | Individual phase details |
| Spine context | < 1KB | Pipeline overview string |
| Phase context (3 phases) | < 3KB | Focused phase details |

### Smart Context Selection

When processing user requests, the adapter:

1. **Detects mentioned phases** from request text
2. **Retrieves relevant phase cards**
3. **Limits to top 3 phases** to avoid token waste
4. **Falls back to spine overview** if no phases detected

Example:
```python
# User request: "Fix the quality check failures in stage 02"
context = adapter.get_guardian_context_for_request(
    "Fix the quality check failures in stage 02"
)
# Returns: Detailed info about 02_quality phase
```

## Benefits for AI Agents

### 1. **Reduced Context Windows**
- Spine: 1KB vs 50KB+ full documentation
- Phase cards: Replace reading entire phase implementation
- Smart filtering: Only relevant phases included

### 2. **Consistent Structure**
- Every phase follows same card format
- Predictable information layout
- Easy for LLMs to parse and reason about

### 3. **Pipeline Awareness**
- Agents understand upstream/downstream dependencies
- Can reason about data flow between phases
- Avoid breaking dependencies

### 4. **Business Context**
- KPIs clearly mapped to phases
- Business impact explicitly stated
- Logistics domain knowledge embedded

## Real-World Example

### Scenario: AI Agent Working on Phase 07

**Without Mind-Q Guardian:**
```
Agent needs to read:
- PHASES_DETAILED_GUIDE.md (150KB)
- phases/07_readiness/impl.py (5KB)
- phases/06_feature_eng/impl.py (4KB)
- contracts/* (10KB)
Total: 169KB context
```

**With Mind-Q Guardian:**
```
Agent gets:
- mindq_spine.yaml (8KB)
- docs/phases/07_readiness.md (0.7KB)
- docs/phases/06_feature_eng.md (0.7KB)
Total: 9.4KB context (94% reduction!)
```

### Performance Impact

- **Token savings:** 94% reduction in context size
- **Faster responses:** Less processing time for LLM
- **Better accuracy:** Focused, relevant information only
- **Cost savings:** Fewer tokens = lower API costs

## Best Practices

### 1. **Regenerate After Major Changes**

```bash
# After adding new phases or updating pipeline
python3 src/guardian_mindq.py /path/to/mind-q --refresh-all
```

### 2. **Commit Generated Artifacts**

```bash
# Add to version control for team collaboration
git add docs/mindq_spine.yaml docs/phases/*.md
git commit -m "Update Mind-Q Guardian artifacts"
```

### 3. **Use with IDE AI Assistants**

Place `mindq_spine.yaml` in:
- `.cursor/rules/` for Cursor
- `.windsurf/rules/` for Windsurf
- `.github/` for Copilot

### 4. **Update Phase Cards for Custom Phases**

If you add custom phases:
```python
# Add to phase_sequence in guardian_mindq.py
self.phase_sequence = [
    ...
    "13_custom_phase",  # Add here
]

# Regenerate
adapter.refresh_all()
```

## Troubleshooting

### Issue: "Phase cards not generated for all phases"

**Cause:** Some phases don't have directories in `phases/`

**Solution:** The adapter only generates cards for:
- Phases with existing directories
- Non-optional phases (always generated)

This is intentional to avoid documenting unimplemented optional phases.

### Issue: "Spine context too large"

**Cause:** Too many phases or verbose descriptions

**Solution:** The adapter automatically limits:
- Phase descriptions to 200 chars
- KPIs to top 5
- Context to most relevant phases

### Issue: "Context doesn't match my request"

**Cause:** Phase detection relies on keyword matching

**Solution:** Use explicit phase IDs in requests:
```
❌ "Fix the data issues"
✅ "Fix the data issues in phase 02_quality"
```

## Future Enhancements

Planned features for Mind-Q Guardian v2:

- [ ] **Phase dependency graph visualization**
- [ ] **Automated phase health scoring**
- [ ] **KPI anomaly detection per phase**
- [ ] **Custom phase templates**
- [ ] **Integration with Guardian MCP server**
- [ ] **Real-time pipeline monitoring**
- [ ] **Phase execution recommendations**

## Support

For issues or questions:
- **Guardian-H Issues:** https://github.com/Haithamhaj/guardian-h/issues
- **Mind-Q Issues:** https://github.com/Haithamhaj/Mind-Q-V4.1/issues

## License

Part of Guardian Enhanced v7.0, same license as Guardian-H.

---

**Made with 💡 by Haitham & GitHub Copilot**

*Last Updated: December 2024*
