"""
MCP Server connection functions for NeuroCode.
"""

from typing import Optional, Dict, Any
from google.genai import types


async def connect_mcp_server(
    server_url: str,
    server_name: str,
    action: str,
    tool_name: str = None,
    tool_args: Dict[str, Any] = None,
    api_key: Optional[str] = "fmcp_Hj4yaUMMFPsf_LwWxuDDiL9bG2b0TYi1DHYzBGdNngw",
) -> Dict[str, Any]:
    """
    Connect to an MCP server and either list tools or call a specific tool.

    Args:
        server_url: URL of the MCP server
        server_name: Display name for the server
        action: 'list_tools' or 'call_tool'
        tool_name: Name of the tool to call (if action is 'call_tool')
        tool_args: Arguments for the tool (if action is 'call_tool')
        api_key: Optional API key for authentication

    Returns:
        Dict containing connection status and tool results
    """
    try:
        from fastmcp import Client

        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        client = Client(server_url, auth=api_key)

        async with client:
            if action == "list_tools":
                response = await client.list_tools()
                tools = [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    }
                    for tool in response
                ]
                return {
                    "status": "connected",
                    "server_name": server_name,
                    "server_url": server_url,
                    "tools": tools
                }
            elif action == "call_tool":
                if not tool_name or not tool_args:
                    return {
                        "status": "error",
                        "error": "tool_name and tool_args are required for call_tool action"
                    }
                result = await client.call_tool(tool_name, tool_args)
                return {
                    "status": "success",
                    "server_name": server_name,
                    "tool_name": tool_name,
                    "result": result
                }
            else:
                return {
                    "status": "error",
                    "error": f"Unknown action: {action}. Use 'list_tools' or 'call_tool'."
                }

    except Exception as e:
        return {
            "status": "error",
            "server_name": server_name,
            "error": str(e)
        }


async def list_mcp_tools(
    server_url: str,
    api_key: Optional[str] = "fmcp_Hj4yaUMMFPsf_LwWxuDDiL9bG2b0TYi1DHYzBGdNngw",
) -> Dict[str, Any]:
    """
    List available tools from an MCP server.

    Args:
        server_url: URL of the MCP server
        api_key: Optional API key for authentication

    Returns:
        Dict containing the list of available tools
    """
    try:
        from fastmcp import Client

        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        client = Client(server_url, auth=api_key)

        async with client:
            response = await client.list_tools()
            tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
                for tool in response
            ]
            return {
                "status": "success",
                "server_url": server_url,
                "tools": tools
            }

    except Exception as e:
        return {
            "status": "error",
            "server_url": server_url,
            "error": str(e)
        }


schema_list_mcp_tools = types.FunctionDeclaration(
    name="list_mcp_tools",
    description="List all available tools from an MCP server.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "server_url": types.Schema(
                type=types.Type.STRING,
                description="The URL of the MCP server to query."
            ),
            "api_key": types.Schema(
                type=types.Type.STRING,
                description="Optional API key for authentication."
            ),
        },
        required=["server_url"]
    )
)


schema_connect_mcp_server = types.FunctionDeclaration(
    name="connect_mcp_server",
    description="Connect to an MCP server and call its tools. Returns available tools on connection.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "server_url": types.Schema(
                type=types.Type.STRING,
                description="The URL of the MCP server to connect to."
            ),
            "server_name": types.Schema(
                type=types.Type.STRING,
                description="A friendly name identifier for the MCP server."
            ),
            "action": types.Schema(
                type=types.Type.STRING,
                enum=["list_tools", "call_tool"],
                description="Action to perform: 'list_tools' to list available tools, 'call_tool' to call a specific tool."
            ),
            "tool_name": types.Schema(
                type=types.Type.STRING,
                description="Name of the tool to call (required if action is 'call_tool')."
            ),
            "tool_args": types.Schema(
                type=types.Type.OBJECT,
                description="Arguments to pass to the tool (required if action is 'call_tool')."
            ),
            "api_key": types.Schema(
                type=types.Type.STRING,
                description="Optional API key for authentication."
            ),
        },
        required=["server_url", "server_name", "action"]
    )
)
