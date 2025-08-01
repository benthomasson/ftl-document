"""LLM service for transforming documents using litellm."""

import os
from typing import TYPE_CHECKING
from pathlib import Path
import litellm


class LLMService:
    """Service for calling LLMs to transform documents."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        """Initialize LLM service with specified model."""
        self.model = model
        self.prompt_dir = Path(__file__).parent / "prompts"

    def load_prompt(self, prompt_name: str) -> str:
        """Load a prompt template from the prompts directory."""
        prompt_path = self.prompt_dir / prompt_name
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

        return prompt_path.read_text(encoding="utf-8")

    def transform_document(
        self, input_content: str, prompt_name: str = "ftl_document"
    ) -> str:
        """Transform input content using the specified prompt."""
        try:
            # Load the prompt template
            prompt_template = self.load_prompt(prompt_name)

            # Create the full prompt with input content
            full_prompt = (
                f"{prompt_template}\n\nInput document to transform:\n\n{input_content}"
            )

            # Call the LLM
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.1,  # Low temperature for consistent output
                max_tokens=4000,  # Sufficient for most documents
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise RuntimeError(f"LLM transformation failed: {str(e)}")

    def set_api_key(self, api_key: str) -> None:
        """Set the OpenAI API key for litellm."""
        os.environ["OPENAI_API_KEY"] = api_key

    def check_api_key(self) -> bool:
        """Check if API key is available."""
        return bool(os.environ.get("OPENAI_API_KEY"))
