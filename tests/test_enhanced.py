#!/usr/bin/env python3
"""
🧪 Test Suite for Enhanced Guardian Features
Tests memory management, decision support, and quality control
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from memory_enhanced import (
    EnhancedMemoryManager, DecisionStatus, ChangeType,
    LockedDecision, ChangeRecord, SessionMemory
)
from decision_support import (
    TechnologyAdvisor, ConflictResolver, DecisionLock, TechCategory
)
from quality_control import (
    DeadCodeDetector, DuplicateFinder, StructureEnforcer,
    FileRegistry, QualityController
)
from guardian_enhanced import GuardianEnhanced

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def test_passed(name):
    print(f"{GREEN}✅ PASSED:{RESET} {name}")

def test_failed(name, reason):
    print(f"{RED}❌ FAILED:{RESET} {name}")
    print(f"   Reason: {reason}")

def test_section(name):
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}🧪 {name}{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}\n")


# ============================================================
# Test 1: Enhanced Memory Manager
# ============================================================

def test_memory_manager():
    test_section("Test 1: Enhanced Memory Manager")
    
    passed = 0
    failed = 0
    
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = EnhancedMemoryManager(tmpdir)
        
        # Test 1.1: Lock Decision
        try:
            decision = memory.lock_decision(
                category="tech_stack",
                decision="React as frontend framework",
                reasoning="Team has React expertise",
                status=DecisionStatus.PERMANENT,
                alternatives=["Vue", "Angular"]
            )
            
            if decision and decision.decision == "React as frontend framework":
                test_passed("Lock Decision")
                passed += 1
            else:
                test_failed("Lock Decision", "Decision not locked correctly")
                failed += 1
        except Exception as e:
            test_failed("Lock Decision", str(e))
            failed += 1
        
        # Test 1.2: Check Conflict
        try:
            conflicts = memory.check_decision_conflict("Switch to Vue instead")
            if len(conflicts) > 0:
                test_passed("Conflict Detection")
                passed += 1
            else:
                test_failed("Conflict Detection", "No conflict detected")
                failed += 1
        except Exception as e:
            test_failed("Conflict Detection", str(e))
            failed += 1
        
        # Test 1.3: Log Change
        try:
            change = memory.log_change(
                ChangeType.FILE_CREATED,
                "Created App.jsx",
                ["src/App.jsx"],
                "Initial component"
            )
            
            if change and change.description == "Created App.jsx":
                test_passed("Log Change")
                passed += 1
            else:
                test_failed("Log Change", "Change not logged")
                failed += 1
        except Exception as e:
            test_failed("Log Change", str(e))
            failed += 1
        
        # Test 1.4: Session Tracking
        try:
            session = memory.start_session("cursor")
            memory.update_session(session.session_id, task="Test task")
            
            retrieved = memory.get_session(session.session_id)
            if retrieved and len(retrieved.tasks_completed) == 1:
                test_passed("Session Tracking")
                passed += 1
            else:
                test_failed("Session Tracking", "Session not tracked correctly")
                failed += 1
        except Exception as e:
            test_failed("Session Tracking", str(e))
            failed += 1
        
        # Test 1.5: Health Report
        try:
            health = memory.get_health_report()
            if 'status' in health and 'health_score' in health:
                test_passed("Health Report")
                passed += 1
            else:
                test_failed("Health Report", "Missing health data")
                failed += 1
        except Exception as e:
            test_failed("Health Report", str(e))
            failed += 1
        
        # Test 1.6: Snapshot Creation
        try:
            snapshot_id = memory.create_snapshot(
                {'test': 'data'},
                label="test_snapshot"
            )
            
            snapshot = memory.get_snapshot(snapshot_id)
            if snapshot and snapshot['label'] == "test_snapshot":
                test_passed("Snapshot Creation")
                passed += 1
            else:
                test_failed("Snapshot Creation", "Snapshot not created")
                failed += 1
        except Exception as e:
            test_failed("Snapshot Creation", str(e))
            failed += 1
    
    print(f"\n📊 Memory Manager: {passed} passed, {failed} failed")
    return failed == 0


# ============================================================
# Test 2: Technology Advisor
# ============================================================

def test_tech_advisor():
    test_section("Test 2: Technology Advisor")
    
    passed = 0
    failed = 0
    
    advisor = TechnologyAdvisor()
    
    # Test 2.1: Get Recommendations
    try:
        recs = advisor.get_recommendation(
            TechCategory.FRONTEND_FRAMEWORK,
            "web application",
            "beginner",
            []
        )
        
        if len(recs) > 0:
            test_passed("Get Recommendations")
            passed += 1
        else:
            test_failed("Get Recommendations", "No recommendations returned")
            failed += 1
    except Exception as e:
        test_failed("Get Recommendations", str(e))
        failed += 1
    
    # Test 2.2: Check Compatibility
    try:
        result = advisor.check_compatibility("react", ["vue", "angular"])
        
        if not result['compatible'] and len(result['conflicts']) > 0:
            test_passed("Check Compatibility - Conflict")
            passed += 1
        else:
            test_failed("Check Compatibility - Conflict", "Should detect conflict")
            failed += 1
    except Exception as e:
        test_failed("Check Compatibility - Conflict", str(e))
        failed += 1
    
    # Test 2.3: Check Synergy
    try:
        result = advisor.check_compatibility("tailwind", ["react", "typescript"])
        
        if result['compatible'] and len(result['synergies']) > 0:
            test_passed("Check Compatibility - Synergy")
            passed += 1
        else:
            test_failed("Check Compatibility - Synergy", "Should detect synergy")
            failed += 1
    except Exception as e:
        test_failed("Check Compatibility - Synergy", str(e))
        failed += 1
    
    # Test 2.4: Explain Choice
    try:
        explanation = advisor.explain_choice("react", {})
        
        if "Advantages" in explanation and "Considerations" in explanation:
            test_passed("Explain Choice")
            passed += 1
        else:
            test_failed("Explain Choice", "Incomplete explanation")
            failed += 1
    except Exception as e:
        test_failed("Explain Choice", str(e))
        failed += 1
    
    print(f"\n📊 Tech Advisor: {passed} passed, {failed} failed")
    return failed == 0


# ============================================================
# Test 3: Conflict Resolver
# ============================================================

def test_conflict_resolver():
    test_section("Test 3: Conflict Resolver")
    
    passed = 0
    failed = 0
    
    resolver = ConflictResolver()
    
    # Test 3.1: Detect Decision Conflict
    try:
        existing_decisions = [
            {
                'decision': 'React as frontend framework',
                'reasoning': 'Team expertise',
                'status': 'PERMANENT'
            }
        ]
        
        conflicts = resolver.detect_conflicts(
            "Change to Vue",
            existing_decisions,
            []
        )
        
        if len(conflicts) > 0:
            test_passed("Detect Decision Conflict")
            passed += 1
        else:
            test_failed("Detect Decision Conflict", "No conflict detected")
            failed += 1
    except Exception as e:
        test_failed("Detect Decision Conflict", str(e))
        failed += 1
    
    # Test 3.2: Suggest Resolution
    try:
        from decision_support import DecisionConflict
        
        conflict = DecisionConflict(
            type="technology",
            conflicting_proposals=["Use React", "Use Vue"],
            existing_decision="React",
            severity="critical",
            resolution_suggestion="Test suggestion"
        )
        
        resolution = resolver.suggest_resolution(conflict)
        
        if "CRITICAL CONFLICT" in resolution:
            test_passed("Suggest Resolution")
            passed += 1
        else:
            test_failed("Suggest Resolution", "Resolution not formatted correctly")
            failed += 1
    except Exception as e:
        test_failed("Suggest Resolution", str(e))
        failed += 1
    
    print(f"\n📊 Conflict Resolver: {passed} passed, {failed} failed")
    return failed == 0


# ============================================================
# Test 4: Quality Control
# ============================================================

def test_quality_control():
    test_section("Test 4: Quality Control")
    
    passed = 0
    failed = 0
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        os.makedirs(f"{tmpdir}/src")
        
        # Python file with unused imports (intentional for dead code detection test)
        with open(f"{tmpdir}/src/test.py", 'w') as f:
            f.write("""
import os
import sys

def hello():
    print("Hello")
""")
        
        # Duplicate files
        with open(f"{tmpdir}/src/file1.py", 'w') as f:
            f.write("def test():\n    pass\n")
        
        with open(f"{tmpdir}/src/file2.py", 'w') as f:
            f.write("def test():\n    pass\n")
        
        # Test 4.1: Dead Code Detector
        try:
            detector = DeadCodeDetector(tmpdir)
            findings = detector.scan()
            
            if len(findings) > 0:
                test_passed("Dead Code Detection")
                passed += 1
            else:
                test_failed("Dead Code Detection", "No dead code found")
                failed += 1
        except Exception as e:
            test_failed("Dead Code Detection", str(e))
            failed += 1
        
        # Test 4.2: Duplicate Finder
        try:
            finder = DuplicateFinder(tmpdir)
            duplicates = finder.scan(similarity_threshold=0.9)
            
            if len(duplicates) > 0:
                test_passed("Duplicate Finder")
                passed += 1
            else:
                test_failed("Duplicate Finder", "No duplicates found")
                failed += 1
        except Exception as e:
            test_failed("Duplicate Finder", str(e))
            failed += 1
        
        # Test 4.3: Structure Enforcer
        try:
            enforcer = StructureEnforcer(tmpdir)
            violations = enforcer.scan()
            
            # Should find missing README
            if any(v.violation_type == "missing_documentation" for v in violations):
                test_passed("Structure Enforcer")
                passed += 1
            else:
                test_failed("Structure Enforcer", "Should detect missing README")
                failed += 1
        except Exception as e:
            test_failed("Structure Enforcer", str(e))
            failed += 1
        
        # Test 4.4: File Registry
        try:
            registry = FileRegistry(tmpdir)
            files = registry.scan()
            
            if len(files) >= 3:  # Should find our 3 test files
                test_passed("File Registry")
                passed += 1
            else:
                test_failed("File Registry", f"Only found {len(files)} files")
                failed += 1
        except Exception as e:
            test_failed("File Registry", str(e))
            failed += 1
        
        # Test 4.5: Quality Controller
        try:
            controller = QualityController(tmpdir)
            report = controller.run_full_scan()
            
            if 'summary' in report and 'health_score' in report['summary']:
                test_passed("Quality Controller")
                passed += 1
            else:
                test_failed("Quality Controller", "Incomplete report")
                failed += 1
        except Exception as e:
            test_failed("Quality Controller", str(e))
            failed += 1
    
    print(f"\n📊 Quality Control: {passed} passed, {failed} failed")
    return failed == 0


# ============================================================
# Test 5: Guardian Enhanced Integration
# ============================================================

def test_guardian_enhanced():
    test_section("Test 5: Guardian Enhanced Integration")
    
    passed = 0
    failed = 0
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create minimal project structure
        os.makedirs(f"{tmpdir}/src")
        
        with open(f"{tmpdir}/package.json", 'w') as f:
            json.dump({
                "name": "test-project",
                "dependencies": {"react": "^18.0.0"}
            }, f)
        
        with open(f"{tmpdir}/src/App.jsx", 'w') as f:
            f.write("export function App() { return <div>Test</div>; }")
        
        # Test 5.1: Full Scan
        try:
            guardian = GuardianEnhanced(tmpdir)
            results = guardian.full_scan(run_quality_check=False)
            
            if 'snapshot' in results and 'health' in results:
                test_passed("Full Scan")
                passed += 1
            else:
                test_failed("Full Scan", "Incomplete results")
                failed += 1
        except Exception as e:
            test_failed("Full Scan", str(e))
            failed += 1
        
        # Test 5.2: Lock Decision
        try:
            guardian = GuardianEnhanced(tmpdir)
            result = guardian.lock_tech_decision(
                "React",
                "frontend_framework",
                "Team expertise",
                "PERMANENT"
            )
            
            if result['success']:
                test_passed("Lock Tech Decision")
                passed += 1
            else:
                test_failed("Lock Tech Decision", result.get('message', 'Unknown error'))
                failed += 1
        except Exception as e:
            test_failed("Lock Tech Decision", str(e))
            failed += 1
        
        # Test 5.3: Check Proposal
        try:
            guardian = GuardianEnhanced(tmpdir)
            guardian.lock_tech_decision("React", "frontend", "Test", "PERMANENT")
            
            result = guardian.check_proposal("Switch to Vue")
            
            if result['has_conflicts']:
                test_passed("Check Proposal - Conflict")
                passed += 1
            else:
                test_failed("Check Proposal - Conflict", "Should detect conflict")
                failed += 1
        except Exception as e:
            test_failed("Check Proposal - Conflict", str(e))
            failed += 1
        
        # Test 5.4: Tech Recommendation
        try:
            guardian = GuardianEnhanced(tmpdir)
            result = guardian.get_tech_recommendation(
                "frontend",
                "web application",
                "beginner"
            )
            
            if 'recommendations' in result and len(result['recommendations']) > 0:
                test_passed("Tech Recommendation")
                passed += 1
            else:
                test_failed("Tech Recommendation", "No recommendations")
                failed += 1
        except Exception as e:
            test_failed("Tech Recommendation", str(e))
            failed += 1
        
        # Test 5.5: Generate Enhanced MDC
        try:
            guardian = GuardianEnhanced(tmpdir)
            guardian.scanner.scan()
            
            mdc = guardian.generate_enhanced_mdc()
            
            required_sections = [
                'LOCKED_DECISIONS',
                'CHANGE_HISTORY',
                'HEALTH_STATUS',
                'ENHANCED_AGENT_RULES'
            ]
            
            if all(section in mdc for section in required_sections):
                test_passed("Generate Enhanced MDC")
                passed += 1
            else:
                test_failed("Generate Enhanced MDC", "Missing sections")
                failed += 1
        except Exception as e:
            test_failed("Generate Enhanced MDC", str(e))
            failed += 1
    
    print(f"\n📊 Guardian Enhanced: {passed} passed, {failed} failed")
    return failed == 0


# ============================================================
# Run All Tests
# ============================================================

def main():
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}🛡️ GUARDIAN ENHANCED TEST SUITE{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    results = {
        "Memory Manager": test_memory_manager(),
        "Tech Advisor": test_tech_advisor(),
        "Conflict Resolver": test_conflict_resolver(),
        "Quality Control": test_quality_control(),
        "Guardian Enhanced": test_guardian_enhanced(),
    }
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}📊 FINAL RESULTS{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    all_passed = True
    for name, passed in results.items():
        status = f"{GREEN}✅ PASSED{RESET}" if passed else f"{RED}❌ FAILED{RESET}"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print(f"{GREEN}🎉 All tests passed! Guardian Enhanced is ready.{RESET}")
    else:
        print(f"{RED}⚠️ Some tests failed. Please review.{RESET}")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
