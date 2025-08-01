"""Core FTL Document classes and data structures."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FTLDocument(BaseModel):
    """Represents an FTL Document with all required sections."""
    
    title: str = Field(..., description="The title of the document")
    dependencies: List[str] = Field(default_factory=list, description="Prerequisites needed")
    tools_required: List[str] = Field(default_factory=list, description="Required automation tools")
    questions: List[str] = Field(default_factory=list, description="User input questions")
    implementation_steps: List[str] = Field(..., description="Ordered implementation steps")
    verification_steps: List[str] = Field(default_factory=list, description="Verification procedures")
    produces: Optional[str] = Field(None, description="What the document creates/achieves")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            # Add custom encoders if needed
        }


class DocumentParser:
    """Parser for converting various document formats to FTL Documents."""
    
    def __init__(self):
        self.supported_formats = ['markdown', 'docx', 'txt', 'html']
    
    def parse_markdown(self, content: str) -> FTLDocument:
        """Parse markdown content into an FTL Document."""
        # Implementation would go here
        raise NotImplementedError("Markdown parsing not yet implemented")
    
    def parse_docx(self, file_path: str) -> FTLDocument:
        """Parse DOCX file into an FTL Document."""
        # Implementation would go here
        raise NotImplementedError("DOCX parsing not yet implemented")
    
    def parse_text(self, content: str) -> FTLDocument:
        """Parse plain text content into an FTL Document."""
        # Implementation would go here
        raise NotImplementedError("Text parsing not yet implemented")
    
    def parse_html(self, content: str) -> FTLDocument:
        """Parse HTML content into an FTL Document."""
        # Implementation would go here
        raise NotImplementedError("HTML parsing not yet implemented")
    
    def auto_parse(self, content: str, format_hint: Optional[str] = None) -> FTLDocument:
        """Automatically detect format and parse content."""
        # Implementation would go here
        raise NotImplementedError("Auto-parsing not yet implemented")