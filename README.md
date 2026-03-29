<p align="center">
  <a href="https://x.com/Tridib2510">
    <img src="https://img.shields.io/badge/-@Tridib2510-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter">
  </a>
  <a href="https://www.youtube.com/@noobbhai7369">
    <img src="https://img.shields.io/badge/-@noobbhai7369-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube">
  </a>
  <a href="https://discord.gg/tridib0311">
    <img src="https://img.shields.io/badge/-tridib0311-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord">
  </a>
</p>

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

[![Watch the demo](https://img.youtube.com/vi/089bAwjMExM/maxresdefault.jpg)](https://youtu.be/089bAwjMExM?si=UDEbEZZUVNne_yvs)
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
-   🌐 Webpage analysis using BeautifulSoup (structure, content, links, images, forms)
-   🖼️ Image analysis using Gemini 2.5 Flash model
-   📊 Token usage tracking (displays prompt tokens, response tokens, and total usage)

------------------------------------------------------------------------

# 🧱 Tech Stack
-   Gemini SDK
-   Agentic AI architecture
-   Colorama
-   tkinter
-   BeautifulSoup4
-   Requests

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
    │   │   ├── execution
    │   │   │   ├── run_python_file.py
    │   │   │   └── run_react_app.py
    │   │   │
    │   │   ├── dependencies
    │   │   │   ├── install_dependencies.py
    │   │   │   └── install_python_dependencies.py
    │   │   │
    │   │   ├── project_creation
    │   │   │   └── createReactApp.py
    │   │   │
    │   │   ├── image_analysis
    │   │   │   └── analyzeImage.py
    │   │   │
    │   │   ├── web_analysis
    │   │   │   └── analyzeWebpage.py
    │   │   │
    │   │   └── executeFunctions.py
    │   │
    │   ├── utils
    │   │   └── file_dialog.py
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

## 2️⃣ Create virtual environment

``` powershell
uv venv
```

------------------------------------------------------------------------

## 3️⃣ Activate virtual environment

**PowerShell:**
``` powershell
.venv\Scripts\Activate.ps1
```

**CMD:**
``` cmd
.venv\Scripts\activate.bat
```

**Git Bash / WSL:**
``` bash
source .venv/bin/activate
```

------------------------------------------------------------------------

## 4️⃣ Install dependencies

``` powershell
uv pip install -r requirements.txt
```

------------------------------------------------------------------------

## 5️⃣ Install project tools

``` powershell
uv tool install .
```

------------------------------------------------------------------------

# ▶️ Running NeuroCode

Run the AI coding assistant:

``` powershell
neurocode
```

Example prompts:

- List all files in this directory
- Create a new Python file called test.py
- Analyze the structure of https://example.com
- Extract all links from https://example.com
- Analyze the forms on https://httpbin.org/forms/post
- Select an image for analysis
- Create a React app with Vite
- Install dependencies for a React project

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
-   Enhanced webpage replication features

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
