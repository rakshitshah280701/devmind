from mcp.server.fastmcp import FastMCP
from typing import Annotated, Dict, Any
import re
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
def find_file(
    filename: Annotated[str, "Name of the file or folder to search for (e.g., notes.txt or project-folder)"],
    base_dir: Annotated[str, "Starting directory for search (leave blank to use home directory)"] = os.path.expanduser("~"),
    max_depth: Annotated[int, "Max search depth, -1 for unlimited"] = -1
) -> str:
    """Recursively search for a file or folder starting from base_dir, with optional depth limit."""
    matches = []

    base_dir = os.path.abspath(base_dir)

    for root, dirs, files in os.walk(base_dir):
        # Calculate depth from base
        depth = os.path.relpath(root, base_dir).count(os.sep)
        if max_depth != -1 and depth > max_depth:
            dirs[:] = []  # Stop deeper traversal
            continue

        if filename in files or filename in dirs:
            matches.append(os.path.join(root, filename))

    if not matches:
        return f"❌ '{filename}' not found under {base_dir} (depth limit: {max_depth})."
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
    
project_index: Dict[str, Dict[str, Any]] = {}

@mcp.tool()
def analyze_project_structure(
    root_path: Annotated[str, "Root directory of your project"]
) -> Dict[str, Any]:
    """
    Analyze and summarize all files in a project and detect interconnections.
    Builds an in-memory index Claude can later use to retrieve full content.
    """
    global project_index
    project_index.clear()

    if not os.path.isdir(root_path):
        return {"error": "❌ Provided path is not a directory."}

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_path)

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception as e:
                continue

            # Extract basic summary and imports
            summary = summarize_heuristic(content)
            imports = detect_imports(content)

            project_index[rel_path] = {
                "path": full_path,
                "summary": summary,
                "imports": imports,
                "content": content[:1000] + ("..." if len(content) > 1000 else "")
            }

    return {"files": list(project_index.keys())}


def summarize_heuristic(code: str) -> str:
    """Rudimentary summary heuristic (could be replaced by LLM calls)."""
    lines = code.strip().splitlines()
    functions = [line for line in lines if line.strip().startswith("def ") or line.strip().startswith("class ")]
    return f"Detected {len(functions)} functions/classes. First 2: {functions[:2]}"


def detect_imports(code: str) -> list:
    """Extract basic import statements."""
    return re.findall(r'^\s*(?:from\s+([\w\.]+)|import\s+([\w\.]+))', code, re.MULTILINE)


@mcp.tool()
def get_file_summary(
    file_path: Annotated[str, "Relative path to file from last analyzed root"]
) -> Dict[str, Any]:
    """Return summary, imports, and partial content for a specific file."""
    data = project_index.get(file_path)
    if not data:
        return {"error": "File not found in current project index."}
    return data

@mcp.tool()
def list_subdirectories(
    path: Annotated[str, "Absolute or relative path to the directory"]
) -> list:
    """List all immediate subdirectories of a given path."""
    try:
        abs_path = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(abs_path):
            return [f"❌ {abs_path} is not a directory."]
        
        return sorted([
            entry for entry in os.listdir(abs_path)
            if os.path.isdir(os.path.join(abs_path, entry))
        ])
    except Exception as e:
        return [f"❌ Error listing subdirectories: {e}"]


@mcp.tool()
def get_file_content(
    file_path: Annotated[str, "Relative path to file from last analyzed root"]
) -> str:
    """Return full content of a file from current project index."""
    data = project_index.get(file_path)
    if not data:
        return "❌ File not found in current project index."
    try:
        with open(data["path"], "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"❌ Error reading file: {e}"



if __name__ == "__main__":
    mcp.run()
