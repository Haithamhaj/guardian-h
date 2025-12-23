<div align="center">

# 🛡️ Guardian-H

### Advanced AI Agent Memory & Decision Support System
### نظام متقدم للذاكرة ودعم القرارات للوكلاء الذكيين

<img src="assets/logo.png" alt="Guardian-H Logo" width="200"/>

**It remembers everything. It prevents conflicts. It maintains quality.**

**يتذكر كل شيء. يمنع التعارضات. يحافظ على الجودة.**

[![npm version](https://img.shields.io/npm/v/guardian-h.svg)](https://www.npmjs.com/package/guardian-h)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[🌐 Web Generator](https://haithamhaj.github.io/guardian-h/) | [📚 Enhanced Guide](docs/ENHANCED_GUIDE.md) | [🇸🇦 الدليل العربي](docs/ENHANCED_GUIDE_AR.md)

</div>

---

## 🚀 What's New in v7.0

🎯 **Solving the 26 Pain Points of Working with AI Agents**

| Feature | Description |
|---------|-------------|
| 🧠 **Enhanced Memory** | Persistent decisions, session tracking, change history |
| 🎯 **Decision Support** | Technology recommendations, conflict detection, decision locking |
| 🔍 **Quality Control** | Dead code detection, duplicate finder, structure enforcement |
| 💊 **Health Monitoring** | Real-time project health, agent fatigue detection |
| 📊 **Session Management** | Track agent sessions, context preservation |
| 🔒 **Decision Locking** | Prevent agents from changing locked technical choices |
| 📝 **Change Verification** | Track and verify all changes made by agents |
| 🗺️ **Project Snapshots** | Versioned snapshots for rollback support |
| 🎯 **Mind-Q Adapter** | NEW! Specialized adapter for data pipeline projects |

### 🆕 Mind-Q Guardian Adapter

Specialized extension for **Mind-Q V4.1** logistics data pipelines:

- **Pipeline Spine**: Auto-generates pipeline structure (21 phases, KPIs, flows)
- **Phase Cards**: Compact markdown cards for each pipeline stage
- **Context Optimization**: 94% reduction in context size for LLMs
- **Smart Context**: Auto-detects relevant phases from user requests

[📖 Mind-Q Guardian Guide](docs/MINDQ_GUARDIAN_GUIDE.md)

[📖 Read the Complete v7.0 Guide](docs/ENHANCED_GUIDE.md) | [📖 اقرأ الدليل الكامل](docs/ENHANCED_GUIDE_AR.md)

---

## 😤 The Problem

You're building with AI agents (Cursor, Windsurf, Copilot, Claude) and this keeps happening:

```
You: "Change the button color"
Agent: Creates 3 new files, refactors everything

You: "Fix the login bug"  
Agent: Uses port 3000 (yours is 8765)

You: "Add a toast message"
Agent: Suggests Vue (you use React)

You: "Why did you change React to Vue?"
Agent: "I forgot we agreed on React"
```

**Result:** Hours wasted. Code breaks. Frustration builds.

---

## 💡 The Solution

**Guardian v7.0 creates a comprehensive memory & decision support system.**

```
✅ Remembers locked decisions across sessions
✅ Detects conflicts before they happen
✅ Prevents duplicate files and dead code
✅ Tracks agent health and fatigue
✅ Maintains project quality automatically
✅ Provides technology recommendations
✅ Preserves context between conversations
```

### 🎯 How It Works

1. **Scan & Remember**: Analyzes your project and creates persistent memory
2. **Lock Decisions**: Lock critical technical choices (React, FastAPI, etc.)
3. **Guard Changes**: Prevents agents from violating locked decisions
4. **Track Health**: Monitors code quality and agent behavior
5. **Verify Changes**: All changes logged and can be verified
6. **Stay Consistent**: Agents read the same context every time

---

## 🚀 Quick Start

### ⚡ For Basic Features (JavaScript)
```bash
npx guardian-h
```

### 🧠 For Full Features (Enhanced)
```bash
# Requires Python 3.7+
npx guardian-enhanced

# Or install globally
npm install -g guardian-h
guardian-enhanced
```

### Lock Your First Decision
```bash
# Lock React as your framework
guardian-enhanced --lock-decision React frontend_framework "Team has React expertise"
```

---

## 🚀 Installation (Choose Your Method)

### ⚡ Method 1: npx (Recommended)
```bash
npx guardian-h
```
**Requirements:** Node.js

---

### 🐧 Method 2: Bash Script (No Node.js needed!)
```bash
curl -sL https://raw.githubusercontent.com/Haithamhaj/guardian-h/main/install.sh | bash
```
**Requirements:** Terminal only (Mac/Linux)

---

### 🌐 Method 3: Web Generator (No installation!)

**[👉 Open Web Generator](https://haithamhaj.github.io/guardian-h/)**

1. Fill in your project info
2. Download the file
3. Place it in your IDE's rules folder

**Requirements:** Just a browser!

---

## 📁 What It Creates

Guardian generates a compact, AI-optimized snapshot:

```yaml
# 🛡️ my-project GUARDIAN

## 📋 RULES (Decision Table)
| Action | Check | Do |
|--------|-------|-----|
| Create file | FILES has similar? | → ASK user first |
| Modify file | In DANGER? | → WARN before proceed |
| Change config | In LOCKED? | → STOP, ask approval |

## 🏗️ TECH_STACK
frontend: React
backend: FastAPI
database: SQLite

## 📂 FILES
src/App.jsx: main-app
api/main.py: server-entry

## 🧠 THINKING
problem_solving:
  1: Read error → Trace flow → Find root cause
  2: One change → Test → Confirm → Show proof
```

---

## 🤖 IDE Support

| IDE | File Location | Auto-detected |
|-----|---------------|---------------|
| **Cursor** | `.cursor/rules/guardian.mdc` | ✅ |
| **Windsurf** | `.windsurf/rules/guardian.md` | ✅ |
| **VS Code + Copilot** | `.github/copilot-instructions.md` | ✅ |
| **Claude Code** | `CLAUDE.md` | ✅ |
| **Other** | `guardian.mdc` (root) | - |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [WORKFLOW.md](docs/WORKFLOW.md) | 5-phase problem-solving workflow |
| [CODE_PRINCIPLES.md](docs/CODE_PRINCIPLES.md) | 18+ code quality principles |
| [THINKING_PATTERNS.md](docs/THINKING_PATTERNS.md) | 12 thinking patterns for debugging |
| [INSTALL.md](INSTALL.md) | Detailed installation guide |
| [FAQ.md](docs/FAQ.md) | Frequently asked questions |

---

## 🔌 MCP Server (Advanced)

Guardian includes a Model Context Protocol server for deep integration:

```json
{
  "guardian": {
    "command": "python3",
    "args": ["/path/to/src/guardian_mcp.py"]
  }
}
```

**Available Tools:**
- `guardian_read_memory` - Read project context
- `guardian_classify_change` - Classify change type
- `guardian_get_tech_stack` - Get tech stack
- `guardian_get_file_map` - Get file structure
- `guardian_log_change` - Log changes

---

## 🔄 Updating

Re-scan your project after major changes:

```bash
# Using npx
npx guardian-h

# Using Bash
curl -sL https://raw.githubusercontent.com/Haithamhaj/guardian-h/main/install.sh | bash
```

---

<a name="arabic"></a>
# 🇸🇦 التوثيق العربي

## 🌟 الجديد في الإصدار 6.1

| الميزة | الوصف |
|--------|-------|
| ✅ **لا يحتاج Python** | ماسح JavaScript نقي - يعمل في أي مكان |
| 🌐 **3 طرق للتثبيت** | npx أو Bash أو صفحة ويب |
| 🧠 **قواعد تفكير الوكيل** | إرشادات مدمجة لقرارات أفضل |
| 📐 **مبادئ الكود** | 18+ مبدأ للأداء والتطوير والبساطة |
| 🔌 **خادم MCP** | تكامل مع Model Context Protocol |

---

## 🚀 التثبيت

### ⚡ الطريقة 1: npx (الموصى بها)
```bash
npx guardian-h
```

### 🐧 الطريقة 2: سكربت Bash (لا يحتاج Node.js!)
```bash
curl -sL https://raw.githubusercontent.com/Haithamhaj/guardian-h/main/install.sh | bash
```

### 🌐 الطريقة 3: مولد الويب (لا يحتاج تثبيت!)

**[👉 افتح مولد الويب](https://haithamhaj.github.io/guardian-h/)**

---

## 📚 التوثيق

| الملف | الوصف |
|-------|-------|
| [WORKFLOW.md](docs/WORKFLOW.md) | سير عمل حل المشكلات |
| [CODE_PRINCIPLES.md](docs/CODE_PRINCIPLES.md) | مبادئ جودة الكود |
| [THINKING_PATTERNS.md](docs/THINKING_PATTERNS.md) | أنماط التفكير للتصحيح |
| [INSTALL.md](INSTALL.md) | دليل التثبيت التفصيلي |

---

<div align="center">

## 🤝 Contributing | المساهمة

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License | الرخصة

MIT - Use it, modify it, ship it.

---

## ⭐ Star History

If Guardian-H helps you, give it a ⭐!

إذا ساعدك Guardian-H، أعطه ⭐!

---

**🛡️ Guardian-H v6.1**

*Discover. Remember. Protect.*

*اكتشف. تذكّر. احمِ.*

---

<img src="https://img.shields.io/badge/Made%20with-❤️-red.svg" alt="Made with love"/>

**A Product by [Imperfect Success](https://imperfectsuccess.com)**

</div>
