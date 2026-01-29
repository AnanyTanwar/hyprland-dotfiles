#!/bin/bash

# ============================================================================
# Hyprland Dotfiles Installation Script
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

print_header() {
    echo -e "\n${CYAN}================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}→${NC} $1"
}

check_command() {
    command -v "$1" &> /dev/null
}

# ============================================================================
# SYSTEM CHECKS
# ============================================================================

print_header "Hyprland Dotfiles Installation"

# Check if running on Arch Linux
if [ ! -f /etc/arch-release ]; then
    print_error "This script is designed for Arch Linux!"
    exit 1
fi
print_success "Running on Arch Linux"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root!"
    exit 1
fi
print_success "Not running as root"

# Check internet connection
if ! ping -c 1 8.8.8.8 &> /dev/null; then
    print_error "No internet connection detected!"
    exit 1
fi
print_success "Internet connection available"

# ============================================================================
# SYSTEM UPDATE
# ============================================================================

print_header "System Update"
echo -e "${YELLOW}Do you want to update the system first? (recommended)${NC}"
read -p "Update system? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Updating system..."
    sudo pacman -Syu --noconfirm || {
        print_error "System update failed!"
        exit 1
    }
    print_success "System updated successfully!"
else
    print_warning "Skipping system update..."
fi

# ============================================================================
# AUR HELPERS
# ============================================================================

print_header "AUR Helpers Installation"

# Install yay if not present
if ! check_command yay; then
    print_info "Installing yay..."
    sudo pacman -S --needed --noconfirm git base-devel
    
    cd /tmp
    rm -rf yay  # Clean up any existing directory
    git clone https://aur.archlinux.org/yay.git
    cd yay
    makepkg -si --noconfirm
    cd ~
    
    if check_command yay; then
        print_success "yay installed successfully!"
    else
        print_error "yay installation failed!"
        exit 1
    fi
else
    print_success "yay is already installed"
fi

# Install paru if not present
if ! check_command paru; then
    print_info "Installing paru..."
    cd /tmp
    rm -rf paru  # Clean up any existing directory
    git clone https://aur.archlinux.org/paru.git
    cd paru
    makepkg -si --noconfirm
    cd ~
    
    if check_command paru; then
        print_success "paru installed successfully!"
    else
        print_warning "paru installation failed (optional)"
    fi
else
    print_success "paru is already installed"
fi

# ============================================================================
# REQUIRED PACKAGES
# ============================================================================

print_header "Installing Required Packages"

packages=(
    # Core Hyprland
    "hyprland"
    "hyprpaper"
    "xdg-desktop-portal-hyprland"
    
    # Status bar & launcher
    "waybar"
    "rofi-wayland"
    
    # Terminals
    "kitty"
    "alacritty"
    
    # Notifications
    "swaync"
    
    # System monitoring
    "btop"
    "cava"
    
    # Development
    "neovim"
    "git"
    
    # Shell & prompt
    "zsh"
    "starship"
    
    # Python for theme generator
    "python"
    "python-pip"
    
    # Screenshot utilities
    "grim"
    "slurp"
    "swappy"
    
    # Clipboard
    "wl-clipboard"
    "cliphist"
    
    # Authentication
    "polkit-kde-agent"
    
    # Qt Wayland support
    "qt5-wayland"
    "qt6-wayland"
    
    # File manager
    "thunar"
    "thunar-archive-plugin"
    "file-roller"
    
    # Network
    "network-manager-applet"
    
    # Audio
    "pavucontrol"
    "pipewire"
    "pipewire-pulse"
    "wireplumber"
)

failed_packages=()

for package in "${packages[@]}"; do
    if ! pacman -Q "$package" &> /dev/null; then
        print_info "Installing $package..."
        if sudo pacman -S --noconfirm "$package"; then
            print_success "$package installed"
        else
            print_error "Failed to install $package"
            failed_packages+=("$package")
        fi
    else
        print_success "$package already installed"
    fi
done

# ============================================================================
# AUR PACKAGES
# ============================================================================

print_header "Installing AUR Packages"

aur_packages=(
    "hyprpicker"
    "wlogout"
    "swww"  # Animated wallpaper daemon
)

for package in "${aur_packages[@]}"; do
    if ! pacman -Q "$package" &> /dev/null; then
        print_info "Installing $package from AUR..."
        if yay -S --noconfirm "$package"; then
            print_success "$package installed"
        else
            print_warning "Failed to install $package (optional)"
        fi
    else
        print_success "$package already installed"
    fi
done

# ============================================================================
# NERD FONTS
# ============================================================================

print_header "Installing Nerd Fonts"

nerd_fonts=(
    "ttf-jetbrains-mono-nerd"
    "ttf-firacode-nerd"
    "ttf-meslo-nerd"
)

for font in "${nerd_fonts[@]}"; do
    if ! pacman -Q "$font" &> /dev/null; then
        print_info "Installing $font..."
        if yay -S --noconfirm "$font"; then
            print_success "$font installed"
        else
            print_warning "Failed to install $font"
        fi
    else
        print_success "$font already installed"
    fi
done

# ============================================================================
# BACKUP EXISTING CONFIGS
# ============================================================================

print_header "Backing Up Existing Configurations"

backup_dir="$HOME/.config-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

configs=(
    "hypr"
    "waybar" 
    "rofi"
    "kitty"
    "alacritty"
    "swaync"
    "btop"
    "cava"
    "nvim"
    "starship"
    "theme-switcher"
)

backed_up=false
for config in "${configs[@]}"; do
    if [ -d "$HOME/.config/$config" ] || [ -f "$HOME/.config/$config" ]; then
        print_info "Backing up $config..."
        mv "$HOME/.config/$config" "$backup_dir/"
        backed_up=true
    fi
done

if [ -f "$HOME/.zshrc" ]; then
    print_info "Backing up .zshrc..."
    cp "$HOME/.zshrc" "$backup_dir/.zshrc"
    backed_up=true
fi

if [ "$backed_up" = true ]; then
    print_success "Configs backed up to: $backup_dir"
else
    print_info "No existing configs to backup"
    rmdir "$backup_dir" 2>/dev/null || true
fi

# ============================================================================
# CREATE SYMLINKS
# ============================================================================

print_header "Creating Symlinks"

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for config in "${configs[@]}"; do
    if [ -d "$DOTFILES_DIR/config/$config" ]; then
        print_info "Linking $config..."
        ln -sf "$DOTFILES_DIR/config/$config" "$HOME/.config/$config"
        print_success "$config linked"
    fi
done

# Link zshrc
if [ -f "$DOTFILES_DIR/.zshrc" ]; then
    print_info "Linking .zshrc..."
    ln -sf "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc"
    print_success ".zshrc linked"
fi

# ============================================================================
# CREATE DIRECTORIES
# ============================================================================

print_header "Creating Directories"

directories=(
    "$HOME/Pictures/Wallpapers"
    "$HOME/Pictures/Screenshots"
    "$HOME/.local/bin"
)

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        print_success "Created: $dir"
    else
        print_info "Already exists: $dir"
    fi
done

# ============================================================================
# GENERATE INITIAL THEMES
# ============================================================================

print_header "Generating Themes"

if [ -f "$HOME/.config/theme-switcher/scripts/generate-themes.py" ]; then
    print_info "Generating theme files..."
    cd "$HOME/.config/theme-switcher/scripts"
    if python generate-themes.py; then
        print_success "Themes generated successfully!"
    else
        print_warning "Theme generation failed (can be done manually later)"
    fi
else
    print_warning "Theme generator not found"
fi

# ============================================================================
# SET DEFAULT SHELL
# ============================================================================

print_header "Shell Configuration"

if [ "$SHELL" != "/bin/zsh" ] && [ "$SHELL" != "/usr/bin/zsh" ]; then
    echo -e "${YELLOW}Do you want to set Zsh as your default shell?${NC}"
    read -p "Set Zsh as default? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if check_command zsh; then
            chsh -s "$(which zsh)"
            print_success "Zsh set as default shell"
        else
            print_error "Zsh not found!"
        fi
    else
        print_info "Keeping current shell: $SHELL"
    fi
else
    print_success "Zsh is already your default shell"
fi

# ============================================================================
# INSTALLATION SUMMARY
# ============================================================================

print_header "Installation Complete!"

if [ ${#failed_packages[@]} -gt 0 ]; then
    print_warning "Some packages failed to install:"
    for pkg in "${failed_packages[@]}"; do
        echo "  - $pkg"
    done
    echo
fi

if [ "$backed_up" = true ]; then
    print_info "Backup location: $backup_dir"
fi

print_info "Wallpapers directory: ~/Pictures/Wallpapers"
print_info "Screenshots directory: ~/Pictures/Screenshots"

echo -e "\n${CYAN}Next Steps:${NC}"
echo -e "1. ${BLUE}Log out and log back in${NC} (or reboot)"
echo -e "2. ${BLUE}Switch themes:${NC} ${GREEN}~/.config/theme-switcher/scripts/switcher.sh${NC}"
echo -e "3. ${BLUE}Keybinding:${NC} ${GREEN}SUPER + T${NC}"

echo -e "\n${YELLOW}Useful Commands:${NC}"
echo -e "  ${GREEN}switcher.sh list${NC}        - List available themes"
echo -e "  ${GREEN}switcher.sh apply <theme>${NC} - Apply specific theme"
echo -e "  ${GREEN}switcher.sh current${NC}     - Show current theme"

echo -e "\n${GREEN}Enjoy your new Hyprland setup! 🚀${NC}\n"