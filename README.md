# 🧠 NeuroCode -- AI Code Editor powered by Gemini

NeuroCode is an **AI‑powered coding assistant and terminal code editor**
inspired by tools like **Claude Code**.

It uses **Agentic AI with the Gemini SDK** to analyze code, modify
files, execute scripts, and assist with development workflows directly
from the terminal.

The goal of NeuroCode is to create a **lightweight AI developer
assistant** that can interact with your codebase using structured tools.

------------------------------------------------------------------------

# 🎥 Demo

Watch the demo on YouTube:

[https://youtu.be/T-roQFdVc0U?si=MsGiVAKBdujInboY]
------------------------------------------------------------------------

# 🚀 Features

-   🤖 Agentic AI coding assistant
-   🧠 Powered by Gemini SDK
-   📂 File system tools for reading and modifying files
-   ▶️ Execute Python files directly from the agent
-   🧩 Modular tool architecture
-   🎨 Colored terminal output using Colorama
-   📁 Safe working‑directory based file operations
-   ⚡ Lightweight and fast

------------------------------------------------------------------------

# 🧱 Tech Stack

-   Python
-   Gemini SDK
-   Agentic AI architecture
-   Colorama
-   UV Python package manager
-   python-dotenv

------------------------------------------------------------------------

# 📂 Project Structure

    NeuroCode
    │
    ├── neurocode
    │   ├── functions
    │   │   ├── file_operations
    │   │   │   ├── getFilesInfo.py
    │   │   │   ├── getFilesContent.py
    │   │   │   ├── writeIntoFile.py
    │   │   │   └── createFolderAndFile.py
    │   │   │
    │   │   └── execution
    │   │       └── run_python_file.py
    │   │
    │   └── main.py
    │
    ├── requirements.txt
    ├── pyproject.toml
    └── README.md

------------------------------------------------------------------------

# ⚙️ Installation

## 1️⃣ Clone the repository

``` bash
git clone https://github.com/Tridib2510/NeuroCode.git
cd NeuroCode
```

------------------------------------------------------------------------

# 🧪 Setting up the Environment (Using UV)

This project uses **uv** as the Python package manager.

### Install UV (PowerShell)

``` powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:

``` powershell
uv --version
```

------------------------------------------------------------------------

## 2️⃣ Initialize UV

``` powershell
uv init
```

------------------------------------------------------------------------

## 3️⃣ Install dependencies

``` powershell
uv add -r requirements.txt
```

------------------------------------------------------------------------

## 4️⃣ Install project tools

``` powershell
uv tool install .
```

------------------------------------------------------------------------

# ▶️ Running NeuroCode

Run the AI coding assistant:

``` powershell
neurocode
```

Example prompt:

    List all files in this directory

Or:

    Create a new Python file called test.py

------------------------------------------------------------------------

# 🧠 How It Works

NeuroCode uses an **Agentic AI architecture** where the Gemini model can
call tools such as:

  Tool                  Purpose
  --------------------- ---------------------------
  getFilesInfo          List files in a directory
  getFilesContent       Read file contents
  writeIntoFile         Write code into files
  createFolderAndFile   Create files and folders
  run_python_file       Execute Python scripts

The AI agent decides **which tool to call based on user prompts**.

------------------------------------------------------------------------

# 🛠 Example Workflow

User prompt:

    Create a Flask app in app.py

Agent workflow:

1.  Generate code using Gemini
2.  Call writeIntoFile tool
3.  Save the generated code
4.  Optionally execute it using run_python_file

------------------------------------------------------------------------

# 📌 Future Improvements

-   Code editing diff view
-   Multi‑file refactoring
-   Codebase search
-   Plugin tool ecosystem
-   Web UI editor
-   LSP integration

------------------------------------------------------------------------

# 🤝 Contributing

Contributions are welcome.

1.  Fork the repository
2.  Create a feature branch
3.  Submit a Pull Request

------------------------------------------------------------------------

# ⭐ Support

If you like this project:

⭐ Star the repository\
🍴 Fork the repo\
📢 Share it with others

------------------------------------------------------------------------

# 📜 License

This project is licensed under the **MIT License**.
