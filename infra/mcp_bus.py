"""
MCP Communication Bus
Author: [Your Name] - [Student ID]

This module implements the Model Context Protocol (MCP) for inter-agent communication.
It handles message passing, tool registration, and coordination between agents.
"""

from typing import Dict, Any, Callable, List
import json
from datetime import datetime


class MCPMessage:
    """
    Represents a message in the MCP protocol.
    """

    def __init__(self, sender: str, receiver: str, message_type: str,
                 payload: Any, message_id: str = None):
        """
        Initialize an MCP message.

        Args:
            sender: Name of the sending agent
            receiver: Name of the receiving agent
            message_type: Type of message (e.g., "request", "response", "tool_call")
            payload: The actual data being sent
            message_id: Unique identifier for the message
        """
        self.sender = sender
        self.receiver = receiver
        self.message_type = message_type
        self.payload = payload
        self.message_id = message_id or self._generate_id()
        self.timestamp = datetime.now().isoformat()

    def _generate_id(self) -> str:
        """Generate a unique message ID."""
        import uuid
        return str(uuid.uuid4())

    def to_dict(self) -> Dict:
        """Convert message to dictionary."""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "message_type": self.message_type,
            "payload": self.payload,
            "message_id": self.message_id,
            "timestamp": self.timestamp
        }


class MCPTool:
    """
    Represents a tool that can be used by agents via MCP.
    """

    def __init__(self, name: str, description: str,
                 handler: Callable, parameters: Dict = None):
        """
        Initialize an MCP tool.

        Args:
            name: Name of the tool
            description: What the tool does
            handler: Function to execute when tool is called
            parameters: Schema describing tool parameters
        """
        self.name = name
        self.description = description
        self.handler = handler
        self.parameters = parameters or {}

    def execute(self, **kwargs) -> Any:
        """
        Execute the tool with given parameters.

        Returns:
            Result of tool execution
        """
        return self.handler(**kwargs)


class MCPBus:
    """
    Message bus implementing the Model Context Protocol.
    Handles communication between agents and tool execution.
    """

    def __init__(self):
        """Initialize the MCP bus."""
        self.agents = {}  # Registry of agents
        self.tools = {}  # Registry of tools
        self.message_history = []  # Log of all messages

    def register_agent(self, agent_name: str, agent: Any):
        """
        Register an agent with the MCP bus.

        Args:
            agent_name: Unique name for the agent
            agent: The agent object
        """
        self.agents[agent_name] = agent
        print(f"[MCP Bus] Registered agent: {agent_name}")

    def register_tool(self, tool: MCPTool):
        """
        Register a tool with the MCP bus.

        Args:
            tool: The MCPTool to register
        """
        self.tools[tool.name] = tool
        print(f"[MCP Bus] Registered tool: {tool.name}")

    def send_message(self, message: MCPMessage) -> MCPMessage:
        """
        Send a message from one agent to another via the bus.

        Args:
            message: The MCPMessage to send

        Returns:
            Response message from the receiver
        """
        # Log the message
        self.message_history.append(message)

        print(f"[MCP Bus] {message.sender} -> {message.receiver}: {message.message_type}")

        # Handle tool calls directly (receiver is "MCPBus")
        if message.message_type == "tool_call":
            # Execute a tool
            tool_name = message.payload.get("tool_name")
            tool_params = message.payload.get("parameters", {})

            if tool_name not in self.tools:
                raise ValueError(f"Tool '{tool_name}' not registered")

            result = self.tools[tool_name].execute(**tool_params)

            response = MCPMessage(
                sender = "MCPBus",
                receiver = message.sender,
                message_type = "tool_response",
                payload = {"result": result}
            )

            self.message_history.append(response)
            return response

        # Check if receiver exists for other message types
        if message.receiver not in self.agents:
            raise ValueError(f"Agent '{message.receiver}' not registered")

        # Get the receiving agent
        receiver_agent = self.agents[message.receiver]

        # Process based on message type
        if message.message_type == "process_request":
            # Agent processes the payload
            result = receiver_agent.process(message.payload)

            # Create response message
            response = MCPMessage(
                sender = message.receiver,
                receiver = message.sender,
                message_type = "process_response",
                payload = result
            )

            self.message_history.append(response)
            return response

        else:
            raise ValueError(f"Unknown message type: {message.message_type}")
    def broadcast(self, sender: str, message_type: str, payload: Any) -> List[MCPMessage]:
        """
        Broadcast a message to all agents.

        Args:
            sender: Name of sending agent
            message_type: Type of message
            payload: Message payload

        Returns:
            List of responses from all agents
        """
        responses = []
        for agent_name in self.agents.keys():
            if agent_name != sender:
                message = MCPMessage(sender, agent_name, message_type, payload)
                response = self.send_message(message)
                responses.append(response)
        return responses

    def get_message_history(self) -> List[Dict]:
        """
        Get the history of all messages.

        Returns:
            List of message dictionaries
        """
        return [msg.to_dict() for msg in self.message_history]

    def get_agent_tools(self, agent_name: str) -> List[str]:
        """
        Get list of tools available to an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            List of tool names
        """
        # For now, return all tools
        # In a more sophisticated system, you'd have per-agent permissions
        return list(self.tools.keys())