import os
import logging
import asyncio
from typing import Optional, Dict, Any, Callable

logger = logging.getLogger('MultiAgentBuilder')

class MCPClient:
    """
    Central MCP connection manager with graceful fallback.
    Manages connections to multiple MCP servers (filesystem, github, postgres, etc.)
    """
    
    def __init__(self):
        self.servers = {}
        self.available_servers = set()
        self._initialized = False
        
    async def initialize(self):
        """Initialize MCP server connections based on environment configuration."""
        if self._initialized:
            return
            
        logger.info("Initializing MCP client...")
        
        # Check which servers are enabled
        enabled_servers = {
            'filesystem': os.getenv('MCP_FILESYSTEM_ENABLED', 'false').lower() == 'true',
            'github': os.getenv('MCP_GITHUB_ENABLED', 'false').lower() == 'true',
            'postgres': os.getenv('MCP_POSTGRES_ENABLED', 'false').lower() == 'true',
            'fetch': os.getenv('MCP_FETCH_ENABLED', 'false').lower() == 'true',
            'puppeteer': os.getenv('MCP_PUPPETEER_ENABLED', 'false').lower() == 'true',
        }
        
        # Attempt to connect to enabled servers
        for server_name, is_enabled in enabled_servers.items():
            if is_enabled:
                try:
                    await self._connect_server(server_name)
                    self.available_servers.add(server_name)
                    logger.info(f"✓ MCP server '{server_name}' connected")
                except Exception as e:
                    logger.warning(f"✗ MCP server '{server_name}' unavailable: {e}")
        
        self._initialized = True
        
        if self.available_servers:
            logger.info(f"MCP initialized with servers: {', '.join(self.available_servers)}")
        else:
            logger.info("MCP initialized with no servers (graceful fallback mode)")
    
    async def _connect_server(self, server_name: str):
        """
        Connect to a specific MCP server.
        In production, this would use the actual MCP SDK.
        For now, we simulate connection readiness.
        """
        # Placeholder for actual MCP connection logic
        # In real implementation:
        # from mcp import ClientSession, StdioServerParameters
        # session = await ClientSession(...).initialize()
        
        self.servers[server_name] = {
            'connected': True,
            'session': None  # Would store actual MCP session
        }
    
    def is_available(self, server_name: str) -> bool:
        """Check if a specific MCP server is connected and available."""
        return server_name in self.available_servers
    
    async def call_tool(
        self, 
        server_name: str, 
        tool_name: str, 
        params: Dict[str, Any],
        fallback_fn: Optional[Callable] = None
    ) -> Any:
        """
        Call an MCP tool with optional fallback.
        
        Args:
            server_name: Name of the MCP server (e.g., 'filesystem')
            tool_name: Name of the tool to call (e.g., 'write_file')
            params: Parameters to pass to the tool
            fallback_fn: Optional fallback function if MCP fails
            
        Returns:
            Result from MCP tool or fallback function
            
        Raises:
            Exception: If MCP call fails and no fallback provided
        """
        if not self.is_available(server_name):
            if fallback_fn:
                logger.debug(f"MCP '{server_name}' unavailable, using fallback")
                return fallback_fn()
            raise Exception(f"MCP server '{server_name}' not available and no fallback provided")
        
        try:
            # Placeholder for actual MCP tool call
            # In real implementation:
            # result = await self.servers[server_name]['session'].call_tool(tool_name, params)
            # return result
            
            logger.debug(f"MCP call: {server_name}.{tool_name}({params})")
            
            # Since we don't have actual MCP servers, use fallback
            if fallback_fn:
                return fallback_fn()
            else:
                raise Exception(f"MCP simulation: tool {tool_name} not implemented")
                
        except Exception as e:
            logger.error(f"MCP tool call failed: {server_name}.{tool_name} - {e}")
            if fallback_fn:
                logger.debug("Using fallback after MCP error")
                return fallback_fn()
            raise
    
    async def close(self):
        """Close all MCP server connections."""
        logger.info("Closing MCP connections...")
        for server_name in list(self.available_servers):
            try:
                # In real implementation:
                # await self.servers[server_name]['session'].close()
                self.servers.pop(server_name, None)
                self.available_servers.discard(server_name)
                logger.debug(f"Closed MCP server: {server_name}")
            except Exception as e:
                logger.error(f"Error closing {server_name}: {e}")
        
        self._initialized = False


# Singleton instance for module-level access
_mcp_client_instance: Optional[MCPClient] = None

def get_mcp_client() -> Optional[MCPClient]:
    """Get the global MCP client instance."""
    return _mcp_client_instance

def set_mcp_client(client: MCPClient):
    """Set the global MCP client instance."""
    global _mcp_client_instance
    _mcp_client_instance = client
