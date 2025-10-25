#!/bin/bash
set -e

echo "Installing seek..."

# Check for system dependencies
MISSING_DEPS=()

if ! command -v zenity &> /dev/null; then
    MISSING_DEPS+=("zenity")
fi

if ! command -v nvim &> /dev/null; then
    MISSING_DEPS+=("neovim")
fi

# Install missing dependencies
if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "⚠️  Missing dependencies: ${MISSING_DEPS[*]}"
    echo "Installing..."
    
    # Detect package manager and install
    if command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm ${MISSING_DEPS[@]}
    elif command -v apt &> /dev/null; then
        sudo apt install -y ${MISSING_DEPS[@]}
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y ${MISSING_DEPS[@]}
    else
        echo "❌ Could not detect package manager."
        echo "Please install manually: ${MISSING_DEPS[*]}"
        exit 1
    fi
fi

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Install the tool
uv tool install .

# Setup config directory and .env
CONFIG_DIR="$HOME/.config/seek"
mkdir -p "$CONFIG_DIR"
mkdir -p "$CONFIG_DIR/responses"

if [ ! -f "$CONFIG_DIR/.env" ]; then
    cp .env.example "$CONFIG_DIR/.env"
    echo ""
    echo "Please edit $CONFIG_DIR/.env and add your DEEPSEEK_API_KEY"
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "Add to ~/.config/hypr/hyprland.conf:"
echo "  bind = SUPER, S, exec, seek"
