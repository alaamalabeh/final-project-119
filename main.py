"""
Main Entry Point for Multi-Agent System
...
"""

from dotenv import load_dotenv
load_dotenv()

import os
import sys
from orchestrator import Orchestrator

def main():
    """
    Main function to run the multi-agent system.
    """
    print("="*70)
    print("MUSIC SCALE TRAINER - AI CODE GENERATION SYSTEM")
    print("Multi-Agent System with Model Context Protocol (MCP)")
    print("Using OpenAI GPT-4o-mini API")
    print("="*70)

    # Check for API key - now checking for Google API key
    # Check for API key - now using OpenAI
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("\n ERROR: OPENAI_API_KEY environment variable not set")
        print("\nPlease set your API key in .env file")
        sys.exit(1)

    # Initialize orchestrator
    print("\n[Main] Initializing Multi-Agent System...")
    orchestrator = Orchestrator(api_key)

    # Check if GUI mode or CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # CLI mode for testing
        run_cli_mode(orchestrator)
    else:
        # GUI mode (default)
        run_gui_mode(orchestrator)


def run_cli_mode(orchestrator: Orchestrator):
    """
    Run in CLI mode for testing.

    Args:
        orchestrator: The orchestrator instance
    """
    print("\n[Main] Running in CLI mode")

    # Default MST requirements
    requirements = """
    MST (Music Scale Trainer) is a software application designed to help musicians
    and music enthusiasts practice and improve their knowledge of musical scales. It
    provides interactive exercises where users can identify and play different scales
    on their instrument of choice. The software offers a variety of difficulty levels,
    real-time feedback on accuracy, and educational resources with explanations
    and audio examples of each scale. Users can track their progress and aim to
    master all major and minor scales.
    """

    print("\n[Main] Processing default MST requirements...")

    # Run the workflow
    result = orchestrator.run_workflow(requirements)

    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    print(f"\n✓ Code generated: generated/mst_app.py")
    print(f"✓ Tests generated: generated/test_mst_generated.py")
    print(f"✓ Usage report: reports/model_usage.json")

    print("\n Model Usage Statistics:")
    import json
    print(json.dumps(result["usage_stats"], indent=2))

    print("\n Workflow complete! Check the 'generated' folder for output.")
    print("\nTo run the generated code:")
    print("  python generated/mst_app.py")
    print("\nTo run the tests:")
    print("  python run_tests.py")


def run_gui_mode(orchestrator: Orchestrator):
    """
    Launch the GUI interface.

    Args:
        orchestrator: The orchestrator instance
    """
    print("\n[Main] Launching GUI...")

    # Import GUI module
    try:
        from gui.requirements_gui import launch_gui
        launch_gui(orchestrator)
    except ImportError as e:
        print(f"\n⚠ Error importing GUI: {e}")
        print("\nFalling back to CLI mode...")
        run_cli_mode(orchestrator)

"""
=============================================================================
DEMO INSTRUCTIONS - How to Run and Test This Project
=============================================================================

STEP 1: Setup
-------------
Ensure you have all dependencies installed:
    pip3.12 install openai pytest python-dotenv

Make sure your .env file contains:
    OPENAI_API_KEY=your-api-key-here


STEP 2: Run the Multi-Agent System (CLI Mode)
----------------------------------------------
To see the complete workflow with all agents:
    python3.12 main.py --cli

This will:
- Initialize all agents (Requirements, Code Generation, Test Generation)
- Parse the MST requirements
- Generate Python code for the Music Scale Trainer
- Generate test cases
- Save outputs to generated/ folder
- Create usage report in reports/model_usage.json


STEP 3: Run the Multi-Agent System (GUI Mode)
----------------------------------------------
To use the graphical interface:
    python3.12 main.py

Then click the "🚀 Generate Code & Tests" button


STEP 4: View Generated Files
-----------------------------
Check what was generated:
    ls -la generated/
    ls -la reports/

View the usage tracking:
    cat reports/model_usage.json


STEP 5: Run the Generated Music Scale Trainer Application
----------------------------------------------------------
Launch the generated MST app:
    python3.12 generated/mst_app.py

Interact with the GUI:
- Select difficulty level (Easy/Medium/Hard)
- Click "Start Exercise" or "Identify Scale"
- Answer scale identification questions
- Track your progress


STEP 6: Run the Generated Tests
--------------------------------
Execute all test cases:
    python3.12 run_tests.py

This will:
- Run 10+ test cases
- Display pass/fail results
- Show pass rate percentage (should be 80%+)


TROUBLESHOOTING
---------------
If you get "OPENAI_API_KEY not set" error:
    export OPENAI_API_KEY='your-api-key-here'

If you get OpenAI quota exceeded:
- The system will use fallback code (this is intentional)
- The fallback demonstrates error handling and fault tolerance

If GUI doesn't launch:
- System will automatically fall back to CLI mode
- Use: python3.12 main.py --cli



=============================================================================
"""

from dotenv import load_dotenv
load_dotenv()

import os
import sys
from orchestrator import Orchestrator

# ... rest of your main.py code ...

if __name__ == "__main__":
    main()