"""
Test Runner Script
Author: [Your Name] - [Student ID]

Automatically runs all generated test cases and reports results.
"""

import subprocess
import sys
import os
import json


def run_tests():
    """
    Run the generated test cases and report results.
    """
    print("=" * 70)
    print("RUNNING GENERATED TEST CASES")
    print("=" * 70)

    test_file = "generated/test_mst_generated.py"

    # Check if test file exists
    if not os.path.exists(test_file):
        print(f"\n Error: Test file not found: {test_file}")
        print("Please generate tests first by running: python main.py")
        sys.exit(1)

    print(f"\n Test file: {test_file}")
    print("\n Running tests with pytest...\n")

    # Try running with pytest first
    try:
        result = subprocess.run(
            ["pytest", test_file, "-v", "--tb=short"],
            capture_output = True,
            text = True
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        # Parse results
        output = result.stdout + result.stderr

        # Count passed and failed tests
        passed = output.count(" PASSED")
        failed = output.count(" FAILED")
        total = passed + failed

        if total > 0:
            pass_rate = (passed / total) * 100

            print("\n" + "=" * 70)
            print("TEST RESULTS SUMMARY")
            print("=" * 70)
            print(f"Total Tests: {total}")
            print(f"Passed: {passed} ")
            print(f"Failed: {failed} ")
            print(f"Pass Rate: {pass_rate:.1f}%")

            if pass_rate >= 80:
                print("\n SUCCESS: Pass rate meets 80% requirement!")
            else:
                print(f"\n WARNING: Pass rate below 80% requirement")

            return result.returncode == 0
        else:
            print("\n Could not parse test results")
            return False

    except FileNotFoundError:
        print(" pytest not found. Trying unittest...\n")

        # Fallback to unittest
        try:
            result = subprocess.run(
                ["python", "-m", "unittest", test_file],
                capture_output = True,
                text = True
            )

            print(result.stdout)
            print(result.stderr)

            # Check if tests ran
            if "Ran" in result.stderr:
                print("\n Tests completed (see output above)")
                return result.returncode == 0
            else:
                print("\n Tests may not have run properly")
                return False

        except Exception as e:
            print(f"\n Error running tests: {e}")
            return False


def main():
    """Main function."""
    success = run_tests()

    print("\n" + "=" * 70)

    if success:
        print(" All tests completed successfully!")
    else:
        print(" Some tests failed or had errors")

    print("=" * 70)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()