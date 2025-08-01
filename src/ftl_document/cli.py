"""Command line interface for ftl-document."""

import click
from pathlib import Path
from typing import Optional

from .core import DocumentParser, FTLDocument
from .generator import DocumentGenerator
from .validator import DocumentValidator, ValidationError


@click.group()
@click.version_option(version="0.1.0")
def main():
    """FTL Document Generator - Convert documentation to FTL format."""
    pass


@main.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['markdown', 'json', 'yaml']), 
              default='markdown', help='Output format')
@click.option('--validate/--no-validate', default=True, help='Validate generated document')
def generate(input_file: Path, output: Optional[Path], format: str, validate: bool):
    """Generate FTL document from input file."""
    try:
        # Read input file
        content = input_file.read_text(encoding='utf-8')
        
        # Parse content
        parser = DocumentParser()
        # For now, assume markdown input - could be enhanced with auto-detection
        document = parser.parse_markdown(content)
        
        # Validate if requested
        if validate:
            validator = DocumentValidator()
            results = validator.validate(document)
            if not results['valid']:
                click.echo(f"Validation failed with {len(results['errors'])} errors:", err=True)
                for error in results['errors']:
                    click.echo(f"  - {error}", err=True)
                raise click.Abort()
            
            if results['warnings']:
                click.echo(f"Validation warnings ({len(results['warnings'])}):")
                for warning in results['warnings']:
                    click.echo(f"  - {warning}")
            
            click.echo(f"Document quality score: {results['score']}/100")
        
        # Generate output
        generator = DocumentGenerator()
        
        if output:
            generator.save_to_file(document, str(output), format)
            click.echo(f"Generated FTL document: {output}")
        else:
            # Output to stdout
            if format == 'markdown':
                content = generator.generate_markdown(document)
            elif format == 'json':
                content = generator.generate_json(document)
            else:  # yaml
                content = generator.generate_yaml(document)
            click.echo(content)
    
    except NotImplementedError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("This feature is not yet implemented.", err=True)
        raise click.Abort()
    except ValidationError as e:
        click.echo(f"Validation error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
def validate(input_file: Path):
    """Validate an FTL document."""
    try:
        # Read and parse document
        content = input_file.read_text(encoding='utf-8')
        parser = DocumentParser()
        document = parser.parse_markdown(content)
        
        # Validate
        validator = DocumentValidator()
        results = validator.validate(document)
        
        # Display results
        if results['valid']:
            click.echo("✓ Document is valid")
        else:
            click.echo("✗ Document validation failed", err=True)
            for error in results['errors']:
                click.echo(f"  Error: {error}", err=True)
        
        if results['warnings']:
            click.echo(f"\nWarnings ({len(results['warnings'])}):")
            for warning in results['warnings']:
                click.echo(f"  - {warning}")
        
        click.echo(f"\nQuality score: {results['score']}/100")
        
        if not results['valid']:
            raise click.Abort()
    
    except NotImplementedError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("This feature is not yet implemented.", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
def template():
    """Generate a template FTL document."""
    template_doc = FTLDocument(
        title="Example FTL Document",
        dependencies=["A prerequisite system or tool"],
        tools_required=["example_tool", "another_tool"],
        questions=[
            "What is the target system?",
            "What configuration is needed?"
        ],
        implementation_steps=[
            "Install required tools",
            "Configure the system",
            "Apply settings",
            "Verify installation"
        ],
        verification_steps=[
            "Test the configuration",
            "Verify expected behavior"
        ],
        produces="A configured system ready for use"
    )
    
    generator = DocumentGenerator()
    content = generator.generate_markdown(template_doc)
    click.echo(content)


if __name__ == '__main__':
    main()