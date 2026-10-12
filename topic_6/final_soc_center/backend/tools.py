import os
from dotenv import load_dotenv
from langchain.mcp import MCPAdapter

load_dotenv()

def get_mcp_annotations(tool) -> dict:
    """Return MCP metadata safely, even if the server provides none."""
    return (
        (tool.metadata or {})
        .get("mcp", {})
        .get("tool", {})
        .get("annotations", {})
    )


def is_safe_read_only_tool(tool) -> bool:
    """
    Allow only tools explicitly declared read-only by the MCP server.

    Any tool with absent/unknown metadata is rejected by default.
    """
    annotations = get_mcp_annotations(tool)

    return (
        annotations.get("read_only_hint") is True
        and annotations.get("destructive_hint") is not True
    )

async def get_virustotal_safe_tools() -> list:
    """Returns read only toolsimport os from Virus Total MCP server.
    Any tool with no metadata is rejected by default
    """

    token_file = os.getenv("VTAI_TOKEN_FILE")
    if not token_file:
        raise RuntimeError("Virus Total (VTAI_TOKEN_FILE) token is not configured")

    mcp_config = {
        "mcpServers": {
            "virustotal": {
                "command": "vt-mcp",
                "args": [],
                "env": {
                    "VTAI_TOKEN_FILE": token_file,
                },
            }
        }
    }

    # Connect to the MCP server and discover its tools dynamically.
    async with MCPAdapter(mcp_config) as adapter:
        discovered_tools = await adapter.list_tools()

        # Keep only explicitly read-only tools.
        safe_tools = [
            tool
            for tool in discovered_tools
            if is_safe_read_only_tool(tool)
        ]

        if not safe_tools:
            raise RuntimeError(
                "VirusTotal did not expose any explicitly read-only tools."
            )

    return safe_tools