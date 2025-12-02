"""
Base Agent Class for Multi-Agent System
Author: [Your Name] - [Student ID]

This module provides the base class that all specialized agents inherit from.
It handles common functionality like API calls, token tracking, and MCP communication.
"""

from typing import Dict, Any, Optional
import google.generativeai as genai
import json


class BaseAgent:
    """
    Base class for all agents in the multi-agent system.
    Provides common functionality for API calls, tracking, and MCP integration.
    """

    def __init__(self, name: str, api_key: str, model: str = "models/gemini-2.5-flash"):
        """
        Initialize the base agent.

        Args:
            name: Name of the agent (e.g., "CodeAgent", "TestAgent")
            api_key: Google AI API key for making API calls
            model: The Gemini model to use for this agent
        """
        self.name = name
        self.model_name = model

        # Configure Gemini
        genai.configure(api_key=api_key)

        # Track API usage for this agent
        self.api_call_count = 0
        self.total_tokens = 0

    def call_llm(self, messages: list, system_prompt: str = "", max_tokens: int = 4000) -> Dict[
        str, Any]:
        """
        Make an API call to Gemini and track usage.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: System prompt to guide the model's behavior
            max_tokens: Maximum tokens in the response

        Returns:
            Dictionary containing the response text and usage information
        """
        try:
            # Create the model instance for each call
            generation_config = genai.GenerationConfig(
                max_output_tokens = max_tokens,
                temperature = 0.7,
            )

            # Set safety settings to be more permissive for code generation
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ]

            model = genai.GenerativeModel(
                self.model_name,
                generation_config = generation_config,
                safety_settings = safety_settings
            )

            # Combine system prompt and messages for Gemini
            full_prompt = ""
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n"

            # Gemini uses a simpler format - just combine all messages
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    full_prompt += f"{content}\n"
                elif role == "assistant":
                    full_prompt += f"Assistant: {content}\n"

            # Make API call to Gemini
            response = model.generate_content(full_prompt)

            # Track usage
            self.api_call_count += 1

            # Check if response has text
            if not response.candidates or not response.candidates[0].content.parts:
                raise Exception(
                    f"No valid response. Finish reason: {response.candidates[0].finish_reason if response.candidates else 'unknown'}")

            # Extract token counts from response metadata
            try:
                input_tokens = response.usage_metadata.prompt_token_count
                output_tokens = response.usage_metadata.candidates_token_count
                total_tokens = response.usage_metadata.total_token_count
            except:
                # Fallback if metadata not available
                input_tokens = len(full_prompt.split()) * 1.3  # Rough estimate
                output_tokens = len(response.text.split()) * 1.3
                total_tokens = input_tokens + output_tokens

            self.total_tokens += int(total_tokens)

            # Extract text from response
            response_text = response.text

            return {
                "text": response_text,
                "input_tokens": int(input_tokens),
                "output_tokens": int(output_tokens),
                "total_tokens": int(total_tokens)
            }

        except Exception as e:
            print(f"Error in {self.name} API call: {str(e)}")
            raise
    def get_usage_stats(self) -> Dict[str, int]:
        """
        Get the usage statistics for this agent.

        Returns:
            Dictionary with API call count and total tokens
        """
        return {
            "numApiCalls": self.api_call_count,
            "totalTokens": self.total_tokens
        }

    def process(self, input_data: Any) -> Any:
        """
        Process input data. To be overridden by child classes.

        Args:
            input_data: Input data to process

        Returns:
            Processed output
        """
        raise NotImplementedError("Child classes must implement process()")