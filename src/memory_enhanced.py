#!/usr/bin/env python3
"""
🧠 Enhanced Guardian Memory System
Provides advanced memory, decision tracking, and session management for AI agents
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum


class DecisionStatus(Enum):
    """Status of a locked decision"""
    PERMANENT = "PERMANENT"  # Never change
    CONDITIONAL = "CONDITIONAL"  # Can change under conditions
    TEMPORARY = "TEMPORARY"  # Can change after period
    REVIEW = "REVIEW"  # Needs review before change


class ChangeType(Enum):
    """Types of changes that can occur"""
    FILE_CREATED = "FILE_CREATED"
    FILE_MODIFIED = "FILE_MODIFIED"
    FILE_DELETED = "FILE_DELETED"
    DECISION_LOCKED = "DECISION_LOCKED"
    DECISION_UNLOCKED = "DECISION_UNLOCKED"
    TECH_CHANGED = "TECH_CHANGED"
    CONFIG_CHANGED = "CONFIG_CHANGED"


@dataclass
class LockedDecision:
    """Represents a locked technical decision"""
    id: str
    category: str  # tech_stack, architecture, pattern, etc.
    decision: str  # e.g., "React as frontend framework"
    reasoning: str  # Why this was chosen
    status: DecisionStatus
    locked_at: str
    locked_by: str  # agent or user
    alternatives_rejected: List[str]
    can_change_if: Optional[str] = None  # Conditions for change
    
    def to_dict(self) -> dict:
        data = asdict(self)
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        data['status'] = DecisionStatus(data['status'])
        return cls(**data)


@dataclass
class ChangeRecord:
    """Records a change in the project"""
    id: str
    timestamp: str
    change_type: ChangeType
    description: str
    files_affected: List[str]
    agent_session: Optional[str]
    reasoning: str
    verification_status: str  # "verified", "unverified", "failed"
    
    def to_dict(self) -> dict:
        data = asdict(self)
        data['change_type'] = self.change_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        data['change_type'] = ChangeType(data['change_type'])
        return cls(**data)


@dataclass
class SessionMemory:
    """Tracks an agent session"""
    session_id: str
    started_at: str
    last_active: str
    agent_type: str  # cursor, claude, copilot, etc.
    tasks_completed: List[str]
    decisions_made: List[str]  # References to LockedDecision IDs
    changes_made: List[str]  # References to ChangeRecord IDs
    context_summary: str
    warnings_issued: int
    errors_encountered: int
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class EnhancedMemoryManager:
    """
    Enhanced memory management system for Guardian
    Provides persistent tracking, decision management, and session history
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.memory_dir = self.project_path / '.guardian'
        self.memory_dir.mkdir(exist_ok=True)
        
        # Memory files
        self.decisions_file = self.memory_dir / 'decisions.json'
        self.changes_file = self.memory_dir / 'changes.json'
        self.sessions_file = self.memory_dir / 'sessions.json'
        self.snapshots_dir = self.memory_dir / 'snapshots'
        self.snapshots_dir.mkdir(exist_ok=True)
        
        # Load existing data
        self.decisions: Dict[str, LockedDecision] = self._load_decisions()
        self.changes: Dict[str, ChangeRecord] = self._load_changes()
        self.sessions: Dict[str, SessionMemory] = self._load_sessions()
    
    # ==================== Decision Management ====================
    
    def lock_decision(
        self, 
        category: str, 
        decision: str, 
        reasoning: str,
        status: DecisionStatus = DecisionStatus.PERMANENT,
        alternatives: List[str] = None,
        locked_by: str = "user"
    ) -> LockedDecision:
        """Lock a technical decision to prevent AI from changing it"""
        decision_id = f"{category}_{len(self.decisions) + 1}"
        
        locked = LockedDecision(
            id=decision_id,
            category=category,
            decision=decision,
            reasoning=reasoning,
            status=status,
            locked_at=datetime.now().isoformat(),
            locked_by=locked_by,
            alternatives_rejected=alternatives or []
        )
        
        self.decisions[decision_id] = locked
        self._save_decisions()
        
        # Log as change
        self._log_change(
            ChangeType.DECISION_LOCKED,
            f"Locked decision: {decision}",
            [],
            reasoning
        )
        
        return locked
    
    def check_decision_conflict(self, proposal: str) -> List[LockedDecision]:
        """
        Check if a proposed change conflicts with locked decisions
        Returns list of conflicting decisions
        """
        conflicts = []
        proposal_lower = proposal.lower()
        
        # Technology mappings for conflict detection
        tech_conflicts = {
            'react': ['vue', 'angular', 'svelte'],
            'vue': ['react', 'angular', 'svelte'],
            'angular': ['react', 'vue', 'svelte'],
            'django': ['flask', 'fastapi'],
            'flask': ['django', 'fastapi'],
            'fastapi': ['django', 'flask'],
            'tailwind': ['bootstrap', 'material-ui'],
            'bootstrap': ['tailwind'],
        }
        
        for decision in self.decisions.values():
            # Check if proposal mentions alternatives that were rejected
            for alt in decision.alternatives_rejected:
                if alt.lower() in proposal_lower:
                    conflicts.append(decision)
                    break
            
            # Check for technology conflicts
            decision_lower = decision.decision.lower()
            
            # Extract technology from decision
            locked_tech = None
            for tech in tech_conflicts.keys():
                if tech in decision_lower:
                    locked_tech = tech
                    break
            
            # If decision locks a technology, check if proposal suggests conflicting one
            if locked_tech and locked_tech in tech_conflicts:
                for conflict_tech in tech_conflicts[locked_tech]:
                    if conflict_tech in proposal_lower:
                        # Check if it's a change attempt
                        change_indicators = ['change', 'switch', 'replace', 'use instead', 
                                            'migrate', 'تغيير', 'استبدال', 'استخدام', 'to']
                        if any(indicator in proposal_lower for indicator in change_indicators):
                            if decision not in conflicts:
                                conflicts.append(decision)
                            break
            
            # Check if trying to explicitly change the locked technology
            decision_words = decision.decision.lower().split()
            if any(word in proposal_lower for word in decision_words if len(word) > 3):
                # Check if it's a change attempt
                change_indicators = ['change', 'switch', 'replace', 'use instead', 
                                    'migrate', 'تغيير', 'استبدال', 'استخدام']
                if any(indicator in proposal_lower for indicator in change_indicators):
                    if decision not in conflicts:
                        conflicts.append(decision)
        
        return conflicts
    
    def get_locked_decisions(self, category: Optional[str] = None) -> List[LockedDecision]:
        """Get all locked decisions, optionally filtered by category"""
        if category:
            return [d for d in self.decisions.values() if d.category == category]
        return list(self.decisions.values())
    
    def unlock_decision(self, decision_id: str, reason: str) -> bool:
        """Unlock a decision (requires good reason)"""
        if decision_id not in self.decisions:
            return False
        
        decision = self.decisions[decision_id]
        
        # Check if can be unlocked
        if decision.status == DecisionStatus.PERMANENT:
            return False  # Cannot unlock permanent decisions
        
        del self.decisions[decision_id]
        self._save_decisions()
        
        self._log_change(
            ChangeType.DECISION_UNLOCKED,
            f"Unlocked decision: {decision.decision}",
            [],
            reason
        )
        
        return True
    
    # ==================== Change History ====================
    
    def log_change(
        self,
        change_type: ChangeType,
        description: str,
        files_affected: List[str],
        reasoning: str,
        session_id: Optional[str] = None
    ) -> ChangeRecord:
        """Log a change in the project"""
        return self._log_change(change_type, description, files_affected, reasoning, session_id)
    
    def _log_change(
        self,
        change_type: ChangeType,
        description: str,
        files_affected: List[str],
        reasoning: str,
        session_id: Optional[str] = None
    ) -> ChangeRecord:
        """Internal change logging"""
        change_id = f"change_{len(self.changes) + 1}"
        
        change = ChangeRecord(
            id=change_id,
            timestamp=datetime.now().isoformat(),
            change_type=change_type,
            description=description,
            files_affected=files_affected,
            agent_session=session_id,
            reasoning=reasoning,
            verification_status="unverified"
        )
        
        self.changes[change_id] = change
        self._save_changes()
        
        return change
    
    def get_changes(
        self,
        limit: int = 50,
        change_type: Optional[ChangeType] = None,
        session_id: Optional[str] = None
    ) -> List[ChangeRecord]:
        """Get change history with optional filters"""
        changes = list(self.changes.values())
        
        # Filter by type
        if change_type:
            changes = [c for c in changes if c.change_type == change_type]
        
        # Filter by session
        if session_id:
            changes = [c for c in changes if c.agent_session == session_id]
        
        # Sort by timestamp (most recent first)
        changes.sort(key=lambda x: x.timestamp, reverse=True)
        
        return changes[:limit]
    
    def verify_change(self, change_id: str, status: str) -> bool:
        """Mark a change as verified/unverified/failed"""
        if change_id not in self.changes:
            return False
        
        self.changes[change_id].verification_status = status
        self._save_changes()
        return True
    
    # ==================== Session Management ====================
    
    def start_session(
        self,
        agent_type: str,
        session_id: Optional[str] = None
    ) -> SessionMemory:
        """Start a new agent session"""
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = SessionMemory(
            session_id=session_id,
            started_at=datetime.now().isoformat(),
            last_active=datetime.now().isoformat(),
            agent_type=agent_type,
            tasks_completed=[],
            decisions_made=[],
            changes_made=[],
            context_summary="",
            warnings_issued=0,
            errors_encountered=0
        )
        
        self.sessions[session_id] = session
        self._save_sessions()
        
        return session
    
    def update_session(
        self,
        session_id: str,
        task: Optional[str] = None,
        context: Optional[str] = None,
        warning: bool = False,
        error: bool = False
    ) -> bool:
        """Update session with new activity"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        session.last_active = datetime.now().isoformat()
        
        if task:
            session.tasks_completed.append(task)
        
        if context:
            session.context_summary = context
        
        if warning:
            session.warnings_issued += 1
        
        if error:
            session.errors_encountered += 1
        
        self._save_sessions()
        return True
    
    def get_session(self, session_id: str) -> Optional[SessionMemory]:
        """Get session information"""
        return self.sessions.get(session_id)
    
    def get_recent_sessions(self, limit: int = 10) -> List[SessionMemory]:
        """Get recent sessions"""
        sessions = list(self.sessions.values())
        sessions.sort(key=lambda x: x.last_active, reverse=True)
        return sessions[:limit]
    
    # ==================== Snapshot Management ====================
    
    def create_snapshot(self, snapshot_data: dict, label: str = "") -> str:
        """Create a versioned snapshot of the project state"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        snapshot_id = f"snapshot_{timestamp}"
        if label:
            snapshot_id += f"_{label}"
        
        snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
        
        snapshot = {
            'id': snapshot_id,
            'timestamp': datetime.now().isoformat(),
            'label': label,
            'data': snapshot_data,
            'locked_decisions_count': len(self.decisions),
            'changes_count': len(self.changes)
        }
        
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        return snapshot_id
    
    def get_snapshot(self, snapshot_id: str) -> Optional[dict]:
        """Retrieve a snapshot by ID"""
        snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
        
        if not snapshot_file.exists():
            return None
        
        with open(snapshot_file) as f:
            return json.load(f)
    
    def list_snapshots(self) -> List[dict]:
        """List all available snapshots"""
        snapshots = []
        
        for snapshot_file in self.snapshots_dir.glob('snapshot_*.json'):
            try:
                with open(snapshot_file) as f:
                    data = json.load(f)
                    snapshots.append({
                        'id': data['id'],
                        'timestamp': data['timestamp'],
                        'label': data.get('label', ''),
                        'locked_decisions': data.get('locked_decisions_count', 0),
                        'changes': data.get('changes_count', 0)
                    })
            except Exception:
                continue
        
        snapshots.sort(key=lambda x: x['timestamp'], reverse=True)
        return snapshots
    
    # ==================== Health Monitoring ====================
    
    def get_health_report(self) -> dict:
        """Generate a health report of the project"""
        recent_changes = self.get_changes(limit=20)
        recent_sessions = self.get_recent_sessions(limit=5)
        
        # Calculate metrics
        unverified_changes = sum(1 for c in recent_changes if c.verification_status == "unverified")
        failed_changes = sum(1 for c in recent_changes if c.verification_status == "failed")
        
        total_warnings = sum(s.warnings_issued for s in recent_sessions)
        total_errors = sum(s.errors_encountered for s in recent_sessions)
        
        # Determine health status
        health_score = 100
        health_score -= unverified_changes * 2
        health_score -= failed_changes * 5
        health_score -= total_warnings * 1
        health_score -= total_errors * 3
        health_score = max(0, health_score)
        
        if health_score >= 90:
            status = "healthy"
        elif health_score >= 70:
            status = "warning"
        elif health_score >= 50:
            status = "concerning"
        else:
            status = "critical"
        
        return {
            'status': status,
            'health_score': health_score,
            'locked_decisions': len(self.decisions),
            'total_changes': len(self.changes),
            'unverified_changes': unverified_changes,
            'failed_changes': failed_changes,
            'active_sessions': len([s for s in recent_sessions if self._is_session_active(s)]),
            'total_warnings': total_warnings,
            'total_errors': total_errors,
            'recommendations': self._generate_recommendations(
                unverified_changes, failed_changes, total_errors
            )
        }
    
    def _is_session_active(self, session: SessionMemory) -> bool:
        """Check if a session is still active (within last hour)"""
        from datetime import datetime, timedelta
        
        last_active = datetime.fromisoformat(session.last_active)
        threshold = datetime.now() - timedelta(hours=1)
        
        return last_active > threshold
    
    def _generate_recommendations(
        self, 
        unverified: int, 
        failed: int, 
        errors: int
    ) -> List[str]:
        """Generate health recommendations"""
        recommendations = []
        
        if unverified > 10:
            recommendations.append("Many unverified changes - run tests to verify recent modifications")
        
        if failed > 3:
            recommendations.append("Multiple failed changes detected - review and fix broken modifications")
        
        if errors > 5:
            recommendations.append("High error rate - agent may be struggling, consider starting fresh session")
        
        if len(self.decisions) == 0:
            recommendations.append("No locked decisions - consider locking key technical choices")
        
        return recommendations
    
    # ==================== Persistence ====================
    
    def _load_decisions(self) -> Dict[str, LockedDecision]:
        """Load decisions from disk"""
        if not self.decisions_file.exists():
            return {}
        
        try:
            with open(self.decisions_file) as f:
                data = json.load(f)
                return {
                    k: LockedDecision.from_dict(v)
                    for k, v in data.items()
                }
        except Exception:
            return {}
    
    def _save_decisions(self):
        """Save decisions to disk"""
        data = {
            k: v.to_dict()
            for k, v in self.decisions.items()
        }
        
        with open(self.decisions_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_changes(self) -> Dict[str, ChangeRecord]:
        """Load changes from disk"""
        if not self.changes_file.exists():
            return {}
        
        try:
            with open(self.changes_file) as f:
                data = json.load(f)
                return {
                    k: ChangeRecord.from_dict(v)
                    for k, v in data.items()
                }
        except Exception:
            return {}
    
    def _save_changes(self):
        """Save changes to disk"""
        data = {
            k: v.to_dict()
            for k, v in self.changes.items()
        }
        
        with open(self.changes_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_sessions(self) -> Dict[str, SessionMemory]:
        """Load sessions from disk"""
        if not self.sessions_file.exists():
            return {}
        
        try:
            with open(self.sessions_file) as f:
                data = json.load(f)
                return {
                    k: SessionMemory.from_dict(v)
                    for k, v in data.items()
                }
        except Exception:
            return {}
    
    def _save_sessions(self):
        """Save sessions to disk"""
        data = {
            k: v.to_dict()
            for k, v in self.sessions.items()
        }
        
        with open(self.sessions_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    # ==================== Export for Guardian MDC ====================
    
    def export_for_mdc(self) -> dict:
        """Export memory data for inclusion in guardian.mdc"""
        return {
            'locked_decisions': [
                {
                    'decision': d.decision,
                    'category': d.category,
                    'status': d.status.value,
                    'reasoning': d.reasoning,
                    'locked_at': d.locked_at
                }
                for d in self.decisions.values()
            ],
            'recent_changes': [
                {
                    'timestamp': c.timestamp,
                    'type': c.change_type.value,
                    'description': c.description,
                    'verification': c.verification_status
                }
                for c in self.get_changes(limit=10)
            ],
            'health': self.get_health_report()
        }
