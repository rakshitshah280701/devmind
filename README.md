
<p align="center">
<img width="409" alt="DevMind Logo" src="https://github.com/user-attachments/assets/5baacc56-c184-4077-baa6-eb204090ba14" />
</p>

# 🧠 DevMind — Developer Assistant with Claude + MCP

DevMind is a local-first developer productivity agent powered by [Claude Desktop](https://www.anthropic.com/index/claude-desktop) and the Model Context Protocol (MCP). It lets you **create**, **navigate**, **analyze**, and **interact with projects** entirely using natural language — like a coding co-pilot that deeply understands your files and codebase.

---

## ⚙️ Tools Available

### ✅ `create_file`
Create a file at a specific location with any content you want.

> _“Create a file named `hello.txt` with content `Hello World!` in the DevMind folder on Desktop.”_

---

### 🔍 `find_file`
Recursively search from any directory and locate files or folders.

> _“Where is `notes.txt` inside my Desktop?”_

---

### ✍️ `edit_file`
Edit any file using:
- `append` – Add content at the end
- `replace_all` – Overwrite the full file
- `replace_line` – Replace a specific line number

---

### ❌ `delete_file`
Delete any file by its path.

---

### 🚚 `move_file`
Move a file to another folder.

---

### 📝 `rename_file`
Rename a file or move+rename in one go.

---

### 📄 `summarize_file`
Returns the full file content for Claude to summarize.

---

### 📁 `list_subdirectories`
List all immediate subdirectories inside a given folder.

> _“List all projects inside `~/Desktop/Github_projects`”_

---

### 🧠 `analyze_project_structure`
Scans every file in your codebase, summarizes each one, detects imports, and builds a memory index of all files.

> Use this once to let Claude “understand” your project structure.

---

### 🔍 `get_file_summary`
Return the summary and imports of any file previously analyzed.

> _“What does `routes/auth.py` do?”_

---

### 📂 `get_file_content`
Return the **full source code** of any file Claude previously indexed.

> _“Show me full content of `models/user.py`”_

---

## 🛠 How to Use

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/devmind.git
cd devmind
```

### 2. Set up the virtual environment (Python 3.11.x recommended)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install uv
uv pip install "mcp[cli]"
```

### 4. Register tools with Claude Desktop via MCP

Install your tool into Claude by running:

```bash
uv run mcp install file_tools.py
```

You’ll see a success message like:

```
INFO     Added server 'file_tools' to Claude config
```

---

## 🧠 Cross check tools connecticity to Claude Desktop

1. Open Claude Desktop.
2. Go to `Settings → Developer`.
3. click on “Edit Config” and it should look something like this:
   

```bash
 {
  "mcpServers": {
    "devmind": {
      "command": "{relativepath}/devmind/.venv/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "{relativepath}/devmind/file_tools.py"
      ]
    }
  }
}
```

> You can now say:
> “Create a Python file in my DevMind folder and write a basic FastAPI app.”

---

## 🛡 Permissions

These tools **only access your local machine**. No cloud APIs, no remote uploads.

Make sure Claude has:

* **Full Disk Access** (System Settings → Privacy & Security → Full Disk Access)

---

## 🚀 Roadmap

* [x] File creation via LLM
* [x] File and Folder search across system
* [x] Create, edit, move, rename and delete files 
* [x] Summarize any file
* [x] Project summarization and indexing
* [x] Per-file summary and full-content tools
* [x] Directory exploration (list_subdirectories)


---

## 📂 Project Structure

```
devmind/
├── .venv/
├── file_tools.py    # MCP tools for file operations
├── README.md
└── ...
```

---

## 🙌 Inspired By

Projects like [Cursor](https://cursor.sh/), [OpenDevin](https://github.com/OpenDevin/OpenDevin), and the magic of local-first agents like Claude with MCP.

---

