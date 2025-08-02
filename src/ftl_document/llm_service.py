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
        self, input_content: str, prompt_name: str = "ftl_document", tools_available: str = "tools"
    ) -> str:
        """Transform input content using the specified prompt."""
        try:
            # Load the prompt template
            system_prompt = self.load_prompt(prompt_name)
            tools = self.load_prompt(tools_available)

            # Call the LLM
            response = litellm.completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"{system_prompt}\n\n{tools}"},
                    {"role": "user", "content": f"Transform this document into a complete ftl-document format. You MUST include detailed Implementation Steps and Verification Steps sections - these cannot be empty. Provide specific, actionable instructions.\n\nDocument to transform:\n\n{input_content}"},
                ],
                temperature=0,  # Low temperature for consistent output
                max_tokens=4096*4,
            )

            result = response.choices[0].message.content.strip()
            print(result)
            return result

        except Exception as e:
            raise RuntimeError(f"LLM transformation failed: {str(e)}")
