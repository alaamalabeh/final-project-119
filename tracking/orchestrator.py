"""
Orchestrator
Author: [Your Name] - [Student ID]

Coordinates the multi-agent system workflow using MCP.
Manages the flow: Requirements -> Code Generation -> Test Generation
"""

from infra.mcp_bus import MCPBus, MCPMessage, MCPTool
from agents.requirements_agent import RequirementsAgent
from agents.code_agents import CodeGenerationAgent
from agents.test_agent import TestGenerationAgent
from typing import Dict
import json
import os


class Orchestrator:
    """
    Orchestrates the multi-agent workflow using MCP for communication.
    """

    def __init__(self, api_key: str):
        """
        Initialize the orchestrator and all agents.

        Args:
            api_key: Anthropic API key for agents
        """
        # Initialize MCP bus
        self.mcp_bus = MCPBus()

        # Initialize all agents
        self.requirements_agent = RequirementsAgent(api_key)
        self.code_agent = CodeGenerationAgent(api_key)
        self.test_agent = TestGenerationAgent(api_key)

        # Register agents with MCP bus
        self.mcp_bus.register_agent("RequirementsAgent", self.requirements_agent)
        self.mcp_bus.register_agent("CodeGenerationAgent", self.code_agent)
        self.mcp_bus.register_agent("TestGenerationAgent", self.test_agent)

        # Register tools
        self._register_tools()

        print("[Orchestrator] Initialized with all agents and tools")

    def _register_tools(self):
        """Register MCP tools that agents can use."""

        # Tool for saving generated code to file
        save_code_tool = MCPTool(
            name = "save_code",
            description = "Save generated code to a file",
            handler = self._save_code_handler,
            parameters = {"code": "string", "filename": "string"}
        )
        self.mcp_bus.register_tool(save_code_tool)

        # Tool for saving test code to file
        save_test_tool = MCPTool(
            name = "save_tests",
            description = "Save generated tests to a file",
            handler = self._save_tests_handler,
            parameters = {"test_code": "string", "filename": "string"}
        )
        self.mcp_bus.register_tool(save_test_tool)

    def _save_code_handler(self, code: str, filename: str) -> str:
        """
        Handler for save_code tool.

        Args:
            code: Code to save
            filename: Filename to save to

        Returns:
            Success message
        """
        os.makedirs("generated", exist_ok = True)
        filepath = os.path.join("generated", filename)
        with open(filepath, "w") as f:
            f.write(code)
        return f"Code saved to {filepath}"

    def _save_tests_handler(self, test_code: str, filename: str) -> str:
        """
        Handler for save_tests tool.

        Args:
            test_code: Test code to save
            filename: Filename to save to

        Returns:
            Success message
        """
        os.makedirs("generated", exist_ok = True)
        filepath = os.path.join("generated", filename)
        with open(filepath, "w") as f:
            f.write(test_code)
        return f"Tests saved to {filepath}"

    def run_workflow(self, requirements_text: str) -> Dict:
        """
        Run the complete workflow from requirements to code and tests.

        Args:
            requirements_text: Natural language requirements

        Returns:
            Dictionary with all generated artifacts and tracking info
        """
        print("\n" + "=" * 60)
        print("STARTING MULTI-AGENT WORKFLOW")
        print("=" * 60)

        # Step 1: Parse requirements using MCP
        print("\n[Step 1] Parsing requirements via MCP...")
        req_message = MCPMessage(
            sender = "Orchestrator",
            receiver = "RequirementsAgent",
            message_type = "process_request",
            payload = requirements_text
        )
        req_response = self.mcp_bus.send_message(req_message)
        structured_requirements = req_response.payload
        print(
            f"✓ Requirements parsed: {len(structured_requirements['requirements'].get('core_features', []))} features identified")

        # Step 2: Generate code using MCP
        print("\n[Step 2] Generating code via MCP...")
        code_message = MCPMessage(
            sender = "Orchestrator",
            receiver = "CodeGenerationAgent",
            message_type = "process_request",
            payload = structured_requirements
        )
        code_response = self.mcp_bus.send_message(code_message)
        generated_code = code_response.payload
        print(f"✓ Code generated: {len(generated_code['code'])} characters")

        # Save code using MCP tool
        save_code_msg = MCPMessage(
            sender = "Orchestrator",
            receiver = "MCPBus",
            message_type = "tool_call",
            payload = {
                "tool_name": "save_code",
                "parameters": {
                    "code": generated_code["code"],
                    "filename": "mst_app.py"
                }
            }
        )
        save_response = self.mcp_bus.send_message(save_code_msg)
        print(f"✓ {save_response.payload['result']}")

        # Step 3: Generate tests using MCP
        print("\n[Step 3] Generating test cases via MCP...")
        test_message = MCPMessage(
            sender = "Orchestrator",
            receiver = "TestGenerationAgent",
            message_type = "process_request",
            payload = (generated_code["code"], structured_requirements)
        )
        test_response = self.mcp_bus.send_message(test_message)
        generated_tests = test_response.payload
        print(f"✓ Tests generated: {len(generated_tests['test_code'])} characters")

        # Save tests using MCP tool
        save_test_msg = MCPMessage(
            sender = "Orchestrator",
            receiver = "MCPBus",
            message_type = "tool_call",
            payload = {
                "tool_name": "save_tests",
                "parameters": {
                    "test_code": generated_tests["test_code"],
                    "filename": "test_mst_generated.py"
                }
            }
        )
        save_test_response = self.mcp_bus.send_message(save_test_msg)
        print(f"✓ {save_test_response.payload['result']}")

        # Collect usage statistics
        usage_stats = self._collect_usage_stats()

        print("\n" + "=" * 60)
        print("WORKFLOW COMPLETE")
        print("=" * 60)

        return {
            "requirements": structured_requirements,
            "generated_code": generated_code,
            "generated_tests": generated_tests,
            "usage_stats": usage_stats,
            "mcp_message_history": self.mcp_bus.get_message_history()
        }

    def _collect_usage_stats(self) -> Dict:
        """
        Collect usage statistics from all agents.

        Returns:
            Dictionary with usage stats in required format
        """
        stats = {}

        # Collect from each agent
        for agent_name, agent in [
            ("RequirementsAgent", self.requirements_agent),
            ("CodeGenerationAgent", self.code_agent),
            ("TestGenerationAgent", self.test_agent)
        ]:
            agent_stats = agent.get_usage_stats()
            # Use model name as key
            model_key = agent.model

            if model_key in stats:
                # Aggregate if same model used by multiple agents
                stats[model_key]["numApiCalls"] += agent_stats["numApiCalls"]
                stats[model_key]["totalTokens"] += agent_stats["totalTokens"]
            else:
                stats[model_key] = agent_stats

        # Save to file
        os.makedirs("reports", exist_ok = True)
        with open("reports/model_usage.json", "w") as f:
            json.dump(stats, f, indent = 2)

        return stats

    def get_usage_report(self) -> str:
        """
        Get a formatted usage report.

        Returns:
            JSON string with usage statistics
        """
        if os.path.exists("reports/model_usage.json"):
            with open("reports/model_usage.json", "r") as f:
                return f.read()
        return "{}"