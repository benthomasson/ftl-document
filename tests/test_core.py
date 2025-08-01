"""Tests for core FTL Document functionality."""

import pytest
from ftl_document.core import FTLDocument, DocumentParser


class TestFTLDocument:
    """Test FTLDocument class."""
    
    def test_create_minimal_document(self):
        """Test creating a document with minimal required fields."""
        doc = FTLDocument(
            title="Test Document",
            implementation_steps=["Step 1", "Step 2"]
        )
        assert doc.title == "Test Document"
        assert doc.implementation_steps == ["Step 1", "Step 2"]
        assert doc.dependencies == []
        assert doc.tools_required == []
    
    def test_create_full_document(self):
        """Test creating a document with all fields."""
        doc = FTLDocument(
            title="Full Test Document",
            dependencies=["Python 3.8+"],
            tools_required=["pytest", "black"],
            questions=["What is your name?"],
            implementation_steps=["Install deps", "Run tests"],
            verification_steps=["Check output"],
            produces="A working test suite"
        )
        assert doc.title == "Full Test Document"
        assert doc.dependencies == ["Python 3.8+"]
        assert doc.tools_required == ["pytest", "black"]
        assert doc.questions == ["What is your name?"]
        assert doc.implementation_steps == ["Install deps", "Run tests"]
        assert doc.verification_steps == ["Check output"]
        assert doc.produces == "A working test suite"


class TestDocumentParser:
    """Test DocumentParser class."""
    
    def test_parser_initialization(self):
        """Test parser initializes correctly."""
        parser = DocumentParser()
        assert 'markdown' in parser.supported_formats
        assert 'docx' in parser.supported_formats
    
    def test_parse_methods_not_implemented(self):
        """Test that parse methods raise NotImplementedError."""
        parser = DocumentParser()
        
        with pytest.raises(NotImplementedError):
            parser.parse_markdown("# Test")
        
        with pytest.raises(NotImplementedError):
            parser.parse_docx("test.docx")
        
        with pytest.raises(NotImplementedError):
            parser.parse_text("Test content")
        
        with pytest.raises(NotImplementedError):
            parser.parse_html("<h1>Test</h1>")
        
        with pytest.raises(NotImplementedError):
            parser.auto_parse("Test content")