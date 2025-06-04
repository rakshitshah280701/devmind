<p align="center">
<img width="409" alt="Screenshot 2025-06-04 at 12 26 16 AM" src="https://github.com/user-attachments/assets/5baacc56-c184-4077-baa6-eb204090ba14" />
</p>

# 🧠 DevMind — Developer Assistant with Claude + MCP

DevMind is a local-first developer productivity agent powered by [Claude Desktop](https://www.anthropic.com/index/claude-desktop) and the Model Context Protocol (MCP). It lets you **create**, **locate**, and soon **edit or delete files** using natural language — like a coding co-pilot that understands your desktop.

---

## ⚙️ Tools Available

### ✅ `create_file`
Create a file at a specific location with any content you want.

> Example:  
> “Create a file named `hello.txt` with content `Hello World!` in the DevMind folder on Desktop.”

### 🔍 `find_file`
Searches your **Desktop**, **Documents**, and **Downloads** folders to locate a file by name.

> Example:  
> “Where is `notes.txt`?”

---

### ✍️ `edit_file`
Edit any file using the following modes:
- `append` – Add content to the end
- `replace_all` – Overwrite entire file
- `replace_line` – Replace a specific line

> _"Add ‘Rakshit Shah’ at the end of `hello.txt`."_  
> _"Replace line 3 in `config.yaml`."_

---

### ❌ `delete_file`
Delete a specific file by path.

> _"Delete `notes.txt` from the Desktop."_  

---

### 🚚 `move_file`
Move a file from one location to another.

> _"Move `test.py` to the Documents folder."_

---

### 📝 `rename_file`
Rename a file to a new name or path.

> _"Rename `draft.txt` to `final.txt`."_  
> _"Rename `example.txt` to `notes/archived.txt`."_

---

### 📄 `summarize_file`
Reads the **entire** file content and sends it to Claude for summarization (no truncation).

> _"Summarize the file `strategy.md`."_  

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
* [x] File and Folder search in common directories
* [x] File delete, rename, and move tools
* [x] Summarize or extract from existing files
* [ ] Create full folder/project templates via prompts


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

