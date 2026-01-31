import os
import anthropic
from typing import List, Dict, Optional

class LLMClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None

    def generate_response(
        self, 
        prompt: str, 
        system_prompt: str = "You are a helpful AI assistant.",
        model: str = "claude-3-opus-20240229",
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        """
        Generates a response from the LLM.
        """
        if not self.client:
            return "Error: ANTHROPIC_API_KEY not found. Please set your API key in the environment or sidebar."

        try:
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_multiple_responses(
        self, 
        prompt: str, 
        count: int = 2, 
        **kwargs
    ) -> List[str]:
        """
        Generates multiple responses for comparison.
        """
        responses = []
        for _ in range(count):
            responses.append(self.generate_response(prompt, **kwargs))
        return responses
