from mcp.server.fastmcp import FastMCP
from typing import Annotated
import os
import shutil

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

# @mcp.tool()
# def find_file(filename: Annotated[str, "Name of the file to search for (e.g., notes.txt)"]) -> str:
#     """Search common folders (Desktop, Documents, Downloads) for the file."""
#     search_dirs = [
#         os.path.expanduser("~/Desktop"),
#         os.path.expanduser("~/Documents"),
#         os.path.expanduser("~/Downloads")
#     ]
#     matches = []
#     for base in search_dirs:
#         for root, _, files in os.walk(base):
#             if filename in files:
#                 matches.append(os.path.join(root, filename))
#     if not matches:
#         return f"❌ File '{filename}' not found in Desktop, Documents, or Downloads."
#     return "\n".join([f"✅ Found: {match}" for match in matches])
    
@mcp.tool()
def find_file(filename: Annotated[str, "Name of the file or folder to search for (e.g., notes.txt or project-folder)"]) -> str:
    """Search common folders (Desktop, Documents, Downloads) for the file or folder."""
    search_dirs = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads")
    ]
    matches = []
    for base in search_dirs:
        for root, dirs, files in os.walk(base):
            # Check files
            if filename in files:
                matches.append(os.path.join(root, filename))
            # Check folders
            if filename in dirs:
                matches.append(os.path.join(root, filename))
    if not matches:
        return f"❌ '{filename}' not found in Desktop, Documents, or Downloads."
    return "\n".join([f"✅ Found: {match}" for match in matches])


@mcp.tool()
def edit_file(
    path: Annotated[str, "Path to the file to edit"],
    mode: Annotated[str, "Edit mode: 'append', 'replace_all', or 'replace_line'"],
    new_content: Annotated[str, "Text to write or append"],
    target_line: Annotated[int, "Line number to replace (1-based index)"] = -1
) -> str:
    """Edit a file based on the mode."""
    try:
        if not os.path.exists(path):
            return "❌ File not found."

        if mode == "append":
            with open(path, "a") as f:
                f.write(new_content)
            return "✅ Content appended."

        elif mode == "replace_all":
            with open(path, "w") as f:
                f.write(new_content)
            return "✅ File content replaced."

        elif mode == "replace_line":
            with open(path, "r") as f:
                lines = f.readlines()
            if target_line < 1 or target_line > len(lines):
                return "❌ Invalid line number."
            lines[target_line - 1] = new_content + "\n"
            with open(path, "w") as f:
                f.writelines(lines)
            return f"✅ Line {target_line} replaced."

        return "❌ Invalid mode. Use: append, replace_all, or replace_line."
    except Exception as e:
        return f"❌ Error editing file: {str(e)}"

@mcp.tool()
def delete_file(path: Annotated[str, "Path of the file to delete"]) -> str:
    """Delete a file."""
    try:
        if os.path.exists(path):
            os.remove(path)
            return f"✅ File deleted: {path}"
        return "❌ File not found."
    except Exception as e:
        return f"❌ Error deleting file: {str(e)}"

@mcp.tool()
def move_file(
    source: Annotated[str, "Path of the source file"],
    destination: Annotated[str, "Target location to move the file to"]
) -> str:
    """Move a file from source to destination."""
    try:
        shutil.move(source, destination)
        return f"✅ File moved to {destination}"
    except Exception as e:
        return f"❌ Error moving file: {str(e)}"

@mcp.tool()
def rename_file(
    source: Annotated[str, "Existing file path"],
    new_name: Annotated[str, "New name for the file (with or without path)"]
) -> str:
    """Rename a file to a new name or path."""
    try:
        new_path = (
            new_name
            if os.path.isabs(new_name)
            else os.path.join(os.path.dirname(source), new_name)
        )
        os.rename(source, new_path)
        return f"✅ File renamed to: {new_path}"
    except Exception as e:
        return f"❌ Error renaming file: {str(e)}"

@mcp.tool()
def summarize_file(path: Annotated[str, "Path to the file to summarize"]) -> str:
    """Returns up to 3000 characters of file content for LLM summarization."""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

if __name__ == "__main__":
    mcp.run()
