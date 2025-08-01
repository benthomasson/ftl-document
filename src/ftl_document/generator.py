"""FTL Document generator for creating formatted output."""

from typing import Optional, Dict, Any
from .core import FTLDocument


class DocumentGenerator:
    """Generates formatted FTL documents from FTLDocument objects."""
    
    def __init__(self, template_dir: Optional[str] = None):
        """Initialize generator with optional custom template directory."""
        self.template_dir = template_dir
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load document templates."""
        # Default markdown template
        default_template = """
# {title}

## Requirements
{dependencies}

## Tools Needed
{tools_required}

## User Questions
{questions}

## Implementation Steps
{implementation_steps}

## Verification Steps
{verification_steps}

## Produces
{produces}
"""
        return {"default": default_template}
    
    def generate_markdown(self, document: FTLDocument) -> str:
        """Generate markdown formatted FTL document."""
        template = self.templates["default"]
        
        # Format sections
        dependencies = self._format_list_section(document.dependencies)
        tools_required = self._format_list_section(document.tools_required, prefix="- ")
        questions = self._format_list_section(document.questions, prefix="- ")
        implementation_steps = self._format_numbered_list(document.implementation_steps)
        verification_steps = self._format_numbered_list(document.verification_steps)
        produces = document.produces or ""
        
        return template.format(
            title=document.title,
            dependencies=dependencies,
            tools_required=tools_required,
            questions=questions,
            implementation_steps=implementation_steps,
            verification_steps=verification_steps,
            produces=produces
        ).strip()
    
    def _format_list_section(self, items: list, prefix: str = "- ") -> str:
        """Format a list of items with given prefix."""
        if not items:
            return ""
        return "\n".join(f"{prefix}{item}" for item in items)
    
    def _format_numbered_list(self, items: list) -> str:
        """Format a numbered list of items."""
        if not items:
            return ""
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))
    
    def generate_json(self, document: FTLDocument) -> str:
        """Generate JSON representation of FTL document."""
        return document.model_dump_json(indent=2)
    
    def generate_yaml(self, document: FTLDocument) -> str:
        """Generate YAML representation of FTL document."""
        import yaml
        return yaml.dump(document.model_dump(), default_flow_style=False)
    
    def save_to_file(self, document: FTLDocument, output_path: str, format: str = "markdown") -> None:
        """Save generated document to file."""
        if format == "markdown":
            content = self.generate_markdown(document)
        elif format == "json":
            content = self.generate_json(document)
        elif format == "yaml":
            content = self.generate_yaml(document)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)