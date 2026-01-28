#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Hyprland Dotfiles Installation${NC}"
echo -e "${GREEN}================================${NC}"

# Check if running on Arch Linux
if [ ! -f /etc/arch-release ]; then
    echo -e "${RED}This script is designed for Arch Linux!${NC}"
    exit 1
fi

# Ask for confirmation to update system
echo -e "\n${YELLOW}Do you want to update the system first? (recommended)${NC}"
read -p "Update system? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Updating system...${NC}"
    sudo pacman -Syu --noconfirm
    echo -e "${GREEN}System updated successfully!${NC}"
else
    echo -e "${YELLOW}Skipping system update...${NC}"
fi

# Install yay if not present
if ! command -v yay &> /dev/null; then
    echo -e "\n${YELLOW}yay not found. Installing yay...${NC}"
    sudo pacman -S --needed --noconfirm git base-devel
    cd /tmp
    git clone https://aur.archlinux.org/yay.git
    cd yay
    makepkg -si --noconfirm
    cd ~
    echo -e "${GREEN}yay installed successfully!${NC}"
else
    echo -e "${GREEN}yay is already installed${NC}"
fi

# Install paru if not present
if ! command -v paru &> /dev/null; then
    echo -e "\n${YELLOW}paru not found. Installing paru...${NC}"
    cd /tmp
    git clone https://aur.archlinux.org/paru.git
    cd paru
    makepkg -si --noconfirm
    cd ~
    echo -e "${GREEN}paru installed successfully!${NC}"
else
    echo -e "${GREEN}paru is already installed${NC}"
fi

# Install required packages from official repos
echo -e "\n${YELLOW}Installing required packages from official repos...${NC}"
packages=(
    "hyprland"
    "waybar"
    "rofi"
    "kitty"
    "alacritty"
    "swaync"
    "btop"
    "cava"
    "neovim"
    "starship"
    "python"
    "python-pip"
    "grim"
    "slurp"
    "wl-clipboard"
    "polkit-kde-agent"
    "qt5-wayland"
    "qt6-wayland"
)

for package in "${packages[@]}"; do
    if ! pacman -Q "$package" &> /dev/null; then
        echo -e "${YELLOW}Installing $package...${NC}"
        sudo pacman -S --noconfirm "$package"
    else
        echo -e "${GREEN}$package is already installed${NC}"
    fi
done

# Install AUR packages
echo -e "\n${YELLOW}Installing AUR packages...${NC}"
aur_packages=(
    "hyprpicker"
    "wlogout"
)

for package in "${aur_packages[@]}"; do
    if ! pacman -Q "$package" &> /dev/null; then
        echo -e "${YELLOW}Installing $package from AUR...${NC}"
        yay -S --noconfirm "$package"
    else
        echo -e "${GREEN}$package is already installed${NC}"
    fi
done

# Install Nerd Fonts
echo -e "\n${YELLOW}Installing Nerd Fonts...${NC}"
nerd_fonts=(
    "ttf-jetbrains-mono-nerd"
    "ttf-firacode-nerd"
    "ttf-meslo-nerd"
)

for font in "${nerd_fonts[@]}"; do
    if ! pacman -Q "$font" &> /dev/null; then
        echo -e "${YELLOW}Installing $font...${NC}"
        yay -S --noconfirm "$font"
    else
        echo -e "${GREEN}$font is already installed${NC}"
    fi
done

# Backup existing configs
echo -e "\n${YELLOW}Backing up existing configs...${NC}"
backup_dir="$HOME/.config-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

configs=("hypr" "waybar" "rofi" "kitty" "alacritty" "swaync" "btop" "cava" "nvim" "starship" "theme-switcher")

for config in "${configs[@]}"; do
    if [ -d "$HOME/.config/$config" ] || [ -f "$HOME/.config/$config" ]; then
        echo -e "${YELLOW}Backing up $config...${NC}"
        mv "$HOME/.config/$config" "$backup_dir/"
    fi
done

if [ -f "$HOME/.zshrc" ]; then
    echo -e "${YELLOW}Backing up .zshrc...${NC}"
    cp "$HOME/.zshrc" "$backup_dir/.zshrc"
fi

# Create symlinks
echo -e "\n${YELLOW}Creating symlinks...${NC}"
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for config in "${configs[@]}"; do
    if [ -d "$DOTFILES_DIR/config/$config" ]; then
        echo -e "${GREEN}Linking $config...${NC}"
        ln -sf "$DOTFILES_DIR/config/$config" "$HOME/.config/$config"
    fi
done

# Link zshrc
if [ -f "$DOTFILES_DIR/.zshrc" ]; then
    echo -e "${GREEN}Linking .zshrc...${NC}"
    ln -sf "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc"
fi

# Create wallpapers directory
echo -e "\n${YELLOW}Creating wallpapers directory...${NC}"
mkdir -p "$HOME/Pictures/Wallpapers"

echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo -e "\n${YELLOW}Your old configs have been backed up to: $backup_dir${NC}"
echo -e "${YELLOW}Add your wallpapers to: ~/Pictures/Wallpapers${NC}"
echo -e "${YELLOW}Please log out and log back in to see changes.${NC}"
echo -e "\n${BLUE}To switch themes, run:${NC}"
echo -e "${GREEN}~/.config/theme-switcher/scripts/switcher.sh${NC}"
