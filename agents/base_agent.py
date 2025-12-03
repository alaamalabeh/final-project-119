# """
# Base Agent Class for Multi-Agent MST System
#
# This module defines the abstract BaseAgent that all specialized agents inherit from.
# It does NOT call Gemini or any external API directly – that is handled by the MCP server.
#
# Each agent:
#   - Has a name and role description
#   - Implements process(input_data) -> output_data
#   - Tracks API usage stats (filled in by the MCP layer when applicable)
# """
#
# from __future__ import annotations
# from abc import ABC, abstractmethod
# from typing import Dict, Any
#
#
# class BaseAgent(ABC):
#     """
#     Base class for all agents in the multi-agent system.
#     Agents should implement process(), which takes a structured dict and
#     returns a structured dict.
#
#     The MCP server (mst_mcp_server.py) or orchestrator is responsible for:
#       - Turning GUI text into structured input_data
#       - Calling process()
#       - If an LLM is used, calling the LLM and then updating usage stats.
#     """
#
#     def __init__(self, name: str, role: str):
#         """
#         Initialize the base agent.
#
#         Args:
#             name: Name of the agent (e.g., "RequirementsAgent", "CodeAgent")
#             role: Short description of the agent's responsibilities
#         """
#         self.name = name
#         self.role = role
#
#         # Usage tracking (filled by orchestrator / MCP tools)
#         self.api_call_count: int = 0
#         self.total_tokens: int = 0
#
#     @abstractmethod
#     def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Main entry point for the agent's work.
#
#         Args:
#             input_data: A structured dictionary containing the agent's input
#                         (for example: requirements text, previous code, etc.)
#
#         Returns:
#             A structured dictionary with the agent's output.
#         """
#         raise NotImplementedError("Child classes must implement process().")
#
#     # --- Optional helpers for usage tracking ---
#
#     def record_usage(self, input_tokens: int, output_tokens: int) -> None:
#         """
#         Called by the MCP tool handler (or orchestrator) to update usage stats
#         after an LLM call involving this agent.
#
#         Args:
#             input_tokens: tokens in the prompt
#             output_tokens: tokens in the response
#         """
#         self.api_call_count += 1
#         self.total_tokens += int(input_tokens + output_tokens)
#
#     def get_usage_stats(self) -> Dict[str, int]:
#         """
#         Return usage statistics for reporting in the demo and written report.
#         """
#         return {
#             "numApiCalls": self.api_call_count,
#             "totalTokens": self.total_tokens,
#         }

"""
Base Agent Class for Multi-Agent System
Author: [Your Name] - [Student ID]

This module provides the base class that all specialized agents inherit from.
It handles common functionality like API calls, token tracking, and MCP communication.
"""

from typing import Dict, Any
import google.generativeai as genai


class BaseAgent:
    """
    Base class for all agents in the multi-agent system.
    Provides common functionality for API calls, tracking, and MCP integration.
    """

    def __init__(self, name: str, api_key: str="AIzaSyCv884Awefym3sqd2MiildW62z6xD-maIE", model: str = "models/gemini-2.5-flash"):
        """
        Initialize the base agent.

        Args:
            name: Name of the agent (e.g., "CodeAgent", "TestAgent")
            api_key: Google AI API key for making API calls
            model: The Gemini model to use for this agent
        """
        self.name = name
        self.model_name = model

        # Configure Gemini (only needs to succeed once per process,
        # but calling here is fine)
        genai.configure(api_key=api_key)

        # Track API usage for this agent
        self.api_call_count = 0
        self.total_tokens = 0

    def call_llm(self, messages: list, system_prompt: str = "", max_tokens: int = 4000) -> Dict[str, Any]:
        """
        Make an API call to Gemini and track usage.
        """
        # (your existing call_llm body here – you can keep what you already had)
        ...
        # don’t delete this function, just leave it as you had it

    def get_usage_stats(self) -> Dict[str, int]:
        """
        Get the usage statistics for this agent.
        """
        return {
            "numApiCalls": self.api_call_count,
            "totalTokens": self.total_tokens
        }

    def process(self, input_data: Any) -> Any:
        """
        Process input data. To be overridden by child classes.
        """
        raise NotImplementedError("Child classes must implement process()")

