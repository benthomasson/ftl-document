"""Validation utilities for FTL Documents."""

from typing import List, Dict, Any
from .core import FTLDocument


class ValidationError(Exception):
    """Exception raised when document validation fails."""
    pass


class DocumentValidator:
    """Validates FTL documents for completeness and correctness."""
    
    def __init__(self):
        self.required_sections = ['title', 'implementation_steps']
        self.recommended_sections = ['dependencies', 'tools_required', 'verification_steps']
    
    def validate(self, document: FTLDocument) -> Dict[str, Any]:
        """Validate an FTL document and return validation results."""
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'score': 0
        }
        
        # Check required sections
        for section in self.required_sections:
            if not self._has_content(document, section):
                results['errors'].append(f"Missing required section: {section}")
                results['valid'] = False
        
        # Check recommended sections
        for section in self.recommended_sections:
            if not self._has_content(document, section):
                results['warnings'].append(f"Missing recommended section: {section}")
        
        # Validate implementation steps
        if document.implementation_steps:
            step_validation = self._validate_implementation_steps(document.implementation_steps)
            results['warnings'].extend(step_validation)
        
        # Calculate score (0-100)
        results['score'] = self._calculate_score(document, results)
        
        return results
    
    def _has_content(self, document: FTLDocument, field_name: str) -> bool:
        """Check if a field has meaningful content."""
        value = getattr(document, field_name, None)
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, list):
            return len(value) > 0
        return bool(value)
    
    def _validate_implementation_steps(self, steps: List[str]) -> List[str]:
        """Validate implementation steps for common issues."""
        warnings = []
        
        if len(steps) < 2:
            warnings.append("Implementation steps should have at least 2 steps")
        
        # Check for vague steps
        vague_keywords = ['configure', 'setup', 'install', 'run']
        for i, step in enumerate(steps, 1):
            if any(keyword in step.lower() and len(step.split()) < 4 for keyword in vague_keywords):
                warnings.append(f"Step {i} may be too vague: '{step}'")
        
        return warnings
    
    def _calculate_score(self, document: FTLDocument, results: Dict[str, Any]) -> int:
        """Calculate a quality score for the document (0-100)."""
        score = 100
        
        # Deduct for errors
        score -= len(results['errors']) * 20
        
        # Deduct for warnings
        score -= len(results['warnings']) * 5
        
        # Bonus for comprehensive content
        if len(document.implementation_steps) >= 5:
            score += 5
        if len(document.verification_steps) >= 3:
            score += 5
        if document.produces:
            score += 5
        
        return max(0, min(100, score))
    
    def validate_and_raise(self, document: FTLDocument) -> None:
        """Validate document and raise ValidationError if invalid."""
        results = self.validate(document)
        if not results['valid']:
            error_msg = "Document validation failed:\n" + "\n".join(results['errors'])
            raise ValidationError(error_msg)