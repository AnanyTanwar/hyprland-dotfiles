#!/usr/bin/env bash

CONFIG_DIR="$HOME/.config"
THEME_SWITCHER_DIR="$CONFIG_DIR/theme-switcher"
THEMES_DIR="$THEME_SWITCHER_DIR/themes"
CURRENT_THEME_FILE="$CONFIG_DIR/.current_theme"
MENU_THEME="$THEME_SWITCHER_DIR/theme-switcher-menu.rasi"

get_current_theme() {
    [[ -f "$CURRENT_THEME_FILE" ]] && cat "$CURRENT_THEME_FILE" || echo "catppuccin-mocha"
}

format_theme_name() {
    local theme=$1
    case "$theme" in
        "catppuccin-mocha") echo "Catppuccin Mocha" ;;
        "catppuccin-latte") echo "Catppuccin Latte" ;;
        "rose-pine") echo "Rosé Pine" ;;
        "nord") echo "Nord" ;;
        "gruvbox") echo "Gruvbox" ;;
        "tokyo-night") echo "Tokyo Night" ;;
        "dracula") echo "Dracula" ;;
        *) echo "$theme" ;;
    esac
}

apply_theme() {
    local theme=$1
    local theme_path="$THEMES_DIR/$theme"
    
    if [[ ! -d "$theme_path" ]]; then
        notify-send "Theme Error" "Theme $theme not found!" -u critical
        return 1
    fi
    
    echo "Applying $theme..."
    
    [[ -f "$theme_path/rofi.rasi" ]] && cp "$theme_path/rofi.rasi" "$CONFIG_DIR/rofi/powermenu.rasi"
    if [[ -f "$theme_path/alacritty-theme.toml" ]]; then
    grep -v "^\[colors" "$CONFIG_DIR/alacritty/alacritty.toml" | grep -v "^background\|^foreground\|^text\|^cursor\|^black\|^red\|^green\|^yellow\|^blue\|^magenta\|^cyan\|^white" > /tmp/alacritty_base.toml
    cat /tmp/alacritty_base.toml "$theme_path/alacritty-theme.toml" > "$CONFIG_DIR/alacritty/alacritty.toml"
    fi
    [[ -f "$theme_path/kitty-theme.conf" ]] && cp "$theme_path/kitty-theme.conf" "$CONFIG_DIR/kitty/theme.conf"
    [[ -f "$theme_path/cava" ]] && cp "$theme_path/cava" "$CONFIG_DIR/cava/config"
    [[ -f "$theme_path/btop.theme" ]] && cp "$theme_path/btop.theme" "$CONFIG_DIR/btop/themes/current.theme"
    [[ -f "$theme_path/waybar.css" ]] && cp "$theme_path/waybar.css" "$CONFIG_DIR/waybar/style.css"
    [[ -f "$theme_path/swaync.css" ]] && cp "$theme_path/swaync.css" "$CONFIG_DIR/swaync/style.css"
    [[ -f "$theme_path/theme-switcher-menu.rasi" ]] && cp "$theme_path/theme-switcher-menu.rasi" "$THEME_SWITCHER_DIR/theme-switcher-menu.rasi"

    echo "$theme" > "$CURRENT_THEME_FILE"
    
    sed -i 's/color_theme = .*/color_theme = "current"/' "$CONFIG_DIR/btop/btop.conf"
    
    pkill waybar && waybar &
    pkill swaync && swaync &
    hyprctl reload &>/dev/null
    
    theme_display=$(format_theme_name "$theme")
    notify-send "Theme Applied" "$theme_display" -i preferences-desktop-theme
}

show_menu() {
    current=$(get_current_theme)
    
    themes=$(ls -1 "$THEMES_DIR" | sort)
    
    options=""
    while IFS= read -r theme; do
        theme_display=$(format_theme_name "$theme")
        if [[ "$theme" == "$current" ]]; then
            options+="$theme_display (active)\n"
        else
            options+="$theme_display\n"
        fi
    done <<< "$themes"
    
    chosen=$(echo -e "$options" | rofi -dmenu -i -p "󰏘 Themes" -theme "$MENU_THEME")
    
    if [[ -n "$chosen" ]]; then
        chosen=$(echo "$chosen" | sed 's/ (active)//')
        
   case "$chosen" in
    "Catppuccin Mocha") theme="catppuccin-mocha" ;;
    "Catppuccin Latte") theme="catppuccin-latte" ;;
    "Rosé Pine") theme="rose-pine" ;;
    "Nord") theme="nord" ;;
    "Gruvbox") theme="gruvbox" ;;
    "Tokyo Night") theme="tokyo-night" ;;
    "Dracula") theme="dracula" ;;
    *) theme=$(echo "$chosen" | tr '[:upper:]' '[:lower:]' | tr ' ' '-') ;;
esac
        
        apply_theme "$theme"
    fi
}

case "${1:-}" in
    apply)
        apply_theme "$2"
        ;;
    *)
        show_menu
        ;;
esac