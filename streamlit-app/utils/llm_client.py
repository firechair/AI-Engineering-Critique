import os
import requests
from openai import OpenAI
from typing import List, Dict, Optional, Tuple
import streamlit as st


class LLMClient:
    """OpenRouter API client for generating and comparing AI responses."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://openrouter.ai/api/v1"):
        """
        Initialize the OpenRouter client.
        
        Args:
            api_key: OpenRouter API key
            base_url: OpenRouter API base URL
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = base_url
        self.models_url = f"{base_url}/models"
        
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=base_url
            )
        else:
            self.client = None
    
    @st.cache_data(ttl=3600)
    def fetch_models(_self) -> List[Dict]:
        """
        Fetch all available models from OpenRouter.
        Results are cached for 1 hour.
        
        Returns:
            List of model dictionaries with their properties
        """
        try:
            headers = {
                "Authorization": f"Bearer {_self.api_key}"
            }
            response = requests.get(_self.models_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            st.error(f"Error fetching models: {str(e)}")
            return []
    
    def get_free_models(self) -> List[Dict]:
        """
        Filter and return only free models (pricing = "0").
        
        Returns:
            List of free model dictionaries
        """
        all_models = self.fetch_models()
        free_models = []
        
        for model in all_models:
            pricing = model.get("pricing", {})
            prompt_price = float(pricing.get("prompt", "1"))
            completion_price = float(pricing.get("completion", "1"))
            
            # Check if both prompt and completion are free
            if prompt_price == 0.0 and completion_price == 0.0:
                free_models.append(model)
        
        return free_models
    
    def generate_response(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful AI assistant.",
        temperature: float = 0.7,
        top_p: float = 1.0,
        max_tokens: int = 4096,
        top_k: Optional[int] = None,
        seed: Optional[int] = None
    ) -> str:
        """
        Generate a single response from the LLM.
        
        Args:
            prompt: User prompt
            model: Model ID (e.g., "google/gemini-flash-1.5")
            system_prompt: System prompt for context
            temperature: Sampling temperature (0.0-2.0)
            top_p: Nucleus sampling threshold (0.0-1.0)
            max_tokens: Maximum response length
            top_k: Top-k sampling parameter (optional)
            seed: Random seed for reproducibility (optional)
        
        Returns:
            Generated response text
        """
        if not self.client:
            return "Error: OPENROUTER_API_KEY not found. Please set your API key in the environment or sidebar."
        
        try:
            # Build parameters
            params = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "top_p": top_p,
                "max_tokens": max_tokens
            }
            
            # Add optional parameters
            if top_k is not None:
                params["top_k"] = top_k
            if seed is not None:
                params["seed"] = seed
            
            response = self.client.chat.completions.create(**params)
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_dual_responses(
        self,
        prompt: str,
        model_a: str,
        model_b: str,
        system_prompt: str = "You are a helpful AI assistant.",
        params_a: Optional[Dict] = None,
        params_b: Optional[Dict] = None
    ) -> Tuple[str, str]:
        """
        Generate two responses for comparison.
        
        Args:
            prompt: User prompt
            model_a: Model ID for Response A
            model_b: Model ID for Response B
            system_prompt: System prompt for context
            params_a: Parameters for Response A (temperature, top_p, max_tokens, etc.)
            params_b: Parameters for Response B
        
        Returns:
            Tuple of (response_a, response_b)
        """
        # Default parameters
        default_params_a = {
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 4096,
            "top_k": None,
            "seed": None
        }
        default_params_b = {
            "temperature": 1.0,
            "top_p": 1.0,
            "max_tokens": 4096,
            "top_k": None,
            "seed": None
        }
        
        # Merge with user-provided parameters
        params_a = {**default_params_a, **(params_a or {})}
        params_b = {**default_params_b, **(params_b or {})}
        
        # Generate both responses
        response_a = self.generate_response(prompt, model_a, system_prompt, **params_a)
        response_b = self.generate_response(prompt, model_b, system_prompt, **params_b)
        
        return response_a, response_b
    
    def regenerate_response(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful AI assistant.",
        **params
    ) -> str:
        """
        Regenerate a single response with updated parameters.
        
        Args:
            prompt: User prompt (possibly edited)
            model: Model ID
            system_prompt: System prompt
            **params: Generation parameters (temperature, top_p, max_tokens, etc.)
        
        Returns:
            Regenerated response text
        """
        return self.generate_response(prompt, model, system_prompt, **params)
    
    def regenerate_both_responses(
        self,
        prompt: str,
        model_a: str,
        model_b: str,
        system_prompt: str = "You are a helpful AI assistant.",
        params_a: Optional[Dict] = None,
        params_b: Optional[Dict] = None
    ) -> Tuple[str, str]:
        """
        Regenerate both responses with updated prompt and/or parameters.
        
        Args:
            prompt: User prompt (possibly edited)
            model_a: Model ID for Response A
            model_b: Model ID for Response B
            system_prompt: System prompt
            params_a: Parameters for Response A
            params_b: Parameters for Response B
        
        Returns:
            Tuple of (response_a, response_b)
        """
        return self.generate_dual_responses(
            prompt, model_a, model_b, system_prompt, params_a, params_b
        )
