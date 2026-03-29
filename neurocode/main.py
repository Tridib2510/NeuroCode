import os
import sys
import tkinter as tk
from tkinter import messagebox
# Modern color palette
COLORS = {
    "bg_primary": "#0d1117",      # Deep dark blue-black
    "bg_secondary": "#161b22",    # Slightly lighter panel
    "bg_tertiary": "#21262d",    # Card/input backgrounds
    "accent": "#000000",         # Black accent (buttons)
    "accent_hover": "#333333",    # Dark gray on hover
    "success": "#ffffff",        # White for success
    "warning": "#888888",         # Gray for warnings
    "error": "#ffffff",          # White for errors
    "text_primary": "#f0f6fc",    # White text
    "text_secondary": "#8b949e", # Muted gray text
    "text_muted": "#484f58",      # Very muted
    "border": "#30363d",          # Subtle borders
}


class ModernButton(tk.Canvas):
    """Rounded modern button using Canvas for smooth corners."""

    def __init__(self, parent, text, command, width=100, height=36, color="#000000", **kwargs):
        super().__init__(parent, width=width, height=height, bg=COLORS["bg_secondary"],
                         highlightthickness=0, **kwargs)
        self.command = command
        self.default_color = color
        self.hover_color = COLORS["accent_hover"]
        self.current_color = color
        self.text = text
        self.width = width
        self.height = height

        self._draw()

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _draw(self):
        self.delete("all")
        padding = 3
        self.create_rounded_rectangle(
            padding, padding, self.width - padding, self.height - padding,
            radius=8, fill=self.current_color, outline=""
        )
        self.create_text(
            self.width // 2, self.height // 2,
            text=self.text, fill="white",
            font=("Segoe UI", 10, "bold")
        )

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = []
        for x, y in [(x1 + radius, y1), (x2 - radius, y1),
                     (x2, y1 + radius), (x2, y2 - radius),
                     (x2 - radius, y2), (x1 + radius, y2),
                     (x1, y2 - radius), (x1, y1 + radius)]:
            points.extend([x, y])
        self.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, start=90, extent=90, **kwargs)
        self.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, start=0, extent=90, **kwargs)
        self.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, start=270, extent=90, **kwargs)
        self.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, start=180, extent=90, **kwargs)
        self.create_polygon(points, **kwargs)

    def _on_click(self, event):
        self.command()

    def _on_enter(self, event=None):
        self.current_color = self.hover_color
        self._draw()

    def _on_leave(self, event=None):
        self.current_color = self.default_color
        self._draw()

    def config_state(self, state):
        if state == tk.DISABLED:
            self.current_color = COLORS["text_muted"]
        else:
            self.current_color = self.default_color
        self._draw()


class ModernEntry(tk.Frame):
    """Modern styled entry field with placeholder support."""

    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(parent, bg=COLORS["bg_tertiary"], padx=0, pady=0)
        self.placeholder = placeholder
        self.placeholder_active = True

        self.entry = tk.Entry(
            self, font=("Segoe UI", 11), bg=COLORS["bg_tertiary"],
            fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"],
            relief=tk.FLAT, bd=0, **kwargs
        )
        self.entry.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        self.entry.insert(0, placeholder)
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=COLORS["text_primary"])
            self.placeholder_active = False

    def _on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=COLORS["text_secondary"])
            self.placeholder_active = True

    def get(self):
        if self.placeholder_active:
            return ""
        return self.entry.get()

    def delete(self, *args):
        self.entry.delete(*args)

    def bind(self, sequence, func):
        self.entry.bind(sequence, func)


class NeuroCodeGUI:
    def __init__(self, container):
        self.root = container

        self.client = None
        self.selected_image_path = None
        self.processing = False
        self.api_key_verified = False
        self.api_key = ""

        # Token usage tracking
        self.total_prompt_tokens = 0
        self.total_candidates_tokens = 0
        self.total_tokens = 0
        self.request_count = 0

        # Token usage tracking
        self.total_prompt_tokens = 0
        self.total_candidates_tokens = 0
        self.total_tokens = 0
        self.request_count = 0

        self._create_main_ui()

    def _create_api_key_panel(self, parent):
        """Create API key configuration panel on the right side."""
        api_frame = tk.Frame(parent, bg=COLORS["bg_secondary"], bd=1,
                            highlightbackground=COLORS["border"], highlightthickness=1)
        api_frame.pack(fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)

        # Header
        header = tk.Frame(api_frame, bg=COLORS["bg_tertiary"])
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="⚙️ Configuration",
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["bg_tertiary"],
            fg=COLORS["text_primary"]
        ).pack(pady=10, padx=15, anchor=tk.W)

        # API Key section
        content = tk.Frame(api_frame, bg=COLORS["bg_secondary"])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tk.Label(
            content,
            text="Gemini API Key:",
            font=("Segoe UI", 10),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        ).pack(anchor=tk.W, pady=(10, 5))

        # API Key entry
        self.api_key_entry = ModernEntry(content, placeholder="Enter API Key...")
        self.api_key_entry.config(width=30)
        self.api_key_entry.pack(fill=tk.X, pady=(0, 10))

        # Status indicator
        self.api_status_frame = tk.Frame(content, bg=COLORS["bg_secondary"])
        self.api_status_frame.pack(fill=tk.X, pady=(0, 10))

        self.api_status_indicator = tk.Label(
            self.api_status_frame,
            text="●",
            font=("Segoe UI", 10),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_muted"]
        )
        self.api_status_indicator.pack(side=tk.LEFT)

        self.api_status_label = tk.Label(
            self.api_status_frame,
            text="Not connected",
            font=("Segoe UI", 9),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_muted"]
        )
        self.api_status_label.pack(side=tk.LEFT, padx=(5, 0))

        # Connect button
        self.connect_btn = ModernButton(
            content, text="Connect",
            command=self.verify_api_key,
            width=100, height=36,
            color=COLORS["accent"]
        )
        self.connect_btn.pack(pady=(0, 10))

        # Error message area
        self.key_error = tk.Label(
            content,
            text="",
            font=("Segoe UI", 9),
            bg=COLORS["bg_secondary"],
            fg=COLORS["error"],
            wraplength=250
        )
        self.key_error.pack(pady=(0, 10))

        # Instructions
        tk.Label(
            content,
            text="Get your API key from:\nconsole.cloud.google.com",
            font=("Segoe UI", 8),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_muted"],
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(20, 0))

        # Token Usage section
        separator = tk.Frame(api_frame, bg=COLORS["border"], height=1)
        separator.pack(fill=tk.X, padx=15, pady=(15, 0))

        usage_header = tk.Frame(api_frame, bg=COLORS["bg_secondary"])
        usage_header.pack(fill=tk.X, padx=15, pady=(10, 5))

        tk.Label(
            usage_header,
            text="📊 Token Usage",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        ).pack(anchor=tk.W)

        usage_content = tk.Frame(api_frame, bg=COLORS["bg_secondary"])
        usage_content.pack(fill=tk.X, padx=15, pady=(0, 10))

        self.usage_requests_label = tk.Label(
            usage_content,
            text="Requests: 0",
            font=("Segoe UI", 9),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"]
        )
        self.usage_requests_label.pack(anchor=tk.W, pady=(0, 2))

        self.usage_prompt_label = tk.Label(
            usage_content,
            text="Prompt Tokens: 0",
            font=("Segoe UI", 9),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"]
        )
        self.usage_prompt_label.pack(anchor=tk.W, pady=(0, 2))

        self.usage_response_label = tk.Label(
            usage_content,
            text="Response Tokens: 0",
            font=("Segoe UI", 9),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"]
        )
        self.usage_response_label.pack(anchor=tk.W, pady=(0, 2))

        self.usage_total_label = tk.Label(
            usage_content,
            text="Total Tokens: 0",
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"]
        )
        self.usage_total_label.pack(anchor=tk.W, pady=(0, 2))

    def verify_api_key(self):
        """Verify API key and initialize the client."""
        api_key = self.api_key_entry.get().strip()

        if not api_key:
            self.key_error.config(text="API Key cannot be empty!")
            return

        self.key_error.config(text="Initializing...")
        self.api_key = api_key

        # Defer heavy imports until API key is provided
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
        from neurocode.functions.dependencies.install_python_dependencies import schema_create_uv_environment, schema_install_python_dependencies
        from neurocode.functions.image_analysis.analyzeImage import schema_analyze_image
        from neurocode.functions.executeFunctions import call_function

        try:
            self.client = genai.Client(api_key=api_key)
            self.call_function = call_function

            # Store schemas for later
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
                ]
            )

            self.config = types.GenerateContentConfig(
                tools=[self.available_functions],
                system_instruction=self._get_system_prompt()
            )

            self.api_key_verified = True
            self.api_status_indicator.config(fg=COLORS["success"])
            self.api_status_label.config(text="Connected", fg=COLORS["success"])
            self.connect_btn.config(text="Connected")
            self.connect_btn.config_state(tk.DISABLED)
            self.log("NeuroCode started. Enter your prompt above.\n")

        except Exception as e:
            self.key_error.config(text=f"Error: {str(e)}")

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

7. Prefer completing the task in the minimum number of tool calls, but do not skip required implementation steps.

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
    """

    def _create_main_ui(self):
        """Create the main split-layout interface with chat and config panels."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.selected_image_path = None
        self.processing = False
        self.messages = []

        # Main container with side-by-side panels
        main_container = tk.PanedWindow(self.root, bg=COLORS["bg_primary"],
                                        sashrelief=tk.FLAT, sashwidth=2,
                                        showhandle=False)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left panel - Chat interface
        left_panel = tk.Frame(main_container, bg=COLORS["bg_primary"])
        main_container.add(left_panel, width=700)

        # Chat content area
        self._create_main_content(left_panel)
        self._create_input_area(left_panel)

        # Right panel - Configuration
        right_panel = tk.Frame(main_container, bg=COLORS["bg_primary"])
        main_container.add(right_panel, width=350)
        self._create_api_key_panel(right_panel)

        # Status bar at bottom
        self._create_status_bar()

        self.log("NeuroCode started. Enter your prompt above.\n")

    def _create_main_content(self, parent):
        content_frame = tk.Frame(parent, bg=COLORS["bg_primary"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        text_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"], bd=1,
                              highlightbackground=COLORS["border"], highlightthickness=1)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Cascadia Code", 10),
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["text_primary"],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=10,
            state=tk.DISABLED
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.output_text.tag_configure("user", foreground="#7ee787", font=("Cascadia Code", 10, "bold"))
        self.output_text.tag_configure("bot", foreground="#f0f6fc", font=("Cascadia Code", 10, "bold"))
        self.output_text.tag_configure("function", foreground=COLORS["warning"], font=("Cascadia Code", 10, "italic"))
        self.output_text.tag_configure("success", foreground=COLORS["success"])
        self.output_text.tag_configure("error", foreground=COLORS["error"])
        self.output_text.tag_configure("muted", foreground=COLORS["text_secondary"])

        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview,
                                  bg=COLORS["bg_secondary"], troughcolor=COLORS["bg_primary"],
                                  activebackground=COLORS["border"])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)

    def _create_status_bar(self):
        status_frame = tk.Frame(self.root, bg=COLORS["bg_secondary"], height=28)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 5))
        status_frame.tkraise()

        self.status_indicator = tk.Label(
            status_frame,
            text="●",
            font=("Segoe UI", 8),
            bg=COLORS["bg_secondary"],
            fg=COLORS["success"]
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(10, 5))

        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("Segoe UI", 9),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"]
        )
        self.status_label.pack(side=tk.LEFT)

        self.image_status = tk.Label(
            status_frame,
            text="No image",
            font=("Segoe UI", 9),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_muted"]
        )
        self.image_status.pack(side=tk.RIGHT, padx=10)

    def _create_input_area(self, parent):
        input_container = tk.Frame(parent, bg=COLORS["bg_secondary"], bd=1,
                                   highlightbackground=COLORS["border"], highlightthickness=1)
        input_container.pack(fill=tk.X, padx=10, pady=(0, 10))

        input_frame = tk.Frame(input_container, bg=COLORS["bg_secondary"])
        input_frame.pack(fill=tk.X, padx=12, pady=8)

        self.input_entry = ModernEntry(input_frame, placeholder="Enter your prompt...")
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        self.input_entry.bind("<Return>", self.on_submit)

        buttons_frame = tk.Frame(input_frame, bg=COLORS["bg_secondary"])
        buttons_frame.pack(side=tk.RIGHT, padx=(10, 0))

        self.select_image_btn = ModernButton(
            buttons_frame, text="🖼 Image",
            command=self.select_image,
            width=80, height=36,
            color=COLORS["bg_tertiary"]
        )
        self.select_image_btn.pack(side=tk.RIGHT, padx=3)

        self.clear_image_btn = ModernButton(
            buttons_frame, text="✕ Clear",
            command=self.clear_image,
            width=70, height=36,
            color=COLORS["bg_tertiary"]
        )
        self.clear_image_btn.pack(side=tk.RIGHT, padx=3)

        self.submit_btn = ModernButton(
            buttons_frame, text="Send →",
            command=self.on_submit,
            width=80, height=36,
            color=COLORS["accent"]
        )
        self.submit_btn.pack(side=tk.RIGHT, padx=3)

    def log(self, text, tag=None):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text, tag)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def log_user(self, text):
        self.log(f"\n{text}\n", "user")

    def log_bot(self, text):
        self.log(f"\n{text}\n", "bot")

    def log_function(self, text):
        self.log(f"\n{text}\n", "function")

    def log_status(self, text, status="info"):
        colors = {"info": COLORS["text_secondary"], "success": COLORS["success"],
                  "error": COLORS["error"], "warning": COLORS["warning"]}
        self.status_label.config(text=text, fg=colors.get(status, COLORS["text_secondary"]))

    def select_image(self):
        from neurocode.utils import select_image_file
        image_path = select_image_file()
        if image_path:
            self.selected_image_path = image_path
            self.image_status.config(text=f"📷 {os.path.basename(image_path)}", fg=COLORS["accent"])
            self.log_function(f"[Image selected: {image_path}]")

    def clear_image(self):
        self.selected_image_path = None
        self.image_status.config(text="No image", fg=COLORS["text_muted"])
        self.log_function("[Image cleared]")

    def on_submit(self, event=None):
        if self.processing:
            return

        if not self.api_key_verified:
            messagebox.showwarning("Not Ready", "Please enter your API key first.")
            return

        prompt = self.input_entry.get().strip()
        if not prompt:
            messagebox.showwarning("Empty Prompt", "Please enter a prompt.")
            return

        self.input_entry.delete(0, tk.END)

        if self.selected_image_path:
            prompt = f"{prompt}\n\nImage path: {self.selected_image_path}"

        self.log_status("Processing...", "warning")
        self.log("\n" + "─" * 50, "muted")
        self.log(f"\nYou: {prompt}\n", "user")

        self.processing = True
        self.submit_btn.config_state(tk.DISABLED)
        self.log_status("Thinking...", "warning")

        import threading
        thread = threading.Thread(target=self.process_request, args=(prompt,))
        thread.start()

    def process_request(self, prompt):
        from google.genai import types
        MAX_ITER = 10
        self.messages.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

        try:
            for i in range(MAX_ITER):
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash", contents=self.messages, config=self.config
                )

                for candidate in response.candidates:
                    if candidate is None or candidate.content is None:
                        continue
                    self.messages.append(candidate.content)

                if response.function_calls:
                    for function_call_part in response.function_calls:
                        self.root.after(0, lambda f=function_call_part: self.log_function(f"\n[FUNCTION: {f.name}]"))
                        result = self.call_function(function_call_part, None)
                        self.root.after(0, lambda r=result: self.messages.append(r))
                        self.root.after(0, lambda r=result: self.log_function(f"\nThinking:{r}"))
                        self.root.after(0, lambda n=function_call_part.name: self.log_function(f"[{n} executed]"))
                else:
                    # Extract and update token usage
                    if response.usage_metadata:
                        prompt_tokens = response.usage_metadata.prompt_token_count or 0
                        response_tokens = response.usage_metadata.candidates_token_count or 0
                        self.root.after(0, lambda p=prompt_tokens, r=response_tokens: self.update_usage_display(p, r))
                    self.root.after(0, lambda r=response.text: self.log_bot(f"\nNeuroCode: {r}"))
                    break
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.log_status("Error occurred", "error"))

        self.root.after(0, self.done_processing)

    def update_usage_display(self, prompt_tokens=0, response_tokens=0):
        """Update the token usage display with new values."""
        self.total_prompt_tokens += prompt_tokens
        self.total_candidates_tokens += response_tokens
        self.total_tokens += prompt_tokens + response_tokens
        self.request_count += 1

        self.usage_requests_label.config(text=f"Requests: {self.request_count}")
        self.usage_prompt_label.config(text=f"Prompt Tokens: {self.total_prompt_tokens:,}")
        self.usage_response_label.config(text=f"Response Tokens: {self.total_candidates_tokens:,}")
        self.usage_total_label.config(text=f"Total Tokens: {self.total_tokens:,}")

    def done_processing(self):
        self.processing = False
        self.submit_btn.config_state(tk.NORMAL)
        self.log_status("Ready", "success")


def create_custom_titlebar(root):
    title_bar = tk.Frame(root, bg="#000000", height=40)
    title_bar.pack(fill="x")

    # Enable dragging the window
    def start_drag(event):
        root.x = event.x
        root.y = event.y

    def drag(event):
        delta_x = event.x - root.x
        delta_y = event.y - root.y
        new_x = root.winfo_x() + delta_x
        new_y = root.winfo_y() + delta_y
        root.geometry(f"+{new_x}+{new_y}")

    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", drag)
    title_bar.bind("<Double-Button-1>", lambda e: toggle_maximize() if root.state() != "zoomed" else None)

    # App title
    title_label = tk.Label(
        title_bar,
        text="  NeuroCode",
        bg="#000000",
        fg="white",
        font=("Segoe UI", 10, "bold")
    )
    title_label.pack(side="left", padx=10)
    title_label.bind("<Button-1>", start_drag)
    title_label.bind("<B1-Motion>", drag)

    # Buttons container
    btn_frame = tk.Frame(title_bar, bg="#000000")
    btn_frame.pack(side="right", padx=5)

    # Minimize
    tk.Button(btn_frame, text="—", bg="#000000", fg="white",
              bd=0, command=lambda: root.iconify()).pack(side="left", padx=5)

    # Maximize / Restore
    def toggle_maximize():
        if root.state() == "zoomed":
            root.state("normal")
        else:
            root.state("zoomed")

    tk.Button(btn_frame, text="⬜", bg="#000000", fg="white",
              bd=0, command=toggle_maximize).pack(side="left", padx=5)

    # Close
    tk.Button(btn_frame, text="✕", bg="#000000", fg="white",
              bd=0, command=root.destroy).pack(side="left", padx=5)

    return title_bar

def main():
    print("NeuroCode starting...")

    root = tk.Tk()
    root.overrideredirect(True)
    root.title("NeuroCode")
    root.geometry("1200x750")
    root.configure(bg=COLORS["bg_primary"])
    root.minsize(800, 600)

    print("GUI window created, click on taskbar icon to access")

    # Create titlebar at top
    title_bar = create_custom_titlebar(root)

    # Create container for main content (below titlebar)
    container = tk.Frame(root, bg=COLORS["bg_primary"])
    container.pack(fill=tk.BOTH, expand=True)

    app = NeuroCodeGUI(container)

    # Set app icon for taskbar AFTER window is fully created
    def set_taskbar_icon():
        try:
            import ctypes
            from PIL import Image
            import sys
            import pathlib

            # Get the package directory
            package_path = pathlib.Path(sys.modules['neurocode'].__file__).parent
            icon_path = package_path / "images" / "icon.png"
            ico_path = package_path / "images" / "icon.ico"

            if icon_path.exists():
                # Convert PNG to ICO with proper sizes
                img = Image.open(icon_path)
                img.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])

                ICO_PATH = str(ico_path.resolve())
                hwnd = int(root.winfo_id())
                user32 = ctypes.windll.user32

                IMAGE_ICON = 1
                LR_LOADFROMFILE = 0x00000010
                GCL_HICON = -14
                WM_SETICON = 0x80
                ICON_BIG = 1
                ICON_SM = 0

                icon_handle = user32.LoadImageW(None, ICO_PATH, IMAGE_ICON, 32, 32, LR_LOADFROMFILE)
                if icon_handle:
                    user32.SetClassLongPtrW(hwnd, GCL_HICON, icon_handle)
                    user32.SendMessageW(hwnd, WM_SETICON, ICON_SM, icon_handle)
                    user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, icon_handle)
        except Exception as e:
            print(f"Icon error: {e}")

    root.after(500, set_taskbar_icon)
    root.mainloop()


if __name__ == "__main__":
    main()
