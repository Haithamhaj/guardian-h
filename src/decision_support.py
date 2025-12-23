#!/usr/bin/env python3
"""
🎯 Decision Support System
Helps non-technical users make better technology choices and avoid conflicts
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TechCategory(Enum):
    """Categories of technology decisions"""
    FRONTEND_FRAMEWORK = "frontend_framework"
    BACKEND_FRAMEWORK = "backend_framework"
    DATABASE = "database"
    STYLING = "styling"
    STATE_MANAGEMENT = "state_management"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    AUTHENTICATION = "authentication"


@dataclass
class TechnologyOption:
    """Represents a technology choice"""
    name: str
    category: TechCategory
    pros: List[str]
    cons: List[str]
    best_for: List[str]
    learning_curve: str  # "easy", "medium", "hard"
    popularity_score: int  # 1-10
    conflicts_with: List[str]
    works_well_with: List[str]


@dataclass
class DecisionConflict:
    """Represents a conflict between proposals"""
    type: str  # "technology", "pattern", "architecture"
    conflicting_proposals: List[str]
    existing_decision: Optional[str]
    severity: str  # "critical", "warning", "info"
    resolution_suggestion: str


class TechnologyAdvisor:
    """
    Provides guidance on technology choices
    Based on project type, team skills, and current stack
    """
    
    # Technology knowledge base
    TECH_DB = {
        "react": TechnologyOption(
            name="React",
            category=TechCategory.FRONTEND_FRAMEWORK,
            pros=[
                "Large ecosystem and community",
                "Component reusability",
                "Virtual DOM for performance",
                "Backed by Meta (Facebook)"
            ],
            cons=[
                "Requires additional libraries for full solution",
                "JSX learning curve",
                "Frequent updates"
            ],
            best_for=["Large applications", "Teams", "Complex UIs"],
            learning_curve="medium",
            popularity_score=10,
            conflicts_with=["vue", "svelte", "angular"],
            works_well_with=["typescript", "tailwind", "next.js"]
        ),
        "vue": TechnologyOption(
            name="Vue",
            category=TechCategory.FRONTEND_FRAMEWORK,
            pros=[
                "Gentle learning curve",
                "Great documentation",
                "Progressive framework",
                "Small bundle size"
            ],
            cons=[
                "Smaller ecosystem than React",
                "Less corporate backing",
                "Fewer job opportunities"
            ],
            best_for=["Small to medium projects", "Solo developers", "Quick prototypes"],
            learning_curve="easy",
            popularity_score=8,
            conflicts_with=["react", "svelte", "angular"],
            works_well_with=["typescript", "tailwind", "nuxt"]
        ),
        "fastapi": TechnologyOption(
            name="FastAPI",
            category=TechCategory.BACKEND_FRAMEWORK,
            pros=[
                "Modern Python framework",
                "Automatic API documentation",
                "Type hints and validation",
                "High performance"
            ],
            cons=[
                "Relatively new",
                "Smaller community than Django",
                "Async can be complex"
            ],
            best_for=["APIs", "Microservices", "Modern Python projects"],
            learning_curve="medium",
            popularity_score=9,
            conflicts_with=["django", "flask"],
            works_well_with=["pydantic", "sqlalchemy", "postgresql"]
        ),
        "django": TechnologyOption(
            name="Django",
            category=TechCategory.BACKEND_FRAMEWORK,
            pros=[
                "Batteries included",
                "Excellent ORM",
                "Admin panel",
                "Mature and stable"
            ],
            cons=[
                "Monolithic approach",
                "Slower for simple APIs",
                "Learning curve for beginners"
            ],
            best_for=["Full web applications", "Content management", "E-commerce"],
            learning_curve="medium",
            popularity_score=9,
            conflicts_with=["fastapi", "flask"],
            works_well_with=["postgresql", "redis", "celery"]
        ),
        "tailwind": TechnologyOption(
            name="Tailwind CSS",
            category=TechCategory.STYLING,
            pros=[
                "Utility-first approach",
                "Highly customizable",
                "No CSS file conflicts",
                "Great developer experience"
            ],
            cons=[
                "HTML can look cluttered",
                "Initial setup needed",
                "Learning new paradigm"
            ],
            best_for=["Modern web apps", "Rapid prototyping", "Component-based"],
            learning_curve="easy",
            popularity_score=10,
            conflicts_with=["bootstrap", "material-ui"],
            works_well_with=["react", "vue", "next.js"]
        ),
        "electron": TechnologyOption(
            name="Electron",
            category=TechCategory.DEPLOYMENT,
            pros=[
                "Cross-platform desktop apps",
                "Use web technologies",
                "Large ecosystem",
                "Easy distribution"
            ],
            cons=[
                "Large bundle size",
                "High memory usage",
                "Slower than native"
            ],
            best_for=["Desktop applications", "Cross-platform tools", "Web to desktop"],
            learning_curve="medium",
            popularity_score=8,
            conflicts_with=["tauri"],
            works_well_with=["react", "vue", "typescript"]
        )
    }
    
    def get_recommendation(
        self,
        category: TechCategory,
        project_type: str,
        team_experience: str = "beginner",
        current_stack: List[str] = None
    ) -> List[Tuple[TechnologyOption, float]]:
        """
        Get technology recommendations based on context
        Returns list of (TechnologyOption, score) tuples sorted by score
        """
        current_stack = current_stack or []
        recommendations = []
        
        # Get all options in category
        options = [
            tech for tech in self.TECH_DB.values()
            if tech.category == category
        ]
        
        for option in options:
            score = self._calculate_score(
                option, project_type, team_experience, current_stack
            )
            recommendations.append((option, score))
        
        # Sort by score
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations
    
    def _calculate_score(
        self,
        option: TechnologyOption,
        project_type: str,
        team_experience: str,
        current_stack: List[str]
    ) -> float:
        """Calculate recommendation score for a technology"""
        score = option.popularity_score * 10  # Base score from popularity
        
        # Adjust for learning curve
        if team_experience == "beginner":
            if option.learning_curve == "easy":
                score += 20
            elif option.learning_curve == "hard":
                score -= 20
        elif team_experience == "expert":
            # Experts can handle complexity
            score += 10
        
        # Adjust for project fit
        project_type_lower = project_type.lower()
        for best_fit in option.best_for:
            if best_fit.lower() in project_type_lower:
                score += 15
        
        # Bonus for compatibility with current stack
        for tech in current_stack:
            tech_lower = tech.lower()
            for compatible in option.works_well_with:
                if compatible.lower() in tech_lower:
                    score += 10
        
        # Penalty for conflicts with current stack
        for tech in current_stack:
            tech_lower = tech.lower()
            for conflict in option.conflicts_with:
                if conflict.lower() in tech_lower:
                    score -= 50  # Heavy penalty for conflicts
        
        return score
    
    def explain_choice(
        self,
        tech_name: str,
        project_context: Dict
    ) -> str:
        """Generate explanation for why a technology was recommended"""
        tech_lower = tech_name.lower()
        
        if tech_lower not in self.TECH_DB:
            return f"No information available for {tech_name}"
        
        option = self.TECH_DB[tech_lower]
        
        explanation = f"""
# Why {option.name}?

## ✅ Advantages:
{self._format_list(option.pros)}

## ⚠️ Considerations:
{self._format_list(option.cons)}

## 🎯 Best suited for:
{self._format_list(option.best_for)}

## 📚 Learning curve: {option.learning_curve.title()}

## 🔗 Works well with:
{self._format_list(option.works_well_with)}

## ⚔️ Conflicts with:
{self._format_list(option.conflicts_with)}
"""
        return explanation
    
    def _format_list(self, items: List[str]) -> str:
        """Format a list as markdown bullet points"""
        if not items:
            return "- None"
        return "\n".join(f"- {item}" for item in items)
    
    def check_compatibility(
        self,
        new_tech: str,
        current_stack: List[str]
    ) -> Dict:
        """Check if a new technology is compatible with current stack"""
        new_tech_lower = new_tech.lower()
        
        if new_tech_lower not in self.TECH_DB:
            return {
                'compatible': None,
                'message': f"Unknown technology: {new_tech}",
                'conflicts': [],
                'synergies': []
            }
        
        option = self.TECH_DB[new_tech_lower]
        conflicts = []
        synergies = []
        
        for tech in current_stack:
            tech_lower = tech.lower()
            
            # Check conflicts
            if any(c.lower() in tech_lower for c in option.conflicts_with):
                conflicts.append(tech)
            
            # Check synergies
            if any(s.lower() in tech_lower for s in option.works_well_with):
                synergies.append(tech)
        
        compatible = len(conflicts) == 0
        
        if conflicts:
            message = f"⚠️ {new_tech} conflicts with: {', '.join(conflicts)}"
        elif synergies:
            message = f"✅ {new_tech} works great with: {', '.join(synergies)}"
        else:
            message = f"✅ {new_tech} is compatible with your stack"
        
        return {
            'compatible': compatible,
            'message': message,
            'conflicts': conflicts,
            'synergies': synergies
        }


class ConflictResolver:
    """
    Detects and resolves conflicts in agent proposals
    """
    
    def detect_conflicts(
        self,
        new_proposal: str,
        existing_decisions: List[Dict],
        current_conversation: List[Dict]
    ) -> List[DecisionConflict]:
        """
        Detect conflicts between new proposal and existing decisions/conversations
        """
        conflicts = []
        
        # Check against existing decisions
        for decision in existing_decisions:
            conflict = self._check_decision_conflict(new_proposal, decision)
            if conflict:
                conflicts.append(conflict)
        
        # Check for internal contradictions in conversation
        contradiction = self._check_conversation_contradiction(
            new_proposal, current_conversation
        )
        if contradiction:
            conflicts.append(contradiction)
        
        return conflicts
    
    def _check_decision_conflict(
        self,
        proposal: str,
        decision: Dict
    ) -> Optional[DecisionConflict]:
        """Check if proposal conflicts with existing decision"""
        proposal_lower = proposal.lower()
        decision_text = decision.get('decision', '').lower()
        
        # Keywords indicating a change attempt
        change_words = [
            'change', 'switch', 'replace', 'use instead', 'migrate to',
            'تغيير', 'استبدال', 'تحويل', 'استخدام بدلا', 'to vue', 'to angular'
        ]
        
        # Extract technology names from the decision
        tech_keywords = ['react', 'vue', 'angular', 'svelte', 'django', 'flask', 'fastapi',
                        'tailwind', 'bootstrap', 'electron', 'next', 'nuxt']
        
        decision_tech = None
        for tech in tech_keywords:
            if tech in decision_text:
                decision_tech = tech
                break
        
        # Check if proposal tries to change the decision
        has_change_word = any(word in proposal_lower for word in change_words)
        
        if has_change_word:
            # Check if the decision technology is mentioned in context
            decision_words = decision_text.split()
            if any(word in proposal_lower for word in decision_words if len(word) > 3):
                return DecisionConflict(
                    type="technology",
                    conflicting_proposals=[proposal],
                    existing_decision=decision.get('decision'),
                    severity="critical",
                    resolution_suggestion=f"This conflicts with locked decision: {decision.get('decision')}. "
                                        f"Reason: {decision.get('reasoning', 'Not specified')}. "
                                        f"If you want to change this, please unlock the decision first."
                )
        
        # Also check if proposal suggests conflicting technology
        if decision_tech:
            # Get conflicting technologies
            conflicts_map = {
                'react': ['vue', 'angular', 'svelte'],
                'vue': ['react', 'angular', 'svelte'],
                'django': ['flask', 'fastapi'],
                'fastapi': ['django', 'flask'],
                'tailwind': ['bootstrap']
            }
            
            if decision_tech in conflicts_map:
                for conflict_tech in conflicts_map[decision_tech]:
                    if conflict_tech in proposal_lower:
                        return DecisionConflict(
                            type="technology",
                            conflicting_proposals=[proposal],
                            existing_decision=decision.get('decision'),
                            severity="critical",
                            resolution_suggestion=f"Proposal suggests {conflict_tech} but {decision_tech} is locked. "
                                                f"Reason: {decision.get('reasoning', 'Not specified')}. "
                                                f"Cannot use both {decision_tech} and {conflict_tech} together."
                        )
        
        return None
    
    def _check_conversation_contradiction(
        self,
        new_proposal: str,
        conversation: List[Dict]
    ) -> Optional[DecisionConflict]:
        """Check for contradictions within the same conversation"""
        # Extract technology mentions from conversation
        tech_mentions = []
        
        for msg in conversation:
            content = msg.get('content', '').lower()
            
            # Look for framework mentions
            frameworks = ['react', 'vue', 'svelte', 'angular', 'django', 'flask', 'fastapi']
            for fw in frameworks:
                if fw in content:
                    tech_mentions.append({
                        'tech': fw,
                        'message': msg.get('content', '')[:100]
                    })
        
        # Check if new proposal contradicts previous mentions
        new_lower = new_proposal.lower()
        
        for mention in tech_mentions:
            # If new proposal mentions a different framework in the same category
            if mention['tech'] not in new_lower:
                # Check if new proposal mentions a conflicting tech
                conflicting = {
                    'react': ['vue', 'svelte', 'angular'],
                    'vue': ['react', 'svelte', 'angular'],
                    'django': ['flask', 'fastapi'],
                    'flask': ['django', 'fastapi'],
                    'fastapi': ['django', 'flask']
                }
                
                if mention['tech'] in conflicting:
                    for conflict_tech in conflicting[mention['tech']]:
                        if conflict_tech in new_lower:
                            return DecisionConflict(
                                type="technology",
                                conflicting_proposals=[new_proposal, mention['message']],
                                existing_decision=None,
                                severity="warning",
                                resolution_suggestion=f"Earlier in conversation, {mention['tech']} was mentioned. "
                                                    f"Now suggesting {conflict_tech}. Which one should we use?"
                            )
        
        return None
    
    def suggest_resolution(self, conflict: DecisionConflict) -> str:
        """Suggest how to resolve a conflict"""
        if conflict.severity == "critical":
            return f"""
🚨 CRITICAL CONFLICT DETECTED

{conflict.resolution_suggestion}

**Action Required:**
1. Review the locked decision
2. If change is necessary, unlock the decision first
3. Document the reason for the change
4. Update all affected files
"""
        
        elif conflict.severity == "warning":
            return f"""
⚠️ POTENTIAL CONFLICT

{conflict.resolution_suggestion}

**Recommendation:**
1. Clarify which technology to use
2. Stick with one choice consistently
3. Update all related code to use the chosen technology
"""
        
        else:
            return f"""
ℹ️ INFORMATION

{conflict.resolution_suggestion}

**Note:** This is informational and may not require action.
"""


class DecisionLock:
    """
    Manages locking and unlocking of decisions with approval workflow
    """
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
    
    def request_lock(
        self,
        category: str,
        decision: str,
        reasoning: str,
        status: str = "PERMANENT"
    ) -> Dict:
        """Request to lock a decision"""
        from memory_enhanced import DecisionStatus
        
        # Validate inputs
        if not decision or not reasoning:
            return {
                'success': False,
                'message': 'Decision and reasoning are required'
            }
        
        # Check if already locked
        existing = self.memory.get_locked_decisions(category)
        for dec in existing:
            if dec.decision.lower() == decision.lower():
                return {
                    'success': False,
                    'message': f'Decision already locked: {dec.decision}',
                    'existing_decision': dec
                }
        
        # Lock the decision
        status_map = {
            'PERMANENT': DecisionStatus.PERMANENT,
            'CONDITIONAL': DecisionStatus.CONDITIONAL,
            'TEMPORARY': DecisionStatus.TEMPORARY,
            'REVIEW': DecisionStatus.REVIEW
        }
        
        locked = self.memory.lock_decision(
            category=category,
            decision=decision,
            reasoning=reasoning,
            status=status_map.get(status, DecisionStatus.PERMANENT)
        )
        
        return {
            'success': True,
            'message': f'Decision locked: {decision}',
            'decision': locked
        }
    
    def request_unlock(
        self,
        decision_id: str,
        reason: str
    ) -> Dict:
        """Request to unlock a decision"""
        # Check if decision exists
        decision = self.memory.decisions.get(decision_id)
        
        if not decision:
            return {
                'success': False,
                'message': f'Decision not found: {decision_id}'
            }
        
        # Check if can be unlocked
        if decision.status.value == "PERMANENT":
            return {
                'success': False,
                'message': f'Cannot unlock PERMANENT decision: {decision.decision}',
                'requires_approval': True,
                'decision': decision
            }
        
        # Unlock
        success = self.memory.unlock_decision(decision_id, reason)
        
        if success:
            return {
                'success': True,
                'message': f'Decision unlocked: {decision.decision}'
            }
        else:
            return {
                'success': False,
                'message': f'Failed to unlock decision'
            }
    
    def get_lock_status(self, proposal: str) -> Dict:
        """Check if a proposal would violate any locked decisions"""
        conflicts = self.memory.check_decision_conflict(proposal)
        
        if conflicts:
            return {
                'locked': True,
                'can_proceed': False,
                'conflicts': [
                    {
                        'decision': c.decision,
                        'status': c.status.value,
                        'reasoning': c.reasoning
                    }
                    for c in conflicts
                ],
                'message': f'❌ This proposal conflicts with {len(conflicts)} locked decision(s)'
            }
        
        return {
            'locked': False,
            'can_proceed': True,
            'conflicts': [],
            'message': '✅ No conflicts with locked decisions'
        }
