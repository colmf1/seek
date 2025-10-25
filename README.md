# Seek - Linux CLI Tool for LLM Queries

AI assistant for Hyprland - ask questions via zenity dialog, get answers in neovim.

## Requirements

- Linux with:
  - zenity (GUI dialogs)
  - neovim (response display)
- DEEPSEEK_API_KEY

## Installation
```bash
git clone https://github.com/colmf1/seek.git
cd seek
chmod +x install.sh
./install.sh
```

Edit `~/.config/your-app/.env`:
```
DEEPSEEK_API_KEY=sk-...
```

## Hyprland Setup

Add to `~/.config/hypr/hyprland.conf`:
```
bind = SUPER, S, exec, seek
```

Press `SUPER + S` to launch!

## Usage

1. Press your keybind (e.g., SUPER + S)
2. Type your question in the zenity dialog
3. Response opens in neovim
4. Close neovim when done (`:q`)
5. Response is saved in 

## Notes

- Files are saved in .config/responses with an llm description of the question
- Files saved as markdown
- TODO: Account for duplicate filenames 

## Uninstall
```bash
uv tool uninstall your-app
rm -rf ~/.config/your-app
```
