#!/usr/bin/env python3
"""
🛡️ Guardian Enhanced Scanner
Integrates memory management, decision support, quality control, and Mind-Q pipeline support
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from guardian_scanner import GuardianScanner
from memory_enhanced import EnhancedMemoryManager, DecisionStatus, ChangeType
from decision_support import TechnologyAdvisor, ConflictResolver, DecisionLock, TechCategory
from quality_control import QualityController

# Try to import Mind-Q adapter (optional)
try:
    from guardian_mindq import MindQGuardianAdapter
    MINDQ_AVAILABLE = True
except ImportError:
    MINDQ_AVAILABLE = False


class GuardianEnhanced:
    """
    Enhanced Guardian with full memory, decision support, and quality control
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        
        # Initialize all systems
        self.scanner = GuardianScanner(str(self.project_path))
        self.memory = EnhancedMemoryManager(str(self.project_path))
        self.tech_advisor = TechnologyAdvisor()
        self.conflict_resolver = ConflictResolver()
        self.decision_lock = DecisionLock(self.memory)
        self.quality_controller = QualityController(str(self.project_path))
        
        # Initialize Mind-Q adapter if this is a Mind-Q project
        self.mindq_adapter = None
        if MINDQ_AVAILABLE and self._is_mindq_project():
            try:
                self.mindq_adapter = MindQGuardianAdapter(str(self.project_path))
                print("🔧 Mind-Q pipeline detected - enhanced context enabled")
            except Exception as e:
                print(f"⚠️  Mind-Q adapter initialization failed: {e}")
        
        # Session tracking
        self.current_session = None
    
    def _is_mindq_project(self) -> bool:
        """
        Detect if this is a Mind-Q project.
        
        Returns:
            True if Mind-Q project markers are found
        """
        # Check for Mind-Q specific markers
        markers = [
            self.project_path / "phases",
            self.project_path / "docs" / "PHASES_DETAILED_GUIDE.md",
            self.project_path / "contracts",
        ]
        
        # If at least 2 markers exist, consider it Mind-Q
        found_markers = sum(1 for marker in markers if marker.exists())
        return found_markers >= 2
    
    def full_scan(self, run_quality_check: bool = True) -> Dict:
        """
        Run a complete Guardian scan with all features
        """
        print(f"🛡️ Guardian Enhanced Scan: {self.project_path.name}")
        print("=" * 60)
        
        # Start tracking session
        self.current_session = self.memory.start_session(
            agent_type="guardian_scanner"
        )
        
        # 1. Run base scanner
        print("\n📊 Phase 1: Project Analysis...")
        snapshot = self.scanner.scan()
        
        # 2. Run quality checks
        quality_report = None
        if run_quality_check:
            print("\n🔍 Phase 2: Quality Control...")
            quality_report = self.quality_controller.run_full_scan()
        
        # 3. Get health report
        print("\n💊 Phase 3: Health Assessment...")
        health = self.memory.get_health_report()
        
        # 4. Create snapshot
        print("\n📸 Phase 4: Creating Snapshot...")
        snapshot_id = self.memory.create_snapshot(
            snapshot_data=snapshot,
            label="full_scan"
        )
        
        # 5. Update session
        self.memory.update_session(
            self.current_session.session_id,
            task="Full project scan completed",
            context=f"Scanned {len(snapshot['files'])} files"
        )
        
        print("\n✅ Scan Complete!")
        print(f"   Files: {len(snapshot['files'])}")
        print(f"   Health Score: {health['health_score']}/100")
        if quality_report:
            print(f"   Code Health: {quality_report['summary']['health_score']}/100")
        print(f"   Locked Decisions: {len(self.memory.decisions)}")
        
        return {
            'snapshot': snapshot,
            'quality': quality_report,
            'health': health,
            'snapshot_id': snapshot_id,
            'session_id': self.current_session.session_id
        }
    
    def generate_enhanced_mdc(self, scan_results: Optional[Dict] = None) -> str:
        """
        Generate enhanced MDC file with all guardian features
        """
        if not scan_results:
            scan_results = self.full_scan(run_quality_check=False)
        
        snapshot = scan_results['snapshot']
        health = scan_results['health']
        
        # Get base MDC content
        base_mdc = self.scanner.generate_mdc()
        
        # Add enhanced sections
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Build locked decisions section
        locked_decisions_str = ""
        for decision in self.memory.get_locked_decisions():
            locked_decisions_str += f"""
  - category: {decision.category}
    decision: {decision.decision}
    status: {decision.status.value}
    reasoning: {decision.reasoning}
    locked_at: {decision.locked_at}
"""
        
        # Build recent changes section
        changes_str = ""
        for change in self.memory.get_changes(limit=10):
            changes_str += f"""
  - timestamp: {change.timestamp}
    type: {change.change_type.value}
    description: {change.description}
    verification: {change.verification_status}
"""
        
        # Build health section
        health_str = f"""
status: {health['status']}
score: {health['health_score']}/100
locked_decisions: {health['locked_decisions']}
total_changes: {health['total_changes']}
unverified_changes: {health['unverified_changes']}
active_sessions: {health['active_sessions']}
"""
        
        # Build recommendations
        recommendations_str = ""
        if health['recommendations']:
            for rec in health['recommendations']:
                recommendations_str += f"  - {rec}\n"
        else:
            recommendations_str = "  - All systems healthy ✅\n"
        
        # Add quality report if available
        quality_str = ""
        if 'quality' in scan_results and scan_results['quality']:
            quality = scan_results['quality']
            quality_str = f"""

---

## 🔍 QUALITY_REPORT
```yaml
code_health: {quality['summary']['health_score']}/100
total_files: {quality['file_registry']['total_files']}
active_files: {quality['file_registry']['active_files']}
dead_code_findings: {quality['dead_code']['findings_count']}
duplicate_files: {quality['duplicates']['count']}
structure_violations: {quality['structure']['violations_count']}
```
"""
        
        # Add Mind-Q context if available
        mindq_context = ""
        if self.mindq_adapter:
            try:
                mindq_context = self.mindq_adapter.get_mindq_context_for_mdc()
            except Exception as e:
                print(f"⚠️  Failed to generate Mind-Q context: {e}")
                mindq_context = ""
        
        # Enhanced MDC with all sections
        enhanced_mdc = f"""{base_mdc}

---

## 🔒 LOCKED_DECISIONS
> ⛔ CANNOT CHANGE WITHOUT EXPLICIT APPROVAL
```yaml
{locked_decisions_str if locked_decisions_str else '  # No locked decisions yet\n  # Use this to lock important technical choices'}
```

---

## 📝 CHANGE_HISTORY
> 📋 Last 10 changes
```yaml
{changes_str if changes_str else '  - No changes recorded yet'}
```

---

## 💊 HEALTH_STATUS
```yaml
{health_str}
```

---

## 💡 RECOMMENDATIONS
```yaml
{recommendations_str}
```
{quality_str}

---

{mindq_context}

---

## 🤖 ENHANCED_AGENT_RULES

### 🛡️ Guardian Protection Layer

**Before ANY Code Change:**
```
1. ✅ Check LOCKED_DECISIONS - am I violating any?
2. ✅ Check CHANGE_HISTORY - similar change attempted before?
3. ✅ Check HEALTH_STATUS - is system in good state?
4. ✅ If proposing tech change - check compatibility
```

**When Agent Suggests Technology:**
```
1. ✅ Check if conflicts with LOCKED_DECISIONS
2. ✅ Ask: "Does this work well with current TECH_STACK?"
3. ✅ Require explicit approval for major tech changes
4. ✅ Document reasoning for the choice
```

**When Creating Files:**
```
1. ✅ Check FILES section for similar files
2. ✅ Check QUALITY_REPORT for duplicates
3. ✅ Follow naming conventions from existing files
4. ✅ Ask user if similar file exists: "Use existing or create new?"
```

**After Making Changes:**
```
1. ✅ Test the change immediately
2. ✅ Update CHANGE_HISTORY with what was done
3. ✅ Show proof (output, screenshot, log)
4. ✅ Mark change as verified or failed
```

**If Agent Gets Confused:**
```
❌ DON'T: Guess or assume
❌ DON'T: Make conflicting suggestions
❌ DON'T: Change locked decisions
✅ DO: Ask user for clarification
✅ DO: Reference this Guardian file
✅ DO: Explain the conflict clearly
```

### 🚨 Red Flags (Stop and Ask User)

```
⛔ Suggesting technology that conflicts with TECH_STACK
⛔ Trying to change LOCKED_DECISIONS
⛔ Creating file similar to existing ones
⛔ Making change that failed before (check CHANGE_HISTORY)
⛔ Multiple agents gave different advice
⛔ Health score is low (< 70)
⛔ Many unverified changes
```

---

## 📊 SESSION_INFO
```yaml
session_id: {scan_results.get('session_id', 'unknown')}
snapshot_id: {scan_results.get('snapshot_id', 'unknown')}
generated_at: {timestamp}
guardian_version: enhanced_v1.0
```

---

*🛡️ Protected by Guardian Enhanced - Your AI Agent's Memory & Decision Support System*
"""
        
        return enhanced_mdc
    
    def lock_tech_decision(
        self,
        tech_name: str,
        category: str,
        reasoning: str,
        status: str = "PERMANENT"
    ) -> Dict:
        """
        Lock a technology decision
        """
        result = self.decision_lock.request_lock(
            category=category,
            decision=f"{tech_name} as {category}",
            reasoning=reasoning,
            status=status
        )
        
        if result['success']:
            # Log the change
            self.memory.log_change(
                ChangeType.DECISION_LOCKED,
                f"Locked: {tech_name}",
                [],
                reasoning
            )
        
        return result
    
    def check_proposal(self, proposal: str) -> Dict:
        """
        Check if a proposal conflicts with locked decisions
        """
        # Check decision conflicts
        conflicts = self.memory.check_decision_conflict(proposal)
        
        # Get tech advisor opinion if it's about technology
        tech_opinion = None
        proposal_lower = proposal.lower()
        
        # Check if proposal mentions any known technology
        for tech_name in self.tech_advisor.TECH_DB.keys():
            if tech_name in proposal_lower:
                # Extract current stack from snapshot
                current_stack = []
                if hasattr(self.scanner, 'snapshot'):
                    tech_stack = self.scanner.snapshot.get('tech_stack', {})
                    current_stack = list(tech_stack.values())
                
                tech_opinion = self.tech_advisor.check_compatibility(
                    tech_name,
                    current_stack
                )
                break
        
        return {
            'has_conflicts': len(conflicts) > 0,
            'conflicts': [
                {
                    'decision': c.decision,
                    'reasoning': c.reasoning,
                    'status': c.status.value
                }
                for c in conflicts
            ],
            'tech_opinion': tech_opinion,
            'recommendation': self._generate_recommendation(conflicts, tech_opinion)
        }
    
    def _generate_recommendation(self, conflicts, tech_opinion) -> str:
        """Generate recommendation based on conflicts and tech opinion"""
        if conflicts:
            return f"⛔ Cannot proceed - conflicts with {len(conflicts)} locked decision(s). Unlock them first."
        
        if tech_opinion and not tech_opinion['compatible']:
            return f"⚠️ {tech_opinion['message']}"
        
        if tech_opinion and tech_opinion['synergies']:
            return f"✅ {tech_opinion['message']}"
        
        return "✅ No conflicts detected. Safe to proceed."
    
    def get_tech_recommendation(
        self,
        category: str,
        project_type: str = "web application",
        team_experience: str = "beginner"
    ) -> Dict:
        """
        Get technology recommendations
        """
        # Map category string to TechCategory enum
        category_map = {
            'frontend': TechCategory.FRONTEND_FRAMEWORK,
            'backend': TechCategory.BACKEND_FRAMEWORK,
            'database': TechCategory.DATABASE,
            'styling': TechCategory.STYLING,
        }
        
        tech_category = category_map.get(category.lower())
        if not tech_category:
            return {
                'error': f"Unknown category: {category}",
                'available_categories': list(category_map.keys())
            }
        
        # Get current stack
        current_stack = []
        if hasattr(self.scanner, 'snapshot'):
            tech_stack = self.scanner.snapshot.get('tech_stack', {})
            current_stack = list(tech_stack.values())
        
        # Get recommendations
        recommendations = self.tech_advisor.get_recommendation(
            tech_category,
            project_type,
            team_experience,
            current_stack
        )
        
        return {
            'category': category,
            'recommendations': [
                {
                    'name': tech.name,
                    'score': score,
                    'learning_curve': tech.learning_curve,
                    'pros': tech.pros[:3],  # Top 3
                    'best_for': tech.best_for
                }
                for tech, score in recommendations[:5]  # Top 5
            ]
        }
    
    def save_enhanced(self, output_path: Optional[str] = None) -> str:
        """
        Save enhanced guardian file
        """
        if output_path is None:
            output_path = self.project_path / 'guardian_enhanced.mdc'
        else:
            output_path = Path(output_path)
        
        # Run full scan
        scan_results = self.full_scan()
        
        # Generate enhanced MDC
        content = self.generate_enhanced_mdc(scan_results)
        
        # Save compact MDC
        output_path.write_text(content)
        print(f"\n✅ Enhanced Guardian saved: {output_path}")
        
        # Save full file index separately (not for LLM context)
        guardian_dir = self.project_path / '.guardian'
        self.scanner.save_file_index(guardian_dir)
        
        # Also save to IDE-specific locations
        self._save_to_ide_locations(content)
        
        return str(output_path)
    
    def _save_to_ide_locations(self, content: str):
        """Save to IDE-specific locations"""
        ide_locations = [
            '.cursor/rules/guardian.mdc',
            '.windsurf/rules/guardian.md',
            '.github/copilot-instructions.md',
            'CLAUDE.md'
        ]
        
        for location in ide_locations:
            location_path = self.project_path / location
            location_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                location_path.write_text(content)
                print(f"   📁 Saved to: {location}")
            except Exception as e:
                print(f"   ⚠️ Could not save to {location}: {e}")


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🛡️ Guardian Enhanced - Advanced AI Memory & Decision Support'
    )
    parser.add_argument(
        'project_path',
        nargs='?',
        default='.',
        help='Path to project root (default: current directory)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output path for guardian file'
    )
    parser.add_argument(
        '--no-quality',
        action='store_true',
        help='Skip quality control scan (faster)'
    )
    parser.add_argument(
        '--lock-decision',
        nargs=3,
        metavar=('TECH', 'CATEGORY', 'REASONING'),
        help='Lock a technology decision'
    )
    parser.add_argument(
        '--check-proposal',
        help='Check if a proposal conflicts with locked decisions'
    )
    
    args = parser.parse_args()
    
    # Initialize Guardian
    guardian = GuardianEnhanced(args.project_path)
    
    # Handle different commands
    if args.lock_decision:
        tech, category, reasoning = args.lock_decision
        result = guardian.lock_tech_decision(tech, category, reasoning)
        print(f"\n{result['message']}")
        return 0 if result['success'] else 1
    
    if args.check_proposal:
        result = guardian.check_proposal(args.check_proposal)
        print(f"\n{result['recommendation']}")
        if result['tech_opinion']:
            print(f"\nTech Opinion: {result['tech_opinion']['message']}")
        return 0 if not result['has_conflicts'] else 1
    
    # Default: full scan and save
    output_path = guardian.save_enhanced(args.output)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
