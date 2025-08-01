"""FTL Document Generator.

A tool for generating FTL documents from arbitrary human readable documentation.
"""

__version__ = "0.1.0"
__author__ = "FTL Team"
__email__ = "team@ftl.dev"

from .core import FTLDocument, DocumentParser
from .generator import DocumentGenerator
from .validator import DocumentValidator

__all__ = [
    "FTLDocument",
    "DocumentParser", 
    "DocumentGenerator",
    "DocumentValidator",
]