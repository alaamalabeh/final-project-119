# mst_mcp_server.py
"""
MST Multi-Agent MCP Server

Exposes your requirements, code, and test agents as MCP tools.
This is what Claude Desktop / MCP Inspector / a client will connect to.
"""

import os
from typing import Dict, Any

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from agents.requirements_agent import RequirementsAgent
from agents.code_agents import CodeAgent
from agents.test_agent import TestAgent

# 1. Load Google API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment or .env")

# 2. Instantiate your agents (they wrap Gemini)
requirements_agent = RequirementsAgent(
    name="RequirementsAgent",
    api_key=GOOGLE_API_KEY
)

code_agent = CodeAgent(
    name="CodeAgent",
    api_key=GOOGLE_API_KEY
)

test_agent = TestAgent(
    name="TestAgent",
    api_key=GOOGLE_API_KEY
)

# 3. Create MCP server
mcp = FastMCP("mst-multi-agent", json_response=True)


# ========== TOOLS ==========

@mcp.tool()
def analyze_requirements(requirements_text: str) -> Dict[str, Any]:
    """
    Use RequirementsAgent to turn raw MST requirements text
    into a structured spec.
    """
    spec = requirements_agent.process(requirements_text)
    usage = requirements_agent.get_usage_stats()
    return {
        "spec": spec,
        "usage": usage,
    }


@mcp.tool()
def generate_mst_code(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use CodeAgent to generate MST core code given a structured spec.
    Returns the code as a string, which your orchestrator can save to a file.
    """
    result = code_agent.process(spec)
    usage = code_agent.get_usage_stats()
    # result should contain at least {"code": "...", ...}
    return {
        "result": result,
        "usage": usage,
    }


@mcp.tool()
def generate_mst_tests(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use TestAgent to generate test code for MSTTrainer given the spec.
    """
    result = test_agent.process(spec)
    usage = test_agent.get_usage_stats()
    return {
        "result": result,
        "usage": usage,
    }


@mcp.tool()
def get_usage_summary() -> Dict[str, Any]:
    """
    Aggregate usage stats across all agents.
    This is great for your Model Usage Tracking rubric section.
    """
    return {
        "requirementsAgent": requirements_agent.get_usage_stats(),
        "codeAgent": code_agent.get_usage_stats(),
        "testAgent": test_agent.get_usage_stats(),
    }


# ========== SERVER ENTRYPOINT ==========

if __name__ == "__main__":
    # You can use "stdio" or "streamable-http".
    # "stdio" is easiest to integrate with Claude Desktop / MCP Inspector.
    mcp.run(transport="stdio")
