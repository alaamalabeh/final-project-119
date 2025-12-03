"""
Base Agent Class for Multi-Agent System (OpenAI Version)
Author: [Your Name] - [Student ID]

This module provides the base class using OpenAI API.
"""

from typing import Dict, Any
from openai import OpenAI


class BaseAgent:
    """
    Base class for all agents using OpenAI.
    """
    
    def __init__(self, name: str, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize the base agent.
        
        Args:
            name: Name of the agent
            api_key: OpenAI API key
            model: The model to use
        """
        self.name = name
        self.model = model
        self.client = OpenAI(api_key=api_key)
        
        # Track API usage
        self.api_call_count = 0
        self.total_tokens = 0
        
    def call_llm(self, messages: list, system_prompt: str = "", max_tokens: int = 4000) -> Dict[str, Any]:
        """
        Make an API call to OpenAI and track usage.
        """
        try:
            # Prepare messages
            openai_messages = []
            
            if system_prompt:
                openai_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            for msg in messages:
                openai_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            # Track usage
            self.api_call_count += 1
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            self.total_tokens += total_tokens
            
            # Extract response
            response_text = response.choices[0].message.content
            
            return {
                "text": response_text,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens
            }
            
        except Exception as e:
            print(f"Error in {self.name} API call: {str(e)}")
            raise
    
    def get_usage_stats(self) -> Dict[str, int]:
        """Get usage statistics."""
        return {
            "numApiCalls": self.api_call_count,
            "totalTokens": self.total_tokens
        }
    
    def process(self, input_data: Any) -> Any:
        """Process input - override in child classes."""
        raise NotImplementedError("Child classes must implement process()")
