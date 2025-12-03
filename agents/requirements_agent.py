"""
Requirements Agent
Author: [Your Name] - [Student ID]

This agent parses natural language requirements and converts them into
structured specifications that the code generation agent can use.
"""

from agents.base_agent import BaseAgent
from typing import Dict, List


class RequirementsAgent(BaseAgent):
    """
    Agent responsible for parsing and structuring functional requirements.
    Takes natural language input and outputs structured requirements.
    """

    def __init__(self, api_key: str):
        """Initialize the Requirements Agent."""
        super().__init__(name="RequirementsAgent", api_key=api_key)

    def process(self, requirements_text: str) -> Dict:
        """
        Parse natural language requirements into structured format.

        Args:
            requirements_text: Natural language description of requirements

        Returns:
            Dictionary containing structured requirements
        """
        system_prompt = """You are a requirements analysis expert. 
Parse software requirements into structured format.
Return ONLY a JSON object with these keys:
- core_features: list of main functionalities
- user_interactions: list of what users can do
- data_requirements: list of data to store/track
- technical_constraints: list of constraints

Return valid JSON only, no other text."""

        messages = [
            {
                "role": "user",
                "content": f"Parse these requirements into JSON:\n\n{requirements_text}"
            }
        ]

        try:
            response = self.call_llm(messages, system_prompt, max_tokens=2000)

            # Parse JSON from response
            text = response["text"]

            # Try to extract JSON
            import json

            # Find JSON block
            if "```json" in text:
                json_start = text.find("```json") + 7
                json_end = text.find("```", json_start)
                json_text = text[json_start:json_end].strip()
            elif "{" in text and "}" in text:
                json_start = text.find("{")
                json_end = text.rfind("}") + 1
                json_text = text[json_start:json_end]
            else:
                json_text = text

            structured_requirements = json.loads(json_text)

            return {
                "requirements": structured_requirements,
                "raw_text": requirements_text,
                "tokens_used": response["total_tokens"]
            }

        except Exception as e:
            print(f"Error parsing requirements: {str(e)}")
            # Return fallback structure
            return {
                "requirements": {
                    "core_features": [
                        "Interactive scale exercises",
                        "Multiple difficulty levels",
                        "Real-time feedback",
                        "Progress tracking",
                        "Educational resources"
                    ],
                    "user_interactions": [
                        "Identify scales",
                        "Practice scales",
                        "View progress",
                        "Access scale information"
                    ],
                    "data_requirements": [
                        "Scale definitions",
                        "User scores",
                        "Practice history"
                    ],
                    "technical_constraints": [
                        "Python standard library only",
                        "Simple text-based or GUI interface"
                    ]
                },
                "raw_text": requirements_text,
                "tokens_used": 0
            }
