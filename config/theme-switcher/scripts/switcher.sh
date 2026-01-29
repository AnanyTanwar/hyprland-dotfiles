#!/usr/bin/env bash

# Theme Switcher - Improved Version
# Switches themes across all configured applications

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}"
THEME_SWITCHER_DIR="$CONFIG_DIR/theme-switcher"
THEMES_DIR="$THEME_SWITCHER_DIR/themes"
PALETTES_DIR="$THEME_SWITCHER_DIR/palettes"
CURRENT_THEME_FILE="$THEME_SWITCHER_DIR/.current-theme"
BACKUP_DIR="$THEME_SWITCHER_DIR/backups"
MENU_THEME="$THEME_SWITCHER_DIR/theme-switcher-menu.rasi"
LOG_FILE="$THEME_SWITCHER_DIR/.theme-switcher.log"

# Theme display name mappings
declare -A THEME_DISPLAY_NAMES=(
    ["catppuccin-mocha"]="󰄛 Catppuccin Mocha"
    ["catppuccin-latte"]="󰄛 Catppuccin Latte"
    ["rose-pine"]=" Rosé Pine"
    ["nord"]="󰔒 Nord"
    ["gruvbox"]=" Gruvbox"
    ["tokyo-night"]="󰓎 Tokyo Night"
    ["dracula"]=" Dracula"
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

error() {
    echo "ERROR: $*" >&2
    log "ERROR: $*"
    notify-send "Theme Switcher Error" "$*" -u critical -i dialog-error
}

success() {
    log "SUCCESS: $*"
}

# Check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Ensure required directories exist
ensure_directories() {
    mkdir -p "$THEMES_DIR" "$BACKUP_DIR" "$PALETTES_DIR"
}

# Get current theme (with fallback)
get_current_theme() {
    if [[ -f "$CURRENT_THEME_FILE" ]]; then
        cat "$CURRENT_THEME_FILE"
    else
        echo "catppuccin-mocha"
    fi
}

# Format theme name for display
format_theme_name() {
    local theme=$1
    echo "${THEME_DISPLAY_NAMES[$theme]:-$theme}"
}

# Reverse lookup: display name to theme slug
get_theme_slug() {
    local display_name=$1
    
    for slug in "${!THEME_DISPLAY_NAMES[@]}"; do
        if [[ "${THEME_DISPLAY_NAMES[$slug]}" == "$display_name" ]]; then
            echo "$slug"
            return 0
        fi
    done
    
    # Fallback: convert display name to slug
    echo "$display_name" | sed 's/^[^ ]* //' | tr '[:upper:]' '[:lower:]' | tr ' ' '-'
}

# Get list of available themes by scanning themes directory
get_available_themes() {
    if [[ ! -d "$THEMES_DIR" ]]; then
        error "Themes directory not found: $THEMES_DIR"
        return 1
    fi
    
    find "$THEMES_DIR" -mindepth 1 -maxdepth 1 -type d -printf "%f\n" | sort
}

# Validate theme exists
validate_theme() {
    local theme=$1
    local theme_path="$THEMES_DIR/$theme"
    
    if [[ ! -d "$theme_path" ]]; then
        error "Theme '$theme' not found at: $theme_path"
        return 1
    fi
    
    # Check for required files
    local required_files=(
        "waybar.css"
        "rofi.rasi"
        "kitty-theme.conf"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$theme_path/$file" ]]; then
            error "Missing required file: $file in theme '$theme'"
            return 1
        fi
    done
    
    return 0
}

# Create backup of current configs
backup_configs() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_path="$BACKUP_DIR/backup_$timestamp"
    
    log "Creating backup at: $backup_path"
    mkdir -p "$backup_path"
    
    # Backup important config files
    [[ -f "$CONFIG_DIR/waybar/style.css" ]] && cp "$CONFIG_DIR/waybar/style.css" "$backup_path/"
    [[ -f "$CONFIG_DIR/kitty/theme.conf" ]] && cp "$CONFIG_DIR/kitty/theme.conf" "$backup_path/"
    [[ -f "$CONFIG_DIR/alacritty/alacritty.toml" ]] && cp "$CONFIG_DIR/alacritty/alacritty.toml" "$backup_path/"
    [[ -f "$CONFIG_DIR/rofi/powermenu.rasi" ]] && cp "$CONFIG_DIR/rofi/powermenu.rasi" "$backup_path/"
    
    # Keep only last 5 backups
    ls -dt "$BACKUP_DIR"/backup_* | tail -n +6 | xargs -r rm -rf
    
    success "Backup created: $backup_path"
}

# ============================================================================
# THEME APPLICATION
# ============================================================================

apply_waybar() {
    local theme_path=$1
    [[ -f "$theme_path/waybar.css" ]] || return 1
    
    cp "$theme_path/waybar.css" "$CONFIG_DIR/waybar/style.css"
    
    # Reload waybar
    if command_exists waybar; then
        pkill waybar 2>/dev/null || true
        waybar &>/dev/null &
        disown
    fi
}

apply_swaync() {
    local theme_path=$1
    [[ -f "$theme_path/swaync.css" ]] || return 1
    
    cp "$theme_path/swaync.css" "$CONFIG_DIR/swaync/style.css"
    
    # Reload swaync
    if command_exists swaync; then
        pkill swaync 2>/dev/null || true
        swaync &>/dev/null &
        disown
    fi
}

apply_rofi() {
    local theme_path=$1
    [[ -f "$theme_path/rofi.rasi" ]] || return 1
    
    mkdir -p "$CONFIG_DIR/rofi"
    cp "$theme_path/rofi.rasi" "$CONFIG_DIR/rofi/powermenu.rasi"
    
    # Also update theme switcher menu
    [[ -f "$theme_path/theme-switcher-menu.rasi" ]] && \
        cp "$theme_path/theme-switcher-menu.rasi" "$THEME_SWITCHER_DIR/theme-switcher-menu.rasi"
}

apply_alacritty() {
    local theme_path=$1
    [[ -f "$theme_path/alacritty-theme.toml" ]] || return 1
    
    local config_file="$CONFIG_DIR/alacritty/alacritty.toml"
    
    if [[ -f "$config_file" ]]; then
        # Remove existing color configuration
        grep -v "^\[colors" "$config_file" | \
        grep -v "^background\|^foreground\|^text\|^cursor\|^black\|^red\|^green\|^yellow\|^blue\|^magenta\|^cyan\|^white" \
        > /tmp/alacritty_base.toml
        
        # Combine base config with new theme
        cat /tmp/alacritty_base.toml "$theme_path/alacritty-theme.toml" > "$config_file"
        rm /tmp/alacritty_base.toml
    else
        # Just copy theme if config doesn't exist
        mkdir -p "$CONFIG_DIR/alacritty"
        cp "$theme_path/alacritty-theme.toml" "$config_file"
    fi
}

apply_kitty() {
    local theme_path=$1
    [[ -f "$theme_path/kitty-theme.conf" ]] || return 1
    
    mkdir -p "$CONFIG_DIR/kitty"
    cp "$theme_path/kitty-theme.conf" "$CONFIG_DIR/kitty/theme.conf"
    
    # Reload kitty instances
    if command_exists kitty; then
        killall -SIGUSR1 kitty 2>/dev/null || true
    fi
}

apply_btop() {
    local theme_path=$1
    [[ -f "$theme_path/btop.theme" ]] || return 1
    
    mkdir -p "$CONFIG_DIR/btop/themes"
    cp "$theme_path/btop.theme" "$CONFIG_DIR/btop/themes/current.theme"
    
    # Update btop config to use current theme
    if [[ -f "$CONFIG_DIR/btop/btop.conf" ]]; then
        sed -i 's/color_theme = .*/color_theme = "current"/' "$CONFIG_DIR/btop/btop.conf"
    fi
}

apply_cava() {
    local theme_path=$1
    [[ -f "$theme_path/cava" ]] || return 1
    
    mkdir -p "$CONFIG_DIR/cava"
    cp "$theme_path/cava" "$CONFIG_DIR/cava/config"
}

apply_hyprland() {
    if command_exists hyprctl; then
        hyprctl reload &>/dev/null || true
    fi
}

# Main theme application function
apply_theme() {
    local theme=$1
    local theme_path="$THEMES_DIR/$theme"
    
    log "Applying theme: $theme"
    
    # Validate theme
    if ! validate_theme "$theme"; then
        error "Theme validation failed: $theme"
        return 1
    fi
    
    # Create backup before applying
    backup_configs
    
    # Apply to each application
    local failed=0
    
    apply_waybar "$theme_path" || { error "Failed to apply waybar theme"; ((failed++)); }
    apply_swaync "$theme_path" || { error "Failed to apply swaync theme"; ((failed++)); }
    apply_rofi "$theme_path" || { error "Failed to apply rofi theme"; ((failed++)); }
    apply_alacritty "$theme_path" || { error "Failed to apply alacritty theme"; ((failed++)); }
    apply_kitty "$theme_path" || { error "Failed to apply kitty theme"; ((failed++)); }
    apply_btop "$theme_path" || { error "Failed to apply btop theme"; ((failed++)); }
    apply_cava "$theme_path" || { error "Failed to apply cava theme"; ((failed++)); }
    
    # Reload window manager
    apply_hyprland
    
    # Save current theme
    echo "$theme" > "$CURRENT_THEME_FILE"
    
    # Show notification
    local theme_display=$(format_theme_name "$theme")
    if [[ $failed -eq 0 ]]; then
        notify-send "Theme Applied" "$theme_display is now active" -i preferences-desktop-theme
        success "Successfully applied theme: $theme"
    else
        notify-send "Theme Partially Applied" "$theme_display applied with $failed errors" -u normal -i dialog-warning
        error "Theme applied with $failed errors: $theme"
    fi
}

# ============================================================================
# THEME MENU
# ============================================================================

show_menu() {
    local current=$(get_current_theme)
    
    # Get available themes
    local themes
    if ! themes=$(get_available_themes); then
        exit 1
    fi
    
    # Build menu options
    local options=""
    while IFS= read -r theme; do
        local theme_display=$(format_theme_name "$theme")
        if [[ "$theme" == "$current" ]]; then
            options+="$theme_display ✓\n"
        else
            options+="$theme_display\n"
        fi
    done <<< "$themes"
    
    # Show rofi menu
    local chosen
    chosen=$(echo -e "$options" | rofi -dmenu -i -p "󰏘 Themes" -theme "$MENU_THEME")
    
    if [[ -n "$chosen" ]]; then
        # Remove the checkmark if present
        chosen=$(echo "$chosen" | sed 's/ ✓$//')
        
        # Convert display name to theme slug
        local theme=$(get_theme_slug "$chosen")
        
        apply_theme "$theme"
    fi
}

# ============================================================================
# ADDITIONAL FEATURES
# ============================================================================

show_current() {
    local current=$(get_current_theme)
    local display=$(format_theme_name "$current")
    echo "Current theme: $display ($current)"
}

list_themes() {
    echo "Available themes:"
    echo "================="
    local current=$(get_current_theme)
    
    get_available_themes | while IFS= read -r theme; do
        local display=$(format_theme_name "$theme")
        if [[ "$theme" == "$current" ]]; then
            echo "  $display (active)"
        else
            echo "  $display"
        fi
    done
}

show_help() {
    cat << EOF
Theme Switcher - Hyprland Dotfiles

Usage: $(basename "$0") [COMMAND] [THEME]

Commands:
    (no args)       Show interactive theme menu
    apply THEME     Apply a specific theme
    current         Show currently active theme
    list            List all available themes
    help            Show this help message

Examples:
    $(basename "$0")                    # Show menu
    $(basename "$0") apply tokyo-night  # Apply Tokyo Night theme
    $(basename "$0") list               # List all themes
    $(basename "$0") current            # Show current theme

Available themes:
EOF
    get_available_themes | while read -r theme; do
        echo "  - $theme"
    done
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    # Ensure directories exist
    ensure_directories
    
    # Parse command
    case "${1:-}" in
        apply)
            if [[ -z "${2:-}" ]]; then
                error "No theme specified. Usage: $0 apply THEME"
                exit 1
            fi
            apply_theme "$2"
            ;;
        current)
            show_current
            ;;
        list)
            list_themes
            ;;
        help|-h|--help)
            show_help
            ;;
        *)
            show_menu
            ;;
    esac
}

main "$@"