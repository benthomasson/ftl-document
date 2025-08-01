"""Core FTL Document classes and data structures."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .llm_service import LLMService


class FTLDocument(BaseModel):
    """Represents an FTL Document with all required sections."""

    title: str = Field(..., description="The title of the document")
    dependencies: List[str] = Field(
        default_factory=list, description="Prerequisites needed"
    )
    tools_required: List[str] = Field(
        default_factory=list, description="Required automation tools"
    )
    questions: List[str] = Field(
        default_factory=list, description="User input questions"
    )
    implementation_steps: List[str] = Field(
        ..., description="Ordered implementation steps"
    )
    verification_steps: List[str] = Field(
        default_factory=list, description="Verification procedures"
    )
    produces: Optional[str] = Field(
        None, description="What the document creates/achieves"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    class Config:
        """Pydantic configuration."""

        json_encoders = {
            # Add custom encoders if needed
        }


class DocumentParser:
    """Parser for converting various document formats to FTL Documents using LLM."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.supported_formats = ["markdown", "docx", "txt", "html"]
        self.llm_service = LLMService(model=model)

    def parse_with_llm(self, content: str) -> FTLDocument:
        """Parse any content using LLM transformation to FTL Document."""
        try:
            # Transform content using LLM
            transformed_content = self.llm_service.transform_document(content)

            # Parse the LLM response into structured data
            return self._parse_ftl_markdown(transformed_content)

        except Exception as e:
            raise RuntimeError(f"Failed to parse content with LLM: {str(e)}")

    def _parse_ftl_markdown(self, markdown_content: str) -> FTLDocument:
        """Parse FTL-formatted markdown into FTLDocument object."""
        lines = markdown_content.strip().split("\n")

        # Initialize fields
        title = ""
        dependencies = []
        tools_required = []
        questions = []
        implementation_steps = []
        verification_steps = []
        produces = ""

        current_section = None

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Check for title (markdown h1)
            if line.startswith("# "):
                title = line[2:].strip()
                continue

            # Check for sections
            if line.startswith("**") and line.endswith("**"):
                section_name = line[2:-2].lower()
                if "requirement" in section_name or "dependencies" in section_name:
                    current_section = "dependencies"
                elif "tool" in section_name:
                    current_section = "tools_required"
                elif "question" in section_name:
                    current_section = "questions"
                elif "implementation" in section_name:
                    current_section = "implementation_steps"
                elif "verification" in section_name:
                    current_section = "verification_steps"
                elif "produce" in section_name:
                    current_section = "produces"
                continue

            # Parse list items
            if line.startswith("- ") and current_section:
                item = line[2:].strip()
                if current_section == "dependencies":
                    dependencies.append(item)
                elif current_section == "tools_required":
                    tools_required.append(item)
                elif current_section == "questions":
                    questions.append(item)
                elif current_section == "produces":
                    produces = item

            # Parse numbered items for steps
            elif line and current_section in [
                "implementation_steps",
                "verification_steps",
            ]:
                # Remove number prefix if present
                if line[0].isdigit() and ". " in line:
                    item = line.split(". ", 1)[1]
                elif line.startswith("- "):
                    item = line[2:].strip()
                else:
                    item = line

                if current_section == "implementation_steps":
                    implementation_steps.append(item)
                elif current_section == "verification_steps":
                    verification_steps.append(item)

        return FTLDocument(
            title=title or "Untitled Document",
            dependencies=dependencies,
            tools_required=tools_required,
            questions=questions,
            implementation_steps=implementation_steps,
            verification_steps=verification_steps,
            produces=produces,
        )

    def parse_markdown(self, content: str) -> FTLDocument:
        """Parse markdown content into an FTL Document using LLM."""
        return self.parse_with_llm(content)

    def parse_docx(self, file_path: str) -> FTLDocument:
        """Parse DOCX file into an FTL Document using LLM."""
        # For now, raise NotImplementedError - could be enhanced later
        raise NotImplementedError("DOCX parsing not yet implemented")

    def parse_text(self, content: str) -> FTLDocument:
        """Parse plain text content into an FTL Document using LLM."""
        return self.parse_with_llm(content)

    def parse_html(self, content: str) -> FTLDocument:
        """Parse HTML content into an FTL Document using LLM."""
        return self.parse_with_llm(content)

    def auto_parse(
        self, content: str, format_hint: Optional[str] = None
    ) -> FTLDocument:
        """Automatically detect format and parse content using LLM."""
        return self.parse_with_llm(content)
