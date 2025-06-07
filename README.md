# Seek - Linux CLI Tool for LLM Queries

`seek` is a command-line tool designed for Linux Mint with i3wm, bound to a keybind (`$mod+a`) to open a Zenity textbox for querying a language model (DeepSeek Chat). It provides quick answers to Python3 and Linux-related questions, displaying responses in a Neovim window. Answers are saved as markdown files in the `docs/` directory.

## Features
- Opens a textbox via `$mod+a` for entering queries.
- Uses the DeepSeek Chat model for concise, markdown-formatted answers.
- Saves responses in `<script_dir>/docs/` with a timestamp or title-based filename.
- Opens responses in Neovim via Alacritty for easy viewing.

## Setup
1. **Create `.env` file**:
   - In the script directory, create a `.env` file with your DeepSeek API key:
     ```
     DEEPSEEK_API_KEY=your_api_key_here
     ```

2. **Ensure dependencies**:
   - Neovim (`nvim`) must be installed.
   - Create the `docs/` directory in the script directory:
     ```
     mkdir -p <script_dir>/docs
     ```

3. **Set up virtual environment**:
   - Navigate to the script directory:
     ```
     cd <script_dir>
     ```
   - Create and activate a virtual environment:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Install requirements:
     ```
     pip install -r requirements.txt
     ```
   - Deactivate the virtual environment:
     ```
     deactivate
     ```

4. **Create the `seek` executable**:
   - Create a file at `~/.local/bin/seek` with the following content:
     ```bash
     #!/bin/bash
     cd <script_dir>
     source venv/bin/activate
     python3 ask.py
     deactivate
     ```
   - Make it executable:
     ```
     chmod +x ~/.local/bin/seek
     ```

5. **Add i3 keybind**:
   - Edit `~/.config/i3/config` and add:
     ```
     bindsym $mod+a exec --no-startup-id ~/.local/bin/seek
     ```

## Usage
- Press `$mod+a` to open a Zenity textbox.
- Enter a Python3 or Linux-related question.
- The response is generated, saved as a markdown file in `<script_dir>/docs/`, and opened in Neovim via Alacritty.
- Filenames are based on a two-word title (e.g., `Python_Error.md`) extracted from the response or a timestamp if no title is found.

## Planned Improvements
- Add handling for duplicate filenames by appending `_n`.
- Explore indexing the file system or referencing open files for context without manual input.

## Limitations
- No web search functionality.
- No support for follow-up questions (designed for one-off queries).
- Output format is fixed to markdown.

## Requirements
- Python 3
- Neovim
- Zenity
- Alacritty
- `langchain_openai` and `python-dotenv` (installed via `requirements.txt`)
- DeepSeek API key