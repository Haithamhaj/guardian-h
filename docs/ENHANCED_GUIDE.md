# 🛡️ Guardian-H Enhanced v7.0 - Complete Guide

## 🌟 What's New in v7.0

Guardian-H v7.0 introduces **Advanced AI Agent Memory & Decision Management System** - a comprehensive solution to the 26 pain points identified in working with AI coding agents.

### 🎯 Core Features

1. **🧠 Enhanced Memory System**
   - Persistent memory across sessions
   - Decision tracking and locking
   - Change history with verification
   - Project snapshots with versioning
   - Health monitoring

2. **🎯 Decision Support System**
   - Technology recommendations
   - Conflict detection
   - Decision locking mechanism
   - Compatibility checking

3. **🔍 Quality Control System**
   - Dead code detection
   - Duplicate file finder
   - Structure enforcement
   - File activity tracking
   - Quality scoring

4. **📊 Health Monitoring**
   - Real-time project health
   - Agent fatigue detection
   - Verification tracking
   - Recommendations engine

---

## 🚀 Installation

### Option 1: npx (Recommended)
```bash
# Run enhanced version
npx guardian-h@latest

# Or use the enhanced command directly
npx guardian-enhanced
```

### Option 2: Install Globally
```bash
npm install -g guardian-h
guardian-enhanced
```

### Option 3: Python Direct (Full Features)
```bash
# Clone or download
git clone https://github.com/Haithamhaj/guardian-h
cd guardian-h

# Run enhanced scanner
python3 src/guardian_enhanced.py /path/to/your/project
```

---

## 📚 Usage Guide

### Basic Usage

```bash
# Scan current directory
guardian-enhanced

# Scan specific project
guardian-enhanced ./my-project

# Custom output
guardian-enhanced -o custom.mdc

# Skip quality check (faster)
guardian-enhanced --no-quality
```

### Advanced Usage

#### 1. Lock a Technology Decision

```bash
# Lock React as frontend framework
guardian-enhanced --lock-decision React frontend_framework "Team has React expertise"
```

Or programmatically:

```python
from src.guardian_enhanced import GuardianEnhanced

guardian = GuardianEnhanced("./my-project")
guardian.lock_tech_decision(
    tech_name="React",
    category="frontend_framework",
    reasoning="Team has 3 years React experience",
    status="PERMANENT"
)
```

#### 2. Check if Proposal Conflicts

```bash
# Check if switching to Vue conflicts
guardian-enhanced --check-proposal "Switch to Vue instead of React"
```

Output:
```
⛔ Cannot proceed - conflicts with 1 locked decision(s). Unlock them first.
```

#### 3. Get Technology Recommendations

```python
from src.guardian_enhanced import GuardianEnhanced

guardian = GuardianEnhanced("./my-project")
recommendations = guardian.get_tech_recommendation(
    category="frontend",
    project_type="web application",
    team_experience="beginner"
)

for rec in recommendations['recommendations']:
    print(f"{rec['name']}: score {rec['score']}")
```

#### 4. Run Quality Scan

```python
from src.quality_control import QualityController

qc = QualityController("./my-project")
report = qc.run_full_scan()

print(f"Dead code findings: {report['dead_code']['findings_count']}")
print(f"Duplicates: {report['duplicates']['count']}")
print(f"Health score: {report['summary']['health_score']}/100")
```

---

## 🗂️ Enhanced Guardian File Structure

The enhanced version creates a `.guardian` directory with persistent data:

```
.guardian/
├── decisions.json      # Locked technical decisions
├── changes.json        # Change history
├── sessions.json       # AI agent sessions
└── snapshots/          # Project snapshots
    ├── snapshot_20241208_140530.json
    └── snapshot_20241208_141215.json
```

---

## 📋 Enhanced MDC Format

The generated `guardian_enhanced.mdc` includes new sections:

```yaml
## 🔒 LOCKED_DECISIONS
- category: frontend_framework
  decision: React as frontend_framework
  status: PERMANENT
  reasoning: Team has React expertise
  locked_at: 2024-12-08T14:05:30

## 📝 CHANGE_HISTORY
- timestamp: 2024-12-08T14:10:15
  type: FILE_CREATED
  description: Created App.jsx
  verification: verified

## 💊 HEALTH_STATUS
status: healthy
score: 95/100
locked_decisions: 3
total_changes: 12
unverified_changes: 0

## 🔍 QUALITY_REPORT
code_health: 88/100
dead_code_findings: 2
duplicate_files: 1
structure_violations: 3

## 💡 RECOMMENDATIONS
- All systems healthy ✅
```

---

## 🤖 How AI Agents Use Enhanced Guardian

### Before Making Changes

```python
# Agent checks proposal against locked decisions
result = guardian.check_proposal("Switch from React to Vue")

if result['has_conflicts']:
    # Agent stops and asks user
    print(f"⛔ {result['recommendation']}")
    # Shows which decision conflicts and why
else:
    # Agent proceeds safely
    print(f"✅ {result['recommendation']}")
```

### After Making Changes

```python
# Agent logs the change
guardian.memory.log_change(
    ChangeType.FILE_CREATED,
    "Created UserProfile component",
    ["src/components/UserProfile.jsx"],
    "Implements user profile display feature"
)

# Later, mark as verified
guardian.memory.verify_change(change_id, "verified")
```

### Session Tracking

```python
# Start session
session = guardian.memory.start_session("cursor")

# Update with tasks
guardian.memory.update_session(
    session.session_id,
    task="Added user authentication",
    warning=False,  # No warnings
    error=False     # No errors
)

# Get health report
health = guardian.memory.get_health_report()
if health['status'] == 'concerning':
    print("⚠️ Consider starting fresh session")
```

---

## 🎯 Solving the 26 Pain Points

### Memory & Context Issues (4 problems)

✅ **Solution: Enhanced Memory System**
- Persistent decisions across sessions
- Session tracking with context
- Snapshot versioning
- Never loses context

### Files & Structure Issues (5 problems)

✅ **Solution: Quality Control System**
- Dead code detector finds unused files
- Duplicate finder prevents redundancy
- File registry tracks active files
- Structure enforcer maintains organization

### Verification & Trust Issues (3 problems)

✅ **Solution: Verification Layer**
- Change history with verification status
- Health monitoring detects agent fatigue
- Recommendations for recovery
- Truth checking through validation

### Technical Decision Issues (4 problems)

✅ **Solution: Decision Support System**
- Technology advisor provides context
- Decision locking prevents conflicts
- Conflict resolver catches contradictions
- Compatibility checking

### Documentation Issues (4 problems)

✅ **Solution: Auto-Documentation**
- Enhanced MDC with all sections
- Single source of truth
- Consistent format
- Auto-synced

### Long Conversation Issues (3 problems)

✅ **Solution: Session Management**
- Fatigue detection
- Session health scoring
- Recommendations to start fresh
- Context preservation

### Modification Issues (3 problems)

✅ **Solution: Change Tracking**
- Butterfly effect prevention
- Side effect tracking
- Impact analysis
- Rollback support via snapshots

---

## 🔧 Configuration

Create `.guardian/config.json` for custom settings:

```json
{
  "quality_control": {
    "max_file_lines": 500,
    "max_function_lines": 100,
    "similarity_threshold": 0.8
  },
  "health": {
    "warning_threshold": 70,
    "critical_threshold": 50
  },
  "decisions": {
    "auto_lock_tech_stack": true,
    "require_approval_for_unlock": true
  }
}
```

---

## 📊 API Reference

### EnhancedMemoryManager

```python
memory = EnhancedMemoryManager(project_path)

# Lock decisions
decision = memory.lock_decision(
    category="tech_stack",
    decision="React as frontend",
    reasoning="Team expertise",
    status=DecisionStatus.PERMANENT,
    alternatives=["Vue", "Angular"]
)

# Check conflicts
conflicts = memory.check_decision_conflict("Switch to Vue")

# Log changes
change = memory.log_change(
    ChangeType.FILE_CREATED,
    "Created App.jsx",
    ["src/App.jsx"],
    "Initial component"
)

# Manage sessions
session = memory.start_session("cursor")
memory.update_session(session_id, task="...")

# Get health
health = memory.get_health_report()

# Create snapshots
snapshot_id = memory.create_snapshot(data, label="before_refactor")
```

### TechnologyAdvisor

```python
advisor = TechnologyAdvisor()

# Get recommendations
recs = advisor.get_recommendation(
    TechCategory.FRONTEND_FRAMEWORK,
    project_type="web app",
    team_experience="beginner",
    current_stack=["typescript"]
)

# Check compatibility
result = advisor.check_compatibility("react", ["vue"])

# Explain choice
explanation = advisor.explain_choice("react", context)
```

### QualityController

```python
qc = QualityController(project_path)

# Full scan
report = qc.run_full_scan()

# Individual scans
dead_code = qc.dead_code_detector.scan()
duplicates = qc.duplicate_finder.scan()
violations = qc.structure_enforcer.scan()
registry = qc.file_registry.scan()
```

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python3 tests/test_enhanced.py

# Run specific test
python3 tests/test_enhanced.py TestMemoryManager
```

All 25 tests should pass:
- Memory Manager: 6 tests
- Tech Advisor: 4 tests
- Conflict Resolver: 2 tests
- Quality Control: 5 tests
- Guardian Enhanced: 5 tests
- Integration: 3 tests

---

## 🌍 IDE Integration

Enhanced Guardian works with all major AI coding IDEs:

### Cursor
Files saved to: `.cursor/rules/guardian.mdc`

### Windsurf
Files saved to: `.windsurf/rules/guardian.md`

### GitHub Copilot
Files saved to: `.github/copilot-instructions.md`

### Claude Code
Files saved to: `CLAUDE.md`

---

## 🚧 Migration from v6 to v7

### Automatic Migration

```bash
# v7 reads v6 files automatically
guardian-enhanced
```

### Manual Steps

1. **Backup existing guardian.mdc**
   ```bash
   cp guardian.mdc guardian.mdc.v6.backup
   ```

2. **Run enhanced scan**
   ```bash
   guardian-enhanced
   ```

3. **Lock existing tech decisions**
   ```python
   guardian = GuardianEnhanced(".")
   # Lock your tech stack
   guardian.lock_tech_decision("React", "frontend", "Existing choice", "PERMANENT")
   ```

4. **Review generated file**
   Check `.guardian/` directory and new sections in MDC

---

## 💡 Best Practices

### 1. Lock Critical Decisions Early

```python
# Lock tech stack after initial setup
guardian.lock_tech_decision("React", "frontend", "Team decision", "PERMANENT")
guardian.lock_tech_decision("FastAPI", "backend", "Team decision", "PERMANENT")
guardian.lock_tech_decision("PostgreSQL", "database", "Project requirement", "PERMANENT")
```

### 2. Run Quality Checks Regularly

```bash
# Weekly quality check
guardian-enhanced --output weekly_report.mdc
```

### 3. Monitor Health

```python
health = guardian.memory.get_health_report()

if health['health_score'] < 70:
    print("⚠️ Warning: Project health declining")
    for rec in health['recommendations']:
        print(f"  - {rec}")
```

### 4. Review Changes

```python
# Get recent changes
changes = guardian.memory.get_changes(limit=10)

# Verify important changes
for change in changes:
    if change.verification_status == "unverified":
        # Test the change
        # Then mark as verified
        guardian.memory.verify_change(change.id, "verified")
```

### 5. Start Fresh Sessions

When agent seems "tired" (making repetitive mistakes):

```python
health = guardian.memory.get_health_report()
if health['status'] == 'concerning':
    # Start new chat/session with agent
    # Previous context is preserved in .guardian/
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Credits

Built with ❤️ by [Haitham](https://github.com/Haithamhaj) and the community

Special thanks to all contributors who helped identify and solve the 26 pain points!

---

## 📞 Support

- GitHub Issues: [Report bugs](https://github.com/Haithamhaj/guardian-h/issues)
- Discussions: [Ask questions](https://github.com/Haithamhaj/guardian-h/discussions)
- Twitter: [@Haithamhaj](https://twitter.com/Haithamhaj)

---

Made with 💡 by [Imperfect Success](https://imperfectsuccess.com)
