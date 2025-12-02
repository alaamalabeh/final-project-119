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
        super().__init__(name = "RequirementsAgent", api_key = api_key)

    def process(self, requirements_text: str) -> Dict:
        """
        Parse natural language requirements into structured format.

        Args:
            requirements_text: Natural language description of requirements

        Returns:
            Dictionary containing structured requirements
        """
        system_prompt = """You are a requirements analysis expert. 
Parse the given software requirements into a structured format.
Extract:
1. Core features (list of main functionalities)
2. User interactions (what users can do)
3. Data requirements (what data needs to be stored/tracked)
4. Technical constraints

Return your response as a JSON object with these keys:
- core_features: list of strings
- user_interactions: list of strings
- data_requirements: list of strings
- technical_constraints: list of strings
"""

        messages = [
            {
                "role": "user",
                "content": f"Parse these requirements:\n\n{requirements_text}\n\nProvide structured JSON output."
            }
        ]

        response = self.call_llm(messages, system_prompt, max_tokens = 2000)

        # Parse JSON from response
        try:
            # Extract JSON from response text
            text = response["text"]
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

            import json
            structured_requirements = json.loads(json_text)

            return {
                "requirements": structured_requirements,
                "raw_text": requirements_text,
                "tokens_used": response["total_tokens"]
            }

        except Exception as e:
            print(f"Error parsing requirements: {str(e)}")
            # Return basic structure if parsing fails
            return {
                "requirements": {
                    "core_features": [requirements_text],
                    "user_interactions": [],
                    "data_requirements": [],
                    "technical_constraints": []
                },
                "raw_text": requirements_text,
                "tokens_used": response["total_tokens"]
            }