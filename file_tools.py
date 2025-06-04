from mcp.server.fastmcp import FastMCP
from typing import Annotated
import os

# Initialize the MCP server
mcp = FastMCP("devmind")

@mcp.tool()
def create_file(
    path: Annotated[str, "Full file path to create"],
    content: Annotated[str, "Text content to write in the file"]
) -> str:
    """Create a file with the given path and content."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return f"✅ File created: {path}"
    except Exception as e:
        return f"❌ Error: {e}"
    
@mcp.tool()
def find_file(filename: Annotated[str, "Name of the file to search for (e.g., notes.txt)"]) -> str:
    """Search common folders (Desktop, Documents, Downloads) for the file."""
    search_dirs = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads")
    ]
    matches = []
    for base in search_dirs:
        for root, _, files in os.walk(base):
            if filename in files:
                matches.append(os.path.join(root, filename))
    if not matches:
        return f"❌ File '{filename}' not found in Desktop, Documents, or Downloads."
    return "\n".join([f"✅ Found: {match}" for match in matches])


if __name__ == "__main__":
    mcp.run()
