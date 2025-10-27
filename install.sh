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
    echo ""
    echo "=== API Provider Setup ==="
    echo "Select your AI provider:"
    echo "1) DeepSeek"
    echo "2) OpenAI"
    echo "3) Anthropic"
    
    while true; do
        read -p "Enter choice (1-3): " provider_choice
        
        case $provider_choice in
            1)
                PROVIDER="deepseek"
                API_KEY_NAME="DEEPSEEK_API_KEY"
                break
                ;;
            2)
                PROVIDER="openai"
                API_KEY_NAME="OPENAI_API_KEY"
                break
                ;;
            3)
                PROVIDER="anthropic"
                API_KEY_NAME="ANTHROPIC_API_KEY"
                break
                ;;
            *)
                echo "Invalid choice. Please enter 1-3."
                ;;
        esac
    done
    
    echo ""
    echo "=== API Key Setup ==="
    while true; do
        read -sp "Enter your $API_KEY_NAME: " api_key
        echo ""
        
        if [ -z "$api_key" ]; then
            read -p "Skip API key setup? (y/n): " skip
            if [[ $skip == "y" ]]; then
                echo "AI_PROVIDER=$PROVIDER" > "$CONFIG_DIR/.env"
                echo "AI_API_KEY" >> "$CONFIG_DIR/.env"
                echo "⚠️  Edit $CONFIG_DIR/.env later to add your key."
                break
            fi
        else
            echo "AI_PROVIDER=$PROVIDER" > "$CONFIG_DIR/.env"
            echo "$API_KEY_NAME=$api_key" >> "$CONFIG_DIR/.env"
            chmod 600 "$CONFIG_DIR/.env"  
            echo "✓ Provider and API key saved securely!"
            break
        fi
    done
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "Add to ~/.config/hypr/hyprland.conf:"
echo "  bind = SUPER, S, exec, seek"


