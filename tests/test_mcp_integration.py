"""
Tests for MCP integration in App Builder.
Verifies graceful fallback and MCP functionality.
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, AsyncMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.mcp_client import MCPClient, set_mcp_client, get_mcp_client
import utils.file_ops as file_ops


class TestMCPClient(unittest.TestCase):
    """Test MCP client initialization and connection management."""
    
    def setUp(self):
        """Set up test environment."""
        self.client = MCPClient()
        
    def test_client_initialization(self):
        """Test MCPClient can be instantiated."""
        self.assertIsNotNone(self.client)
        self.assertEqual(len(self.client.servers), 0)
        self.assertEqual(len(self.client.available_servers), 0)
        
    def test_is_available_returns_false_when_not_connected(self):
        """Test is_available returns False for disconnected servers."""
        self.assertFalse(self.client.is_available('filesystem'))
        self.assertFalse(self.client.is_available('github'))
        
    def test_get_set_mcp_client(self):
        """Test global MCP client getter/setter."""
        set_mcp_client(self.client)
        self.assertEqual(get_mcp_client(), self.client)
        
        # Cleanup
        set_mcp_client(None)


class TestFileOpsWithMCP(unittest.TestCase):
    """Test file operations with MCP integration."""
    
    def setUp(self):
        """Set up test environment with temp directory."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        
        # Clear any existing MCP client
        file_ops.set_mcp_client(None)
        
    def tearDown(self):
        """Clean up test directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_write_file_without_mcp(self):
        """Test file writing works without MCP (native fallback)."""
        content = "Hello, World!"
        result = file_ops.write_file(self.test_file, content)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))
        
        with open(self.test_file, 'r') as f:
            self.assertEqual(f.read(), content)
    
    def test_read_file_without_mcp(self):
        """Test file reading works without MCP (native fallback)."""
        content = "Test content"
        
        # Write file
        with open(self.test_file, 'w') as f:
            f.write(content)
        
        # Read via file_ops
        result = file_ops.read_file(self.test_file)
        self.assertEqual(result, content)
    
    def test_write_file_creates_directories(self):
        """Test that write_file creates parent directories."""
        nested_file = os.path.join(self.test_dir, 'nested', 'dir', 'file.txt')
        content = "Nested content"
        
        result = file_ops.write_file(nested_file, content)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(nested_file))
        
    def test_read_nonexistent_file_returns_empty(self):
        """Test reading non-existent file returns empty string."""
        result = file_ops.read_file('/nonexistent/file.txt')
        self.assertEqual(result, "")
    
    def test_file_exists(self):
        """Test file_exists function."""
        # Non-existent file
        self.assertFalse(file_ops.file_exists(self.test_file))
        
        # Create file
        with open(self.test_file, 'w') as f:
            f.write("test")
        
        # Should exist now
        self.assertTrue(file_ops.file_exists(self.test_file))
    
    def test_list_files(self):
        """Test list_files function."""
        # Empty directory
        files = file_ops.list_files(self.test_dir)
        self.assertEqual(files, [])
        
        # Create some files
        for i in range(3):
            filepath = os.path.join(self.test_dir, f'file{i}.txt')
            with open(filepath, 'w') as f:
                f.write(f"content {i}")
        
        # List files
        files = file_ops.list_files(self.test_dir)
        self.assertEqual(len(files), 3)
        self.assertIn('file0.txt', files)
        self.assertIn('file1.txt', files)
        self.assertIn('file2.txt', files)


class TestMCPGracefulFallback(unittest.TestCase):
    """Test graceful fallback when MCP is unavailable."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        file_ops.set_mcp_client(None)
    
    def test_file_ops_with_unavailable_mcp_client(self):
        """Test file_ops falls back gracefully when MCP client has no servers."""
        # Create MCP client with no servers
        mock_client = Mock()
        mock_client.is_available.return_value = False
        
        file_ops.set_mcp_client(mock_client)
        
        # File operations should still work via native fallback
        test_file = os.path.join(self.test_dir, 'test.txt')
        content = "Fallback test"
        
        result = file_ops.write_file(test_file, content)
        self.assertTrue(result)
        
        read_content = file_ops.read_file(test_file)
        self.assertEqual(read_content, content)


class TestMCPIntegration(unittest.TestCase):
    """Integration tests for MCP system."""
    
    def test_system_works_without_mcp_env(self):
        """Test that system initializes correctly without ENABLE_MCP."""
        # This would normally be tested with the full orchestrator
        # For now, just verify imports work
        from main import MultiAgentBuilder
        
        with patch.dict(os.environ, {'ENABLE_MCP': 'false'}):
            builder = MultiAgentBuilder()
            self.assertFalse(builder.mcp_enabled)
            self.assertIsNone(builder.mcp_client)
    
    def test_system_handles_mcp_enabled(self):
        """Test system initializes with MCP enabled."""
        from main import MultiAgentBuilder
        
        with patch.dict(os.environ, {'ENABLE_MCP': 'true'}):
            builder = MultiAgentBuilder()
            self.assertTrue(builder.mcp_enabled)
            # mcp_client will be None until _init_mcp_client is called


if __name__ == '__main__':
    unittest.main()
