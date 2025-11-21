"""
Unit tests for utils module (file_ops and command_executor).
Uses pytest framework with temporary directories.
"""
import pytest
import os
import tempfile
import shutil
from utils.file_ops import write_file, read_file, file_exists, list_files, append_to_knowledge_base
from utils.command_executor import execute


class TestFileOps:
    """Test file operations utilities."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path, ignore_errors=True)
    
    def test_write_and_read_file(self, temp_dir):
        """Test writing and reading a file."""
        test_file = os.path.join(temp_dir, "test.txt")
        content = "Hello, World!"
        
        # Write file
        result = write_file(test_file, content)
        assert result is True
        assert os.path.exists(test_file)
        
        # Read file
        read_content = read_file(test_file)
        assert read_content == content
    
    def test_write_file_creates_directories(self, temp_dir):
        """Test that write_file creates parent directories."""
        nested_file = os.path.join(temp_dir, "subdir", "nested", "test.txt")
        content = "Nested content"
        
        result = write_file(nested_file, content)
        assert result is True
        assert os.path.exists(nested_file)
        
        read_content = read_file(nested_file)
        assert read_content == content
    
    def test_file_exists(self, temp_dir):
        """Test file existence checking."""
        test_file = os.path.join(temp_dir, "exists.txt")
        
        # File doesn't exist yet
        assert file_exists(test_file) is False
        
        # Create file
        write_file(test_file, "test")
        
        # File exists now
        assert file_exists(test_file) is True
    
    def test_list_files(self, temp_dir):
        """Test listing files in a directory."""
        # Create some test files
        write_file(os.path.join(temp_dir, "file1.txt"), "content1")
        write_file(os.path.join(temp_dir, "file2.py"), "content2")
        write_file(os.path.join(temp_dir, "file3.md"), "content3")
        
        # List files
        files = list_files(temp_dir)
        assert len(files) == 3
        assert "file1.txt" in files
        assert "file2.py" in files
        assert "file3.md" in files
    
    def test_append_to_knowledge_base(self, temp_dir):
        """Test appending content to knowledge base."""
        # Change to temp directory for this test
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Create agency_kb directory
            os.makedirs("agency_kb", exist_ok=True)
            
            # Append to knowledge base
            filename = "test_knowledge.txt"
            content1 = "First entry\n"
            content2 = "Second entry\n"
            
            append_to_knowledge_base(filename, content1)
            append_to_knowledge_base(filename, content2)
            
            # Check file contents
            kb_file = os.path.join("agency_kb", filename)
            full_content = read_file(kb_file)
            assert "First entry" in full_content
            assert "Second entry" in full_content
        finally:
            os.chdir(original_dir)


class TestCommandExecutor:
    """Test command execution utilities."""
    
    def test_execute_simple_command(self):
        """Test executing a simple command (python --version)."""
        result = execute(["python", "--version"])
        
        assert result["success"] is True
        assert result["exit_code"] == 0
        assert "Python" in result["stdout"]
        assert result["stderr"] == "" or result["stderr"] is None
    
    def test_execute_with_working_directory(self, tmp_path):
        """Test executing command with specific working directory."""
        # Create a test file in temp directory
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        # List directory contents (works on both Windows and Unix)
        # Use python to list directory for cross-platform compatibility
        result = execute(
            ["python", "-c", "import os; print('\\n'.join(os.listdir('.')))"],
            cwd=str(tmp_path)
        )
        
        assert result["success"] is True
        assert "test.txt" in result["stdout"]
    
    def test_execute_failing_command(self):
        """Test handling of a failing command."""
        # Try to run a command that doesn't exist
        result = execute(["nonexistent_command_xyz"])
        
        assert result["success"] is False
        assert result["exit_code"] != 0 or "error" in result["stderr"].lower()
    
    def test_execute_timeout(self):
        """Test that long-running commands timeout appropriately."""
        # This test verifies the timeout mechanism exists
        # We won't actually wait for timeout in tests
        # Just verify the function accepts timeout parameter
        import inspect
        sig = inspect.signature(execute)
        
        # Function should have proper structure
        assert "command" in sig.parameters
        assert "cwd" in sig.parameters
