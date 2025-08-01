"""Tests for FTL Document generator."""

import pytest
from ftl_document.core import FTLDocument
from ftl_document.generator import DocumentGenerator


class TestDocumentGenerator:
    """Test DocumentGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = DocumentGenerator()
        self.sample_doc = FTLDocument(
            title="Test Document",
            dependencies=["Python 3.8+", "Git"],
            tools_required=["pytest", "black"],
            questions=["What is the project name?", "Which Python version?"],
            implementation_steps=["Install dependencies", "Run setup", "Configure settings"],
            verification_steps=["Run tests", "Check output"],
            produces="A configured development environment"
        )
    
    def test_generate_markdown(self):
        """Test markdown generation."""
        result = self.generator.generate_markdown(self.sample_doc)
        
        assert "# Test Document" in result
        assert "## Requirements" in result
        assert "## Tools Needed" in result
        assert "## User Questions" in result
        assert "## Implementation Steps" in result
        assert "## Verification Steps" in result
        assert "## Produces" in result
        
        # Check content formatting
        assert "- Python 3.8+" in result
        assert "1. Install dependencies" in result
        assert "A configured development environment" in result
    
    def test_generate_json(self):
        """Test JSON generation."""
        result = self.generator.generate_json(self.sample_doc)
        
        assert '"title": "Test Document"' in result
        assert '"dependencies"' in result
        assert '"implementation_steps"' in result
    
    def test_generate_yaml(self):
        """Test YAML generation."""
        result = self.generator.generate_yaml(self.sample_doc)
        
        assert "title: Test Document" in result
        assert "dependencies:" in result
        assert "implementation_steps:" in result
    
    def test_format_list_section(self):
        """Test list formatting."""
        items = ["Item 1", "Item 2", "Item 3"]
        result = self.generator._format_list_section(items)
        
        assert result == "- Item 1\n- Item 2\n- Item 3"
    
    def test_format_numbered_list(self):
        """Test numbered list formatting."""
        items = ["First step", "Second step", "Third step"]
        result = self.generator._format_numbered_list(items)
        
        assert result == "1. First step\n2. Second step\n3. Third step"
    
    def test_empty_lists(self):
        """Test handling of empty lists."""
        assert self.generator._format_list_section([]) == ""
        assert self.generator._format_numbered_list([]) == ""