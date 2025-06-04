Here’s the full `README.md` content in clean, copy-pastable Markdown format — updated with the **`uv run mcp install file_tools.py`** step clearly explained:

---

````markdown
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

## 🛠 How to Use

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/devmind.git
cd devmind
````

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

### 4. Register tools with Claude via MCP

Install your tool into Claude by running:

```bash
uv run mcp install file_tools.py
```

You’ll see a success message like:

```
INFO     Added server 'file_tools' to Claude config
```

---

## 🧠 Connect to Claude Desktop

1. Open Claude Desktop.
2. Go to `Settings → Developer`.
3. Add a new tool:

   * **Command**: path to `uv` (typically `/Users/yourname/.venv/bin/uv`)
   * **Arguments**:

     ```bash
     run --with mcp[cli] mcp run /full/path/to/file_tools.py
     ```
4. Save the tool.

Claude should show a **green dot (🟢)** for “Connected.”

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
* [x] File search in common directories
* [ ] File delete, rename, and move tools
* [ ] Create full folder/project templates via prompts
* [ ] Summarize or extract from existing files
* [ ] Add fuzzy filename search (`notes.txt` ≈ `my_notes_backup.txt`)

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

## 📝 License

MIT

```

---

You’re good to go — paste this straight into `README.md`. Let me know when you're ready for the next tool, or want to test commands in Claude.
```
