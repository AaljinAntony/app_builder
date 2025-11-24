"""
Quick test for Researcher agent functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.researcher import Researcher


def test_researcher_module_not_found():
    """Test Researcher with ModuleNotFoundError."""
    print("\n=== Test 1: ModuleNotFoundError ===")
    
    researcher = Researcher(mcp_client=None)
    
    context = {
        'last_error': "ModuleNotFoundError: No module named 'flask'",
        'language_config': {'backend': {'language': 'python', 'framework': 'flask'}}
    }
    
    result = researcher.run(
        task="Research solution for ModuleNotFoundError",
        project_path="/tmp/test",
        context=context
    )
    
    print(f"Success: {result['success']}")
    print(f"Solutions found: {len(result['output'].get('solutions', []))}")
    
    if result['success']:
        for i, solution in enumerate(result['output']['solutions'], 1):
            print(f"\nSolution {i}:")
            print(f"  Title: {solution['title']}")
            print(f"  Type: {solution['type']}")
            print(f"  Confidence: {solution['confidence']}")
            print(f"  Steps: {solution['steps'][:2]}")  # First 2 steps
    
    assert result['success'], "Researcher should succeed"
    assert len(result['output']['solutions']) > 0, "Should find solutions"
    
    print("\n✓ Test 1 passed")


def test_researcher_syntax_error():
    """Test Researcher with SyntaxError."""
    print("\n=== Test 2: SyntaxError ===")
    
    researcher = Researcher(mcp_client=None)
    
    context = {
        'last_error': "SyntaxError: invalid syntax on line 42",
        'language_config': {'backend': {'language': 'python'}}
    }
    
    result = researcher.run(
        task="Research solution for SyntaxError",
        project_path="/tmp/test",
        context=context
    )
    
    print(f"Success: {result['success']}")
    print(f"Error type detected: {result['output']['solutions'][0]['type']}")
    print(f"Confidence: {result['output']['solutions'][0]['confidence']}")
    
    assert result['success'], "Researcher should succeed"
    assert result['output']['solutions'][0]['type'] == 'syntax', "Should detect syntax error"
    assert result['output']['solutions'][0]['confidence'] == 'high', "Should be high confidence"
    
    print("\n✓ Test 2 passed")


def test_researcher_connection_refused():
    """Test Researcher with ConnectionRefusedError."""
    print("\n=== Test 3: ConnectionRefusedError ===")
    
    researcher = Researcher(mcp_client=None)
    
    context = {
        'last_error': "ConnectionRefusedError: [Errno 111] Connection refused",
        'language_config': {'backend': {'language': 'python', 'framework': 'flask'}}
    }
    
    result = researcher.run(
        task="Research solution for connection error",
        project_path="/tmp/test",
        context=context
    )
    
    print(f"Success: {result['success']}")
    solution = result['output']['solutions'][0]
    print(f"Solution title: {solution['title']}")
    print(f"First step: {solution['steps'][0]}")
    
    assert result['success'], "Researcher should succeed"
    assert 'connection' in solution['type'].lower(), "Should detect connection error"
    
    print("\n✓ Test 3 passed")


def test_researcher_summary_format():
    """Test that summary is properly formatted."""
    print("\n=== Test 4: Summary Formatting ===")
    
    researcher = Researcher(mcp_client=None)
    
    context = {
        'last_error': "NameError: name 'undefined_var' is not defined",
        'language_config': {'backend': {'language': 'python'}}
    }
    
    result = researcher.run(
        task="Research solution",
        project_path="/tmp/test",
        context=context
    )
    
    summary = result['output']['summary']
    
    print("Summary preview:")
    print(summary[:200] + "...")
    
    assert "RESEARCHER:" in summary, "Should have header"
    assert "Solution 1:" in summary, "Should list solutions"
    assert "Steps:" in summary, "Should have steps"
    
    print("\n✓ Test 4 passed")


if __name__ == '__main__':
    print("=" * 70)
    print("RESEARCHER AGENT TESTS")
    print("=" * 70)
    
    try:
        test_researcher_module_not_found()
        test_researcher_syntax_error()
        test_researcher_connection_refused()
        test_researcher_summary_format()
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
