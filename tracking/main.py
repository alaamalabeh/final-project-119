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
    print("Using Google Gemini API")
    print("="*70)

    # Check for API key - now checking for Google API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("\n ERROR: GOOGLE_API_KEY environment variable not set")
        print("\nPlease set your API key:")
        print("  export GOOGLE_API_KEY='your-api-key-here'")
        print("\nOr create a .env file with:")
        print("  GOOGLE_API_KEY=your-api-key-here")
        print("\n Get your free API key at: https://makersuite.google.com/app/apikey")
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


if __name__ == "__main__":
    main()