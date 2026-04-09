import os
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFrame, QListWidget,
    QComboBox, QDialog, QSizePolicy, QScrollArea, QSplitter
)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QFont, QAction, QIcon, QTextCursor

# Modern color palette
COLORS = {
    "bg_primary": "#0d1117",
    "bg_secondary": "#161b22",
    "bg_tertiary": "#21262d",
    "accent": "#000000",
    "accent_hover": "#333333",
    "success": "#ffffff",
    "warning": "#888888",
    "error": "#ffffff",
    "text_primary": "#f0f6fc",
    "text_secondary": "#8b949e",
    "text_muted": "#484f58",
    "border": "#30363d",
    "user_msg": "#7ee787",
    "bot_msg": "#f0f6fc",
    "func_msg": "#8b949e",
}


def apply_dark_stylesheet(app):
    """Apply dark theme stylesheet to the application."""
    return """
        QMainWindow {
            background-color: #0d1117;
        }
        QWidget {
            background-color: #0d1117;
            color: #f0f6fc;
            font-family: "Segoe UI", sans-serif;
        }
        QFrame#card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
        }
        QFrame#input_container {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
        }
        QTextEdit {
            background-color: #0d1117;
            color: #f0f6fc;
            border: none;
            padding: 15px;
            font-family: "Cascadia Code", "Consolas", monospace;
            font-size: 10pt;
            selection-background-color: #58a6ff;
        }
        QLineEdit {
            background-color: #21262d;
            color: #f0f6fc;
            border: none;
            border-radius: 6px;
            padding: 10px 15px;
            font-size: 10pt;
        }
        QLineEdit:focus {
            border: 1px solid #58a6ff;
        }
        QPushButton {
            background-color: #000000;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            min-width: 80px;
            min-height: 36px;
        }
        QPushButton:hover {
            background-color: #333333;
        }
        QPushButton:disabled {
            background-color: #484f58;
            color: #8b949e;
        }
        QPushButton#secondary {
            background-color: #21262d;
            color: #f0f6fc;
        }
        QPushButton#secondary:hover {
            background-color: #30363d;
        }
        QLabel {
            color: #f0f6fc;
        }
        QLabel#muted {
            color: #8b949e;
        }
        QLabel#header {
            font-size: 14pt;
            font-weight: bold;
        }
        QListWidget {
            background-color: #21262d;
            color: #f0f6fc;
            border: none;
            border-radius: 6px;
            padding: 5px;
        }
        QListWidget::item:selected {
            background-color: #000000;
        }
        QComboBox {
            background-color: #21262d;
            color: #f0f6fc;
            border: none;
            border-radius: 6px;
            padding: 8px 15px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: #21262d;
            color: #f0f6fc;
            selection-background-color: #000000;
        }
        QScrollBar:vertical {
            background-color: #161b22;
            width: 8px;
            border: none;
        }
        QScrollBar::handle:vertical {
            background-color: #30363d;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #484f58;
        }
        QScrollBar:horizontal {
            background-color: #161b22;
            height: 8px;
            border: none;
        }
        QScrollBar::handle:horizontal {
            background-color: #30363d;
            border-radius: 4px;
        }
        QDialog {
            background-color: #0d1117;
        }
        QStatusBar {
            background-color: #161b22;
            color: #8b949e;
        }
    """


class ConnectorsDialog(QDialog):
    """Dialog for managing MCP server connections."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MCP Connectors")
        self.setMinimumSize(600, 450)
        self.setModal(True)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Header
        header = QLabel("⚡ MCP Connectors")
        header.setObjectName("header")
        layout.addWidget(header)

        # Main content splitter
        splitter = QSplitter(Qt.Horizontal)

        # Left panel - Server list
        list_frame = QFrame()
        list_frame.setObjectName("card")
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(10, 10, 10, 10)

        list_title = QLabel("Connected Servers")
        list_title.setStyleSheet("font-weight: bold;")
        list_layout.addWidget(list_title)

        self.server_list = QListWidget()
        list_layout.addWidget(self.server_list)

        splitter.addWidget(list_frame)

        # Right panel - Add new connection
        add_frame = QFrame()
        add_frame.setObjectName("card")
        add_layout = QVBoxLayout(add_frame)
        add_layout.setContentsMargins(10, 10, 10, 10)

        add_title = QLabel("Add New Connection")
        add_title.setStyleSheet("font-weight: bold;")
        add_layout.addWidget(add_title)

        # Name field
        name_label = QLabel("Name:")
        name_label.setStyleSheet("color: #8b949e;")
        add_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Filesystem Server")
        add_layout.addWidget(self.name_input)

        # URL field
        url_label = QLabel("MCP URL:")
        url_label.setStyleSheet("color: #8b949e;")
        add_layout.addWidget(url_label)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("e.g., http://localhost:3000")
        add_layout.addWidget(self.url_input)

        # Type field
        type_label = QLabel("Type:")
        type_label.setStyleSheet("color: #8b949e;")
        add_layout.addWidget(type_label)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["stdio", "sse", "http"])
        add_layout.addWidget(self.type_combo)

        # API Key field (optional)
        api_key_label = QLabel("API Key (optional):")
        api_key_label.setStyleSheet("color: #8b949e;")
        add_layout.addWidget(api_key_label)
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Leave empty if not required")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        add_layout.addWidget(self.api_key_input)

        add_layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self._add_connection)
        btn_layout.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.setObjectName("secondary")
        self.disconnect_btn.clicked.connect(self._disconnect_selected)
        btn_layout.addWidget(self.disconnect_btn)

        add_layout.addLayout(btn_layout)

        # Status
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #8b949e;")
        add_layout.addWidget(self.status_label)

        splitter.addWidget(add_frame)
        splitter.setSizes([300, 300])

        layout.addWidget(splitter)

    def _add_connection(self):
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()
        server_type = self.type_combo.currentText()
        api_key = self.api_key_input.text().strip()

        if not name or not url:
            self.status_label.setText("Name and URL are required")
            self.status_label.setStyleSheet("color: #ff6b6b;")
            return

        # Store server info for later use (including empty api_key)
        display = f"{name} ({server_type}) - {url}"
        self.server_list.addItem(display)
        self.status_label.setText(f"Added: {name}")
        self.status_label.setStyleSheet("color: #7ee787;")

        self.name_input.clear()
        self.url_input.clear()
        self.api_key_input.clear()

    def _disconnect_selected(self):
        current_row = self.server_list.currentRow()
        if current_row >= 0:
            self.server_list.takeItem(current_row)
            self.status_label.setText("Disconnected")
            self.status_label.setStyleSheet("color: #8b949e;")
        else:
            self.status_label.setText("Select a server first")
            self.status_label.setStyleSheet("color: #ff6b6b;")


class NeuroCodeWindow(QMainWindow):
    """Main NeuroCode window with professional PySide6 UI."""

    def __init__(self):
        super().__init__()
        self.client = None
        self.call_function = None
        self.available_functions = None
        self.config = None
        self.selected_image_path = None
        self.processing = False
        self.api_key_verified = False
        self.api_key = ""

        # Token usage tracking
        self.total_prompt_tokens = 0
        self.total_candidates_tokens = 0
        self.total_tokens = 0
        self.request_count = 0
        self.messages = []

        self.setWindowTitle("NeuroCode")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 750)

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Create the main UI structure."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)

        # Left panel - Chat interface
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(10)

        # Chat output area
        chat_frame = QFrame()
        chat_frame.setObjectName("card")
        chat_layout = QVBoxLayout(chat_frame)
        chat_layout.setContentsMargins(0, 0, 0, 0)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Cascadia Code", 10))
        chat_layout.addWidget(self.output_text)

        left_layout.addWidget(chat_frame, 1)

        # Input area
        input_container = QFrame()
        input_container.setObjectName("input_container")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(12, 8, 12, 8)

        self.input_entry = QLineEdit()
        self.input_entry.setPlaceholderText("Enter your prompt...")
        self.input_entry.returnPressed.connect(self.on_submit)
        input_layout.addWidget(self.input_entry, 1)

        # Buttons
        self.select_image_btn = QPushButton("🖼 Image")
        self.select_image_btn.setObjectName("secondary")
        self.select_image_btn.clicked.connect(self.select_image)
        input_layout.addWidget(self.select_image_btn)

        self.clear_image_btn = QPushButton("✕ Clear")
        self.clear_image_btn.setObjectName("secondary")
        self.clear_image_btn.clicked.connect(self.clear_image)
        input_layout.addWidget(self.clear_image_btn)

        self.connectors_btn = QPushButton("⚡ Connectors")
        self.connectors_btn.setObjectName("secondary")
        self.connectors_btn.clicked.connect(self.open_connectors)
        input_layout.addWidget(self.connectors_btn)

        self.submit_btn = QPushButton("Send →")
        self.submit_btn.clicked.connect(self.on_submit)
        input_layout.addWidget(self.submit_btn)

        left_layout.addWidget(input_container)

        splitter.addWidget(left_panel)

        # Right panel - Configuration
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        config_frame = QFrame()
        config_frame.setObjectName("card")
        config_layout = QVBoxLayout(config_frame)

        # Header
        config_header = QLabel("⚙️ Configuration")
        config_header.setObjectName("header")
        config_layout.addWidget(config_header)

        # API Key section
        api_label = QLabel("Gemini API Key:")
        config_layout.addWidget(api_label)

        self.api_key_entry = QLineEdit()
        self.api_key_entry.setPlaceholderText("Enter API Key...")
        self.api_key_entry.setEchoMode(QLineEdit.Password)
        config_layout.addWidget(self.api_key_entry)

        # Status
        status_layout = QHBoxLayout()
        self.api_status_indicator = QLabel("●")
        self.api_status_indicator.setStyleSheet("color: #484f58;")
        status_layout.addWidget(self.api_status_indicator)

        self.api_status_label = QLabel("Not connected")
        self.api_status_label.setStyleSheet("color: #484f58;")
        status_layout.addWidget(self.api_status_label)
        status_layout.addStretch()

        config_layout.addLayout(status_layout)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.verify_api_key)
        config_layout.addWidget(self.connect_btn)

        self.key_error = QLabel("")
        self.key_error.setStyleSheet("color: #ff6b6b;")
        config_layout.addWidget(self.key_error)

        config_layout.addSpacing(20)

        # Token Usage section
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #30363d;")
        config_layout.addWidget(separator)

        usage_header = QLabel("📊 Token Usage")
        usage_header.setStyleSheet("font-weight: bold;")
        config_layout.addWidget(usage_header)

        self.usage_requests_label = QLabel("Requests: 0")
        self.usage_requests_label.setStyleSheet("color: #8b949e;")
        config_layout.addWidget(self.usage_requests_label)

        self.usage_prompt_label = QLabel("Prompt Tokens: 0")
        self.usage_prompt_label.setStyleSheet("color: #8b949e;")
        config_layout.addWidget(self.usage_prompt_label)

        self.usage_response_label = QLabel("Response Tokens: 0")
        self.usage_response_label.setStyleSheet("color: #8b949e;")
        config_layout.addWidget(self.usage_response_label)

        self.usage_total_label = QLabel("Total Tokens: 0")
        self.usage_total_label.setStyleSheet("font-weight: bold;")
        config_layout.addWidget(self.usage_total_label)

        config_layout.addStretch()

        # Instructions
        instructions = QLabel("Get your API key from:\nconsole.cloud.google.com")
        instructions.setStyleSheet("color: #484f58; font-size: 8pt;")
        config_layout.addWidget(instructions)

        right_layout.addWidget(config_frame, 1)

        splitter.addWidget(right_panel)
        splitter.setSizes([750, 350])
        splitter.setStretchFactor(0, 1)

        main_layout.addWidget(splitter)

        # Status bar
        self.statusBar().showMessage("Ready")

    def _apply_styles(self):
        """Apply dark theme stylesheet."""
        self.setStyleSheet(apply_dark_stylesheet(self))

    def log(self, text, tag=None):
        """Log text to the output area."""
        color = COLORS["text_primary"]
        if tag == "user":
            color = COLORS["user_msg"]
        elif tag == "bot":
            color = COLORS["bot_msg"]
        elif tag == "function":
            color = COLORS["func_msg"]

        self.output_text.moveCursor(QTextCursor.End)
        if color != COLORS["text_primary"]:
            self.output_text.insertHtml(f'<span style="color: {color};">{text}</span>')
        else:
            self.output_text.insertPlainText(text)
        self.output_text.moveCursor(QTextCursor.End)

    def log_user(self, text):
        self.log(f"\n{text}\n", "user")

    def log_bot(self, text):
        self.log(f"\n{text}\n", "bot")

    def log_function(self, text):
        self.log(f"\n{text}\n", "function")

    def log_status(self, text, status="info"):
        colors = {"info": "#8b949e", "success": "#7ee787",
                  "error": "#ff6b6b", "warning": "#8b949e"}
        self.statusBar().showMessage(text)
        self.statusBar().setStyleSheet(f"color: {colors.get(status, '#8b949e')};")

    def select_image(self):
        from PySide6.QtWidgets import QFileDialog
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if image_path:
            self.selected_image_path = image_path
            self.statusBar().showMessage(f"📷 {os.path.basename(image_path)}")
            self.log_function(f"[Image selected: {image_path}]")

    def clear_image(self):
        self.selected_image_path = None
        self.statusBar().showMessage("No image")
        self.log_function("[Image cleared]")

    def open_connectors(self):
        dialog = ConnectorsDialog(self)
        dialog.exec()

    def verify_api_key(self):
        """Verify API key and initialize the client."""
        api_key = self.api_key_entry.text().strip()

        if not api_key:
            self.key_error.setText("API Key cannot be empty!")
            return

        self.key_error.setText("Initializing...")

        from google.genai import types
        from google import genai
        from neurocode.utils import select_image_file
        from neurocode.functions.execution.run_python_file import schema_run_python_file
        from neurocode.functions.file_operations.getFilesInfo import schema_get_files_info
        from neurocode.functions.file_operations.writeIntoFile import schema_write_file
        from neurocode.functions.file_operations.getFilesContent import schema_get_files_content
        from neurocode.functions.file_operations.createFolderAndFile import schema_create_file
        from neurocode.functions.project_creation.createReactApp import schema_create_react_vite_app
        from neurocode.functions.execution.run_react_app import schema_run_react_app
        from neurocode.functions.dependencies.install_dependencies import schema_install_dependencies
        from neurocode.functions.dependencies.install_python_dependencies import (
            schema_create_uv_environment, schema_install_python_dependencies
        )
        from neurocode.functions.image_analysis.analyzeImage import schema_analyze_image
        from neurocode.functions.executeFunctions import call_function
        from neurocode.functions.mcp.mcp_connection import schema_connect_mcp_server, schema_list_mcp_tools, connect_mcp_server
        import asyncio

        try:
            self.client = genai.Client(api_key=api_key)
            self.call_function = call_function

            self.available_functions = types.Tool(
                function_declarations=[
                    schema_get_files_info,
                    schema_write_file,
                    schema_run_python_file,
                    schema_get_files_content,
                    schema_create_file,
                    schema_create_react_vite_app,
                    schema_run_react_app,
                    schema_install_dependencies,
                    schema_create_uv_environment,
                    schema_install_python_dependencies,
                    schema_analyze_image,
                    schema_connect_mcp_server,
                    schema_list_mcp_tools,
                ]
            )

            self.config = types.GenerateContentConfig(
                tools=[self.available_functions],
                system_instruction=self._get_system_prompt()
            )

            self.api_key_verified = True
            self.api_status_indicator.setStyleSheet("color: #7ee787;")
            self.api_status_label.setText("Connected")
            self.api_status_label.setStyleSheet("color: #7ee787;")
            self.connect_btn.setText("Connected")
            self.connect_btn.setEnabled(False)
            self.log("NeuroCode started. Enter your prompt above.\n")

        except Exception as e:
            self.key_error.setText(f"Error: {str(e)}")

    def _get_system_prompt(self):
        return """
You are an advanced AI coding agent responsible for completing programming tasks using available tools.

Your goal is to FULLY implement the user's request, not just scaffold a project.

Core rules:

1. Always analyze the user's request and determine what files, code, and structure are required.

2. If the user asks for an application (for example a React app), follow this workflow:
    - First create the project if it does not exist.
    - Then inspect the project files.
    - Modify or write code inside the appropriate files to implement the requested functionality.
    - Only run the application after the code implementation is complete.

3. Do NOT assume the default template already satisfies the user's request. You must modify files when functionality is requested.

4. When implementing features:
    - Use getFilesInfo to inspect directories if needed.
    - Use getFilesContent to read files before modifying them.
    - Use write_file to update or create code files.

5. If a user asks for a specific application (example: calculator, todo app, weather app), you must implement the UI and logic inside the React project files (typically App.jsx or App.tsx).

6. Only start the development server (run_react_app) AFTER:
    - the project exists
    - dependencies are installed
    - the necessary code implementation is complete.

7. Prefer completing the task in minimum number of tool calls, but do not skip required implementation steps.

8. Never repeat the same tool call if the task has already been completed.

9. Never use absolute paths for file operations (get_files_info, get_file_content, write_file, create_file, etc.). All paths must be relative to the working directory.

10. For image analysis, you can use absolute paths (e.g., from file selection) or relative paths within the working directory.

Available capabilities:
- List files and directories
- Read file contents
- Write files
- Run Python scripts
- Create folders and files
- Create React apps
- Install npm dependencies
- Run React apps with npm run dev
- Create UV Python virtual environments
- Install Python dependencies using UV
- Analyze images using Gemini 2.5 Flash model (image classification, detailed description)
- Analyze webpages using beautiful soup
- Connect to MCP servers and call their tools
    """

    def on_submit(self):
        if self.processing:
            return

        if not self.api_key_verified:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Not Ready", "Please enter your API key first.")
            return

        prompt = self.input_entry.text().strip()
        if not prompt:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Empty Prompt", "Please enter a prompt.")
            return

        self.input_entry.clear()

        if self.selected_image_path:
            prompt = f"{prompt}\n\nImage path: {self.selected_image_path}"

        self.log_status("Processing...", "warning")
        self.log("\n" + "─" * 50, "muted")
        self.log(f"\nYou: {prompt}\n", "user")

        self.processing = True
        self.submit_btn.setEnabled(False)
        self.log_status("Thinking...", "warning")

        self.worker = RequestWorker(self, prompt)
        self.worker.finished.connect(self._on_requestFinished)
        self.worker.function_started.connect(self._on_functionStarted)
        self.worker.function_args.connect(self._on_functionArgs)
        self.worker.error.connect(self._on_requestError)
        self.worker.start()

    def _on_requestFinished(self, response_text, prompt_tokens, response_tokens):
        """Handle the completion of a request."""
        self.messages.append(response_text)

        if prompt_tokens > 0 or response_tokens > 0:
            self.update_usage_display(prompt_tokens, response_tokens)

        self.processing = False
        self.submit_btn.setEnabled(True)
        self.log_bot(f"\nNeuroCode: {response_text}")
        self.log_status("Ready", "success")

    def _on_functionStarted(self, function_name):
        """Display the function being executed."""
        self.log_function(f"\n[{function_name}]\n")
        self.log_status(f"Executing {function_name}...", "warning")

    def _on_functionArgs(self, args):
        """Display the function arguments."""
        for arg_name, arg_value in args.items():
            self.log_function(f"  └─ {arg_name}: {arg_value}")

    def _on_requestError(self, error_message):
        """Handle request errors."""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", f"Request failed: {error_message}")
        self.processing = False
        self.submit_btn.setEnabled(True)
        self.log_status("Error occurred", "error")

    def update_usage_display(self, prompt_tokens=0, response_tokens=0):
        """Update the token usage display."""
        self.total_prompt_tokens += prompt_tokens
        self.total_candidates_tokens += response_tokens
        self.total_tokens += prompt_tokens + response_tokens
        self.request_count += 1

        self.usage_requests_label.setText(f"Requests: {self.request_count}")
        self.usage_prompt_label.setText(f"Prompt Tokens: {self.total_prompt_tokens:,}")
        self.usage_response_label.setText(f"Response Tokens: {self.total_candidates_tokens:,}")
        self.usage_total_label.setText(f"Total Tokens: {self.total_tokens:,}")


class RequestWorker(QThread):
    """Worker thread for processing API requests."""

    finished = Signal(str, int, int)
    error = Signal(str)
    function_started = Signal(str)
    function_args = Signal(dict)

    def __init__(self, window, prompt):
        super().__init__()
        self.window = window
        self.prompt = prompt

    def run(self):
        from google.genai import types

        MAX_ITER = 10
        self.window.messages.append(
            types.Content(role="user", parts=[types.Part(text=self.prompt)])
        )

        try:
            for i in range(MAX_ITER):
                response = self.window.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=self.window.messages,
                    config=self.window.config
                )

                for candidate in response.candidates:
                    if candidate is None or candidate.content is None:
                        continue
                    self.window.messages.append(candidate.content)

                if response.function_calls:
                    for function_call_part in response.function_calls:
                        self.function_started.emit(f"⚙️ Calling function: {function_call_part.name}")
                        self.window.log_function(f"\n[FUNCTION: {function_call_part.name}]")
                        if function_call_part.args:
                            self.function_args.emit(function_call_part.args)
                        result = self.window.call_function(function_call_part, None)
                        self.window.messages.append(result)
                else:
                    prompt_tokens = 0
                    response_tokens = 0
                    if response.usage_metadata:
                        prompt_tokens = response.usage_metadata.prompt_token_count or 0
                        response_tokens = response.usage_metadata.candidates_token_count or 0
                    self.finished.emit(response.text, prompt_tokens, response_tokens)
                    return

        except Exception as e:
            self.error.emit(str(e))


def main():
    print("NeuroCode starting...")

    app = QApplication(sys.argv)

    # Set app icon
    try:
        import pathlib
        package_path = pathlib.Path(sys.modules['neurocode'].__file__).parent
        icon_path = package_path / "images" / "icon.png"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
    except Exception as e:
        print(f"Icon error: {e}")

    window = NeuroCodeWindow()
    window.show()

    print("GUI window created")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
