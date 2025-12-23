#!/usr/bin/env python3
"""
🔍 Quality Control System
Detects dead code, duplicates, and enforces project structure
"""

import os
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class DeadCodeFinding:
    """Represents a piece of potentially dead code"""
    file_path: str
    line_number: int
    code_type: str  # "function", "class", "import", "variable"
    name: str
    reason: str
    confidence: float  # 0.0 to 1.0


@dataclass
class DuplicateFile:
    """Represents duplicate or similar files"""
    file1: str
    file2: str
    similarity: float  # 0.0 to 1.0
    reason: str
    suggestion: str


@dataclass
class StructureViolation:
    """Represents a violation of project structure rules"""
    file_path: str
    violation_type: str
    severity: str  # "error", "warning", "info"
    message: str
    suggestion: str


class DeadCodeDetector:
    """
    Detects potentially unused code
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.findings: List[DeadCodeFinding] = []
    
    def scan(self) -> List[DeadCodeFinding]:
        """Scan project for dead code"""
        self.findings = []
        
        # Scan Python files
        for py_file in self.project_path.rglob('*.py'):
            if self._should_skip(py_file):
                continue
            self._scan_python_file(py_file)
        
        # Scan JavaScript/TypeScript files
        for js_file in self.project_path.rglob('*.js'):
            if self._should_skip(js_file):
                continue
            self._scan_js_file(js_file)
        
        for ts_file in self.project_path.rglob('*.ts'):
            if self._should_skip(ts_file):
                continue
            self._scan_js_file(ts_file)
        
        return self.findings
    
    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'dist', 'build'}
        return any(skip_dir in file_path.parts for skip_dir in skip_dirs)
    
    def _scan_python_file(self, file_path: Path):
        """Scan a Python file for dead code"""
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            # Find unused imports
            imports = self._find_python_imports(content)
            for imp, line_num in imports:
                if not self._is_import_used(imp, content):
                    self.findings.append(DeadCodeFinding(
                        file_path=str(file_path.relative_to(self.project_path)),
                        line_number=line_num,
                        code_type="import",
                        name=imp,
                        reason=f"Import '{imp}' appears to be unused",
                        confidence=0.7
                    ))
            
            # Find private functions that are never called
            private_funcs = self._find_python_private_functions(content)
            for func, line_num in private_funcs:
                if not self._is_function_called(func, content):
                    self.findings.append(DeadCodeFinding(
                        file_path=str(file_path.relative_to(self.project_path)),
                        line_number=line_num,
                        code_type="function",
                        name=func,
                        reason=f"Private function '{func}' is never called",
                        confidence=0.6
                    ))
        
        except Exception:
            pass
    
    def _scan_js_file(self, file_path: Path):
        """Scan a JavaScript/TypeScript file for dead code"""
        try:
            content = file_path.read_text()
            
            # Find unused imports
            imports = self._find_js_imports(content)
            for imp, line_num in imports:
                if not self._is_js_import_used(imp, content):
                    self.findings.append(DeadCodeFinding(
                        file_path=str(file_path.relative_to(self.project_path)),
                        line_number=line_num,
                        code_type="import",
                        name=imp,
                        reason=f"Import '{imp}' appears to be unused",
                        confidence=0.7
                    ))
        
        except Exception:
            pass
    
    def _find_python_imports(self, content: str) -> List[Tuple[str, int]]:
        """Find all imports in Python code"""
        imports = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Match: import module
            match = re.match(r'^import\s+(\w+)', line.strip())
            if match:
                imports.append((match.group(1), i))
            
            # Match: from module import name
            match = re.match(r'^from\s+\S+\s+import\s+(\w+)', line.strip())
            if match:
                imports.append((match.group(1), i))
        
        return imports
    
    def _is_import_used(self, imp: str, content: str) -> bool:
        """Check if an import is used in the code"""
        # Simple heuristic: search for the import name in the rest of the code
        # Exclude the import line itself
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('import') or line.strip().startswith('from'):
                continue
            if imp in line:
                return True
        return False
    
    def _find_python_private_functions(self, content: str) -> List[Tuple[str, int]]:
        """Find private functions (starting with _)"""
        functions = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            match = re.match(r'^\s*def\s+(_\w+)\s*\(', line)
            if match:
                functions.append((match.group(1), i))
        
        return functions
    
    def _is_function_called(self, func: str, content: str) -> bool:
        """Check if a function is called"""
        # Look for function calls: func(...) or self.func(...)
        pattern = rf'{re.escape(func)}\s*\('
        matches = list(re.finditer(pattern, content))
        # More than 1 match means it's called (1st match is the definition)
        return len(matches) > 1
    
    def _find_js_imports(self, content: str) -> List[Tuple[str, int]]:
        """Find all imports in JavaScript/TypeScript code"""
        imports = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Match: import X from 'Y'
            match = re.match(r"import\s+(\w+)\s+from", line.strip())
            if match:
                imports.append((match.group(1), i))
            
            # Match: import { X } from 'Y'
            match = re.match(r"import\s+\{\s*(\w+)", line.strip())
            if match:
                imports.append((match.group(1), i))
        
        return imports
    
    def _is_js_import_used(self, imp: str, content: str) -> bool:
        """Check if a JS import is used"""
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('import'):
                continue
            if imp in line:
                return True
        return False


class DuplicateFinder:
    """
    Finds duplicate and similar files
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.duplicates: List[DuplicateFile] = []
    
    def scan(self, similarity_threshold: float = 0.8) -> List[DuplicateFile]:
        """Find duplicate and similar files"""
        self.duplicates = []
        
        # Group files by extension
        files_by_ext = defaultdict(list)
        
        for file_path in self.project_path.rglob('*'):
            if not file_path.is_file():
                continue
            if self._should_skip(file_path):
                continue
            
            ext = file_path.suffix.lower()
            if ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.css', '.scss']:
                files_by_ext[ext].append(file_path)
        
        # Compare files within same extension
        for ext, files in files_by_ext.items():
            for i, file1 in enumerate(files):
                for file2 in files[i+1:]:
                    similarity = self._calculate_similarity(file1, file2)
                    if similarity >= similarity_threshold:
                        self.duplicates.append(DuplicateFile(
                            file1=str(file1.relative_to(self.project_path)),
                            file2=str(file2.relative_to(self.project_path)),
                            similarity=similarity,
                            reason=f"Files are {similarity*100:.1f}% similar",
                            suggestion=self._suggest_merge(file1, file2, similarity)
                        ))
        
        return self.duplicates
    
    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'dist', 'build'}
        return any(skip_dir in file_path.parts for skip_dir in skip_dirs)
    
    def _calculate_similarity(self, file1: Path, file2: Path) -> float:
        """Calculate similarity between two files"""
        try:
            content1 = file1.read_text()
            content2 = file2.read_text()
            
            # Check exact match
            if content1 == content2:
                return 1.0
            
            # Note: Using SHA-256 for content comparison (not for security)
            # This is for detecting identical files efficiently
            import hashlib
            hash1 = hashlib.sha256(content1.encode()).hexdigest()
            hash2 = hashlib.sha256(content2.encode()).hexdigest()
            
            if hash1 == hash2:
                return 1.0
            
            # Calculate line-by-line similarity
            lines1 = set(content1.split('\n'))
            lines2 = set(content2.split('\n'))
            
            if not lines1 or not lines2:
                return 0.0
            
            common_lines = lines1 & lines2
            total_lines = len(lines1 | lines2)
            
            if total_lines == 0:
                return 0.0
            
            return len(common_lines) / total_lines
        
        except Exception:
            return 0.0
    
    def _suggest_merge(self, file1: Path, file2: Path, similarity: float) -> str:
        """Suggest how to merge duplicate files"""
        if similarity >= 0.95:
            return f"Files are nearly identical. Consider removing one and using a single file."
        elif similarity >= 0.8:
            return f"Files are very similar. Consider refactoring common code into a shared module."
        else:
            return f"Files share common code. Extract shared functionality into utilities."


class StructureEnforcer:
    """
    Enforces project structure rules
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.violations: List[StructureViolation] = []
        
        # Define structure rules
        self.rules = {
            'max_file_lines': 500,
            'max_function_lines': 100,
            'required_docs': ['README.md'],
            'naming_conventions': {
                'components': r'^[A-Z][a-zA-Z0-9]*\.(jsx|tsx)$',
                'utils': r'^[a-z][a-z0-9_]*\.(py|js|ts)$',
                'tests': r'^test_[a-z][a-z0-9_]*\.(py|js|ts)$'
            }
        }
    
    def scan(self) -> List[StructureViolation]:
        """Scan project for structure violations"""
        self.violations = []
        
        # Check required documentation
        self._check_required_docs()
        
        # Check file sizes
        for file_path in self.project_path.rglob('*'):
            if not file_path.is_file():
                continue
            if self._should_skip(file_path):
                continue
            
            if file_path.suffix in ['.py', '.js', '.jsx', '.ts', '.tsx']:
                self._check_file_size(file_path)
                self._check_function_sizes(file_path)
                self._check_naming_conventions(file_path)
        
        return self.violations
    
    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'dist', 'build'}
        return any(skip_dir in file_path.parts for skip_dir in skip_dirs)
    
    def _check_required_docs(self):
        """Check if required documentation exists"""
        for doc in self.rules['required_docs']:
            doc_path = self.project_path / doc
            if not doc_path.exists():
                self.violations.append(StructureViolation(
                    file_path=doc,
                    violation_type="missing_documentation",
                    severity="warning",
                    message=f"Required documentation '{doc}' is missing",
                    suggestion=f"Create {doc} to document your project"
                ))
    
    def _check_file_size(self, file_path: Path):
        """Check if file exceeds maximum line count"""
        try:
            lines = file_path.read_text().split('\n')
            line_count = len(lines)
            
            if line_count > self.rules['max_file_lines']:
                self.violations.append(StructureViolation(
                    file_path=str(file_path.relative_to(self.project_path)),
                    violation_type="file_too_large",
                    severity="warning",
                    message=f"File has {line_count} lines (max: {self.rules['max_file_lines']})",
                    suggestion="Consider splitting this file into smaller modules"
                ))
        
        except Exception:
            pass
    
    def _check_function_sizes(self, file_path: Path):
        """Check if functions exceed maximum line count"""
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            # Find functions (Python and JS)
            if file_path.suffix == '.py':
                pattern = r'^\s*def\s+(\w+)\s*\('
            else:
                pattern = r'(?:function|const|let|var)\s+(\w+)\s*(?:=\s*)?\('
            
            current_function = None
            function_start = 0
            indent_level = 0
            
            for i, line in enumerate(lines):
                match = re.match(pattern, line)
                if match:
                    # Check previous function
                    if current_function:
                        func_lines = i - function_start
                        if func_lines > self.rules['max_function_lines']:
                            self.violations.append(StructureViolation(
                                file_path=str(file_path.relative_to(self.project_path)),
                                violation_type="function_too_large",
                                severity="info",
                                message=f"Function '{current_function}' has {func_lines} lines (max: {self.rules['max_function_lines']})",
                                suggestion="Consider breaking this function into smaller functions"
                            ))
                    
                    current_function = match.group(1)
                    function_start = i
        
        except Exception:
            pass
    
    def _check_naming_conventions(self, file_path: Path):
        """Check if file follows naming conventions"""
        file_name = file_path.name
        parent_dir = file_path.parent.name
        
        # Check component naming
        if parent_dir in ['components', 'component']:
            pattern = self.rules['naming_conventions']['components']
            if not re.match(pattern, file_name):
                self.violations.append(StructureViolation(
                    file_path=str(file_path.relative_to(self.project_path)),
                    violation_type="naming_convention",
                    severity="info",
                    message=f"Component file should follow PascalCase naming",
                    suggestion=f"Rename to follow pattern: {pattern}"
                ))
        
        # Check test naming
        if 'test' in parent_dir or file_name.startswith('test'):
            if file_path.suffix in ['.py', '.js', '.ts']:
                pattern = self.rules['naming_conventions']['tests']
                if not re.match(pattern, file_name):
                    self.violations.append(StructureViolation(
                        file_path=str(file_path.relative_to(self.project_path)),
                        violation_type="naming_convention",
                        severity="info",
                        message=f"Test file should start with 'test_'",
                        suggestion=f"Rename to follow pattern: {pattern}"
                    ))


class FileRegistry:
    """
    Maintains a registry of active files and their status
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.registry: Dict[str, Dict] = {}
    
    def scan(self) -> Dict[str, Dict]:
        """Scan and register all project files"""
        self.registry = {}
        
        for file_path in self.project_path.rglob('*'):
            if not file_path.is_file():
                continue
            if self._should_skip(file_path):
                continue
            
            rel_path = str(file_path.relative_to(self.project_path))
            
            self.registry[rel_path] = {
                'size': file_path.stat().st_size,
                'modified': file_path.stat().st_mtime,
                'extension': file_path.suffix,
                'status': self._determine_status(file_path)
            }
        
        return self.registry
    
    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'dist', 'build'}
        return any(skip_dir in file_path.parts for skip_dir in skip_dirs)
    
    def _determine_status(self, file_path: Path) -> str:
        """Determine file status"""
        # Simple heuristic: check if file has recent modifications
        import time
        current_time = time.time()
        file_mtime = file_path.stat().st_mtime
        age_days = (current_time - file_mtime) / (24 * 3600)
        
        if age_days < 7:
            return "active"
        elif age_days < 30:
            return "recent"
        else:
            return "old"
    
    def get_active_files(self) -> List[str]:
        """Get list of active files"""
        return [
            path for path, info in self.registry.items()
            if info['status'] == 'active'
        ]
    
    def get_old_files(self) -> List[str]:
        """Get list of old/potentially unused files"""
        return [
            path for path, info in self.registry.items()
            if info['status'] == 'old'
        ]


class QualityController:
    """
    Main quality control orchestrator
    """
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.dead_code_detector = DeadCodeDetector(project_path)
        self.duplicate_finder = DuplicateFinder(project_path)
        self.structure_enforcer = StructureEnforcer(project_path)
        self.file_registry = FileRegistry(project_path)
    
    def run_full_scan(self) -> Dict:
        """Run all quality checks"""
        print("🔍 Running Quality Control Scan...")
        
        print("   📂 Scanning file registry...")
        registry = self.file_registry.scan()
        
        print("   💀 Detecting dead code...")
        dead_code = self.dead_code_detector.scan()
        
        print("   🔄 Finding duplicates...")
        duplicates = self.duplicate_finder.scan()
        
        print("   📐 Checking structure...")
        violations = self.structure_enforcer.scan()
        
        report = {
            'file_registry': {
                'total_files': len(registry),
                'active_files': len(self.file_registry.get_active_files()),
                'old_files': len(self.file_registry.get_old_files())
            },
            'dead_code': {
                'findings_count': len(dead_code),
                'findings': [
                    {
                        'file': f.file_path,
                        'type': f.code_type,
                        'name': f.name,
                        'reason': f.reason,
                        'confidence': f.confidence
                    }
                    for f in dead_code
                ]
            },
            'duplicates': {
                'count': len(duplicates),
                'files': [
                    {
                        'file1': d.file1,
                        'file2': d.file2,
                        'similarity': d.similarity,
                        'suggestion': d.suggestion
                    }
                    for d in duplicates
                ]
            },
            'structure': {
                'violations_count': len(violations),
                'violations': [
                    {
                        'file': v.file_path,
                        'type': v.violation_type,
                        'severity': v.severity,
                        'message': v.message,
                        'suggestion': v.suggestion
                    }
                    for v in violations
                ]
            },
            'summary': self._generate_summary(dead_code, duplicates, violations)
        }
        
        print(f"   ✅ Scan complete!")
        return report
    
    def _generate_summary(
        self,
        dead_code: List[DeadCodeFinding],
        duplicates: List[DuplicateFile],
        violations: List[StructureViolation]
    ) -> Dict:
        """Generate summary of quality issues"""
        critical_count = sum(1 for v in violations if v.severity == "error")
        warning_count = sum(1 for v in violations if v.severity == "warning")
        
        return {
            'total_issues': len(dead_code) + len(duplicates) + len(violations),
            'critical': critical_count,
            'warnings': warning_count,
            'dead_code_files': len(set(f.file_path for f in dead_code)),
            'duplicate_pairs': len(duplicates),
            'health_score': self._calculate_health_score(dead_code, duplicates, violations)
        }
    
    def _calculate_health_score(
        self,
        dead_code: List[DeadCodeFinding],
        duplicates: List[DuplicateFile],
        violations: List[StructureViolation]
    ) -> int:
        """Calculate overall code health score (0-100)"""
        score = 100
        
        # Deduct for issues
        score -= len(dead_code) * 2
        score -= len(duplicates) * 5
        score -= sum(10 if v.severity == "error" else 3 if v.severity == "warning" else 1 
                     for v in violations)
        
        return max(0, min(100, score))
