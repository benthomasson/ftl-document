"""Tests for FTL Document validator."""

import pytest
from ftl_document.core import FTLDocument
from ftl_document.validator import DocumentValidator, ValidationError


class TestDocumentValidator:
    """Test DocumentValidator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = DocumentValidator()

    def test_valid_document(self):
        """Test validation of a valid document."""
        doc = FTLDocument(
            title="Valid Document",
            dependencies=["Python 3.8+"],
            tools_required=["pytest"],
            implementation_steps=["Step 1", "Step 2", "Step 3"],
            verification_steps=["Verify 1", "Verify 2"],
        )

        results = self.validator.validate(doc)

        assert results["valid"] is True
        assert len(results["errors"]) == 0
        assert results["score"] > 80

    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        doc = FTLDocument(
            title="", implementation_steps=[]  # Empty title  # Empty steps
        )

        results = self.validator.validate(doc)

        assert results["valid"] is False
        assert len(results["errors"]) == 2
        assert any("title" in error for error in results["errors"])
        assert any("implementation_steps" in error for error in results["errors"])

    def test_missing_recommended_fields(self):
        """Test validation with missing recommended fields."""
        doc = FTLDocument(
            title="Test Document",
            implementation_steps=["Step 1", "Step 2"],
            # Missing dependencies, tools_required, verification_steps
        )

        results = self.validator.validate(doc)

        assert results["valid"] is True  # Still valid, just warnings
        assert len(results["warnings"]) >= 2
        assert any("dependencies" in warning for warning in results["warnings"])
        assert any("verification_steps" in warning for warning in results["warnings"])

    def test_implementation_steps_validation(self):
        """Test validation of implementation steps."""
        doc = FTLDocument(
            title="Test Document",
            implementation_steps=["Install"],  # Too vague and too few steps
        )

        results = self.validator.validate(doc)

        assert len(results["warnings"]) >= 1
        assert any("at least 2 steps" in warning for warning in results["warnings"])

    def test_score_calculation(self):
        """Test score calculation."""
        # High-quality document
        good_doc = FTLDocument(
            title="Comprehensive Document",
            dependencies=["Python 3.8+"],
            tools_required=["pytest", "black"],
            implementation_steps=["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"],
            verification_steps=["Verify 1", "Verify 2", "Verify 3"],
            produces="A great result",
        )

        results = self.validator.validate(good_doc)
        assert results["score"] >= 95

        # Low-quality document
        bad_doc = FTLDocument(
            title="Bad Document", implementation_steps=["Do something"]
        )

        results = self.validator.validate(bad_doc)
        assert results["score"] < 81

    def test_validate_and_raise_valid(self):
        """Test validate_and_raise with valid document."""
        doc = FTLDocument(
            title="Valid Document", implementation_steps=["Step 1", "Step 2"]
        )

        # Should not raise
        self.validator.validate_and_raise(doc)

    def test_validate_and_raise_invalid(self):
        """Test validate_and_raise with invalid document."""
        doc = FTLDocument(title="", implementation_steps=[])  # Invalid  # Invalid

        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_and_raise(doc)

        assert "validation failed" in str(exc_info.value).lower()
