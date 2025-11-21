
import os
import shutil
import tempfile
from unittest.mock import patch, MagicMock
from agents.planner import Planner

def test_planner_writes_plan_md():
    # Create a temporary directory for the project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = temp_dir
        
        # Mock context
        context = {
            "language_config": {"language": "Python"},
            "last_action": None
        }
        
        # Mock gemini_client response
        mock_response = {
            "plan": [
                {"step_id": 1, "description": "Step 1", "files": ["file1.py"]},
                {"step_id": 2, "description": "Step 2", "files": ["file2.py"]}
            ]
        }
        
        with patch('agents.planner.generate_with_retry') as mock_gen, \
             patch('agents.planner.extract_json') as mock_extract:
            
            mock_gen.return_value = "mocked response"
            mock_extract.return_value = mock_response
            
            planner = Planner()
            result = planner.run("Test Task", project_path, context)
            
            # Check result success
            if not result["success"]:
                print(f"FAILED: Planner run returned failure: {result.get('error')}")
                return
            
            # Check if PLAN.md exists
            plan_file = os.path.join(project_path, "PLAN.md")
            if os.path.exists(plan_file):
                print("SUCCESS: PLAN.md was created.")
                with open(plan_file, 'r') as f:
                    content = f.read()
                    print("--- PLAN.md Content ---")
                    print(content)
                    print("-----------------------")
                    
                    if "# Implementation Plan" in content and "Step 1" in content:
                        print("SUCCESS: PLAN.md content looks correct.")
                    else:
                        print("FAILED: PLAN.md content is incorrect.")
            else:
                print("FAILED: PLAN.md was NOT created.")

if __name__ == "__main__":
    test_planner_writes_plan_md()
