# 🌸 Hyprland Dotfiles

<p align="center">
  <img src="https://img.shields.io/badge/OS-Arch_Linux-1793D1?logo=arch-linux&logoColor=white&style=flat-square"/>
  <img src="https://img.shields.io/badge/WM-Hyprland-5e81ac?logo=wayland&logoColor=white&style=flat-square"/>
  <img src="https://img.shields.io/github/license/AnanyTanwar/hyprland-dotfiles?color=brightgreen&style=flat-square"/>
  <img src="https://img.shields.io/github/stars/AnanyTanwar/hyprland-dotfiles?style=flat-square"/>
</p>

A beautiful and feature-rich Hyprland rice for Arch Linux with custom theme switching capabilities.

![Main Screenshot](screenshots/tokyo-night/tokyonight_main.png)

## ✨ Features

- 🎨 **Custom Theme Switcher** - Switch between 7 beautiful themes instantly
  - Dracula
  - Tokyo Night
  - Catppuccin Mocha
  - Catppuccin Latte
  - Rose Pine
  - Gruvbox
  - Nord
- 🚀 **Modular Hyprland Configuration** - Clean, organized config structure
- 📊 **Themed Applications** - Consistent theming across all apps
- 🎯 **Productive Workflow** - Optimized keybinds and workspace management
- 💻 **Developer-Friendly** - Neovim with LSP, Treesitter, and more

## 📦 What's Included

### Window Manager & Desktop
- **Hyprland** - Dynamic tiling Wayland compositor
- **Waybar** - Customizable status bar with custom scripts
- **Rofi** - Application launcher (Type-2 Style-2)
- **Swaync** - Notification daemon

### Terminals & Shells
- **Kitty** - GPU-accelerated terminal
- **Alacritty** - Lightweight terminal
- **Zsh** - Shell with Powerlevel10k

### Development
- **Neovim** - Configured with:
  - LSP support
  - Treesitter syntax highlighting
  - Telescope fuzzy finder
  - Neo-tree file explorer
  - Auto-completion
  - And more plugins!

### System Monitoring & Utilities
- **Btop** - Resource monitor
- **Cava** - Audio visualizer
- **Starship** - Cross-shell prompt (alternative to p10k)

### Theme Management
- **Custom Theme Switcher** - Python-based theme generator
  - Automatically generates themes for all apps from JSON palettes
  - Instant theme switching via Rofi menu
  - Support for 7 color schemes

## 🖼️ Screenshots

### Tokyo Night
![Tokyo Night Main](screenshots/tokyo-night/tokyonight_main.png)
![Tokyo Night Dev](screenshots/tokyo-night/tokyo_dev.png)

### Gruvbox
![Gruvbox Main](screenshots/gruvbox/gruvbox_main.png)
![Gruvbox Dev](screenshots/gruvbox/gruv_dev.png)

### Dracula
![Dracula Main](screenshots/dracula/dracula_main.png)
![Dracula Dev](screenshots/dracula/dracula_dev.png)


## 📋 Requirements

- Arch Linux (or Arch-based distro)
- Git
- An AUR helper will be installed automatically (yay/paru)

## 🚀 Installation

### Automatic Installation (Recommended)

1. **Clone the repository**
```bash
   git clone https://github.com/AnanyTanwar/hyprland-dotfiles.git
   cd hyprland-dotfiles
```

2. **Run the install script**
```bash
   chmod +x install.sh
   ./install.sh
```

   The script will:
   - Update your system (with confirmation)
   - Install yay and paru if not present
   - Install all required packages
   - Install Nerd Fonts (JetBrains Mono, FiraCode, Meslo)
   - Backup your existing configs to `~/.config-backup-<timestamp>`
   - Create symlinks to the dotfiles

3. **Log out and log back in** to apply changes

### Manual Installation

If you prefer to install manually:

1. **Install dependencies**
```bash
   # Core packages
   sudo pacman -S hyprland waybar rofi kitty alacritty swaync btop cava neovim starship python python-pip grim slurp wl-clipboard polkit-kde-agent qt5-wayland qt6-wayland

   # AUR packages (using yay)
   yay -S hyprpicker wlogout ttf-jetbrains-mono-nerd ttf-firacode-nerd
```

2. **Backup your configs**
```bash
   mkdir -p ~/.config-backup
   cp -r ~/.config/hypr ~/.config-backup/
   cp -r ~/.config/waybar ~/.config-backup/
   # ... backup other configs
```

3. **Clone and symlink**
```bash
   git clone https://github.com/AnanyTanwar/hyprland-dotfiles.git ~/hyprland-dotfiles
   
   # Create symlinks
   ln -sf ~/hyprland-dotfiles/config/hypr ~/.config/hypr
   ln -sf ~/hyprland-dotfiles/config/waybar ~/.config/waybar
   ln -sf ~/hyprland-dotfiles/config/rofi ~/.config/rofi
   ln -sf ~/hyprland-dotfiles/config/kitty ~/.config/kitty
   ln -sf ~/hyprland-dotfiles/config/alacritty ~/.config/alacritty
   ln -sf ~/hyprland-dotfiles/config/swaync ~/.config/swaync
   ln -sf ~/hyprland-dotfiles/config/btop ~/.config/btop
   ln -sf ~/hyprland-dotfiles/config/cava ~/.config/cava
   ln -sf ~/hyprland-dotfiles/config/nvim ~/.config/nvim
   ln -sf ~/hyprland-dotfiles/config/starship ~/.config/starship
   ln -sf ~/hyprland-dotfiles/config/theme-switcher ~/.config/theme-switcher
   ln -sf ~/hyprland-dotfiles/.zshrc ~/.zshrc
```

## 🎨 Theme Switching

To switch themes, run:
```bash
~/.config/theme-switcher/scripts/switcher.sh
```

Or bind it to a keybind in your Hyprland config (already configured as `SUPER + T`).

The theme switcher will automatically update:
- Waybar
- Rofi
- Kitty
- Alacritty
- Swaync
- Btop
- Cava

> **Note:** Starship theme switching will be added in a future update. Currently using Catppuccin Mocha by default.

## ⌨️ Keybinds

### Essential Keybinds

| Keybind | Action |
|---------|--------|
| `SUPER + Q` | Close window |
| `SUPER + Return` | Open terminal |
| `SUPER + D` | Open Rofi launcher |
| `SUPER + T` | Theme switcher |
| `SUPER + E` | File manager |
| `SUPER + V` | Toggle floating |
| `SUPER + F` | Toggle fullscreen |
| `SUPER + [1-9]` | Switch to workspace |
| `SUPER + SHIFT + [1-9]` | Move window to workspace |
| `SUPER + Mouse` | Move/resize windows |

> See `config/hypr/config/keybinds.conf` for complete keybind list

## 📁 Directory Structure
```
hyprland-dotfiles/
├── config/
│   ├── hypr/              # Hyprland configuration
│   │   ├── hyprland.conf
│   │   ├── hyprlock.conf
│   │   ├── config/        # Modular configs
│   │   └── scripts/       # Utility scripts
│   ├── waybar/            # Status bar
│   ├── rofi/              # App launcher
│   ├── kitty/             # Terminal
│   ├── alacritty/         # Alternative terminal
│   ├── swaync/            # Notifications
│   ├── nvim/              # Neovim config
│   ├── btop/              # System monitor
│   ├── cava/              # Audio visualizer
│   ├── starship/          # Shell prompt
│   └── theme-switcher/    # Custom theme switcher
│       ├── palettes/      # Color palettes (JSON)
│       ├── themes/        # Generated theme files
│       └── scripts/       # Switcher scripts
├── .zshrc                 # Zsh configuration (with p10k)
├── install.sh             # Installation script
└── README.md
```

## 🔧 Customization

### Adding Your Own Theme

1. Create a new color palette JSON in `config/theme-switcher/palettes/`:
```json
   {
     "name": "my-theme",
     "base": "#1e1e2e",
     "text": "#cdd6f4",
     "red": "#f38ba8",
     ...
   }
```

2. Run the theme generator:
```bash
   cd ~/.config/theme-switcher/scripts
   python generate-themes.py
```

3. Your new theme will appear in the theme switcher!

### Modifying Hyprland Config

The Hyprland config is modular for easy customization:
- `config/animations.conf` - Animation settings
- `config/appearance.conf` - Borders, gaps, colors
- `config/keybinds.conf` - Keyboard shortcuts
- `config/monitors.conf` - Monitor configuration
- `config/programs.conf` - Default applications
- `config/windowrules.conf` - Window rules
- `config/workspaces.conf` - Workspace settings

## 🐛 Troubleshooting

### Theme switcher not working
```bash
# Make sure scripts are executable
chmod +x ~/.config/theme-switcher/scripts/*.sh
chmod +x ~/.config/hypr/scripts/*.sh
```

### Waybar not showing
```bash
# Restart waybar
pkill waybar
waybar &
```

### Missing icons in terminal
Make sure you have Nerd Fonts installed:
```bash
yay -S ttf-jetbrains-mono-nerd
```

## 🎯 Planned Features

- [ ] GTK theme integration
- [ ] Starship theme switching
- [ ] Wallpaper manager integration
- [ ] More color schemes
- [ ] Auto-wallpaper based on theme
- [ ] Firefox theme integration

## 🙏 Acknowledgments

- [Hyprland](https://hyprland.org/) - Amazing Wayland compositor
- [Catppuccin](https://github.com/catppuccin/catppuccin) - Beautiful pastel theme
- [Tokyo Night](https://github.com/tokyo-night/tokyo-night-vscode-theme) - Clean dark theme
- [Dracula](https://draculatheme.com/) - Dark theme
- [Rose Pine](https://rosepinetheme.com/) - Soho vibes theme
- [Gruvbox](https://github.com/morhetz/gruvbox) - Retro groove theme
- [Nord](https://www.nordtheme.com/) - Arctic-inspired theme
- The Hyprland and r/unixporn communities for inspiration

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Contributing

Feel free to open issues or submit pull requests if you have suggestions or improvements!

---

**Made with ❤️ by [Anany Tanwar](https://github.com/AnanyTanwar)**

*If you like this rice, give it a ⭐!*
