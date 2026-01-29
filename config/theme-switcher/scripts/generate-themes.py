#!/usr/bin/env python3

"""
Theme Generator for Hyprland Dotfiles
Generates theme files for multiple applications from JSON color palettes
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import argparse

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path.home() / ".config" / "theme-switcher"
PALETTES_DIR = BASE_DIR / "palettes"
THEMES_DIR = BASE_DIR / "themes"

# Required color keys that all palettes must have (for validation)
REQUIRED_COLORS = {
    'base', 'text', 'red', 'green', 'yellow', 'blue', 'pink'
}

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ThemeConfig:
    """Configuration for theme generation"""
    name: str
    palette_file: Path
    output_dir: Path
    colors: Dict[str, str]


# ============================================================================
# COLOR MAPPING FUNCTIONS
# ============================================================================

def get_mapped_colors(theme_name: str, colors: Dict[str, str]) -> Dict[str, str]:
    """
    Map theme-specific color names to a unified color scheme.
    This allows different themes to use their own naming conventions.
    """
    
    # Catppuccin themes (Mocha, Latte, etc.)
    if theme_name.startswith("catppuccin"):
        return {
            'base': colors.get('base', '#1e1e2e'),
            'mantle': colors.get('mantle', '#181825'),
            'crust': colors.get('crust', '#11111b'),
            'text': colors.get('text', '#cdd6f4'),
            'subtext0': colors.get('subtext0', '#a6adc8'),
            'subtext1': colors.get('subtext1', '#bac2de'),
            'surface0': colors.get('surface0', '#313244'),
            'surface1': colors.get('surface1', '#45475a'),
            'surface2': colors.get('surface2', '#585b70'),
            'overlay0': colors.get('overlay0', '#6c7086'),
            'overlay1': colors.get('overlay1', '#7f849c'),
            'blue': colors.get('blue', '#89b4fa'),
            'lavender': colors.get('lavender', '#b4befe'),
            'sapphire': colors.get('sapphire', '#74c7ec'),
            'sky': colors.get('sky', '#89dceb'),
            'teal': colors.get('teal', '#94e2d5'),
            'green': colors.get('green', '#a6e3a1'),
            'yellow': colors.get('yellow', '#f9e2af'),
            'peach': colors.get('peach', '#fab387'),
            'maroon': colors.get('maroon', '#eba0ac'),
            'red': colors.get('red', '#f38ba8'),
            'mauve': colors.get('mauve', '#cba6f7'),
            'pink': colors.get('pink', '#f5c2e7')
        }
    
    # Rose Pine theme
    elif theme_name == "rose-pine":
        return {
            'base': colors.get('base', '#191724'),
            'mantle': colors.get('surface', '#1f1d2e'),
            'crust': colors.get('base', '#191724'),
            'text': colors.get('text', '#e0def4'),
            'subtext0': colors.get('subtle', '#908caa'),
            'subtext1': colors.get('subtle', '#908caa'),
            'surface0': colors.get('surface', '#1f1d2e'),
            'surface1': colors.get('overlay', '#26233a'),
            'surface2': colors.get('highlight_med', '#403d52'),
            'overlay0': colors.get('muted', '#6e6a86'),
            'overlay1': colors.get('subtle', '#908caa'),
            'blue': colors.get('pine', '#31748f'),
            'lavender': colors.get('iris', '#c4a7e7'),
            'sapphire': colors.get('foam', '#9ccfd8'),
            'sky': colors.get('foam', '#9ccfd8'),
            'teal': colors.get('foam', '#9ccfd8'),
            'green': colors.get('foam', '#9ccfd8'),
            'yellow': colors.get('gold', '#f6c177'),
            'peach': colors.get('gold', '#f6c177'),
            'maroon': colors.get('love', '#eb6f92'),
            'red': colors.get('love', '#eb6f92'),
            'mauve': colors.get('iris', '#c4a7e7'),
            'pink': colors.get('rose', '#ebbcba')
        }
    
    # Nord theme
    elif theme_name == "nord":
        return {
            'base': colors.get('nord0', '#2e3440'),
            'mantle': colors.get('nord1', '#3b4252'),
            'crust': colors.get('nord0', '#2e3440'),
            'text': colors.get('nord4', '#d8dee9'),
            'subtext0': colors.get('nord4', '#d8dee9'),
            'subtext1': colors.get('nord5', '#e5e9f0'),
            'surface0': colors.get('nord1', '#3b4252'),
            'surface1': colors.get('nord2', '#434c5e'),
            'surface2': colors.get('nord3', '#4c566a'),
            'overlay0': colors.get('nord3', '#4c566a'),
            'overlay1': colors.get('nord4', '#d8dee9'),
            'blue': colors.get('nord10', '#5e81ac'),
            'lavender': colors.get('nord15', '#b48ead'),
            'sapphire': colors.get('nord8', '#88c0d0'),
            'sky': colors.get('nord8', '#88c0d0'),
            'teal': colors.get('nord7', '#8fbcbb'),
            'green': colors.get('nord14', '#a3be8c'),
            'yellow': colors.get('nord13', '#ebcb8b'),
            'peach': colors.get('nord12', '#d08770'),
            'maroon': colors.get('nord11', '#bf616a'),
            'red': colors.get('nord11', '#bf616a'),
            'mauve': colors.get('nord15', '#b48ead'),
            'pink': colors.get('nord15', '#b48ead')
        }
    
    # Gruvbox theme
    elif theme_name == "gruvbox":
        return {
            'base': colors.get('bg', '#282828'),
            'mantle': colors.get('bg0', '#282828'),
            'crust': colors.get('bg', '#282828'),
            'text': colors.get('fg', '#ebdbb2'),
            'subtext0': colors.get('fg2', '#d5c4a1'),
            'subtext1': colors.get('fg1', '#ebdbb2'),
            'surface0': colors.get('bg1', '#3c3836'),
            'surface1': colors.get('bg2', '#504945'),
            'surface2': colors.get('bg3', '#665c54'),
            'overlay0': colors.get('bg4', '#7c6f64'),
            'overlay1': colors.get('gray', '#928374'),
            'blue': colors.get('blue', '#83a598'),
            'lavender': colors.get('purple', '#d3869b'),
            'sapphire': colors.get('aqua', '#8ec07c'),
            'sky': colors.get('aqua', '#8ec07c'),
            'teal': colors.get('aqua', '#8ec07c'),
            'green': colors.get('green', '#b8bb26'),
            'yellow': colors.get('yellow', '#fabd2f'),
            'peach': colors.get('orange', '#fe8019'),
            'maroon': colors.get('red', '#fb4934'),
            'red': colors.get('red', '#fb4934'),
            'mauve': colors.get('purple', '#d3869b'),
            'pink': colors.get('purple', '#d3869b')
        }
    
    # Tokyo Night theme
    elif theme_name == "tokyo-night":
        return {
            'base': colors.get('bg', '#1a1b26'),
            'mantle': colors.get('bg_dark', '#16161e'),
            'crust': colors.get('bg_dark', '#16161e'),
            'text': colors.get('fg', '#c0caf5'),
            'subtext0': colors.get('fg_dark', '#a9b1d6'),
            'subtext1': colors.get('fg', '#c0caf5'),
            'surface0': colors.get('bg_highlight', '#292e42'),
            'surface1': colors.get('terminal_black', '#414868'),
            'surface2': colors.get('dark3', '#545c7e'),
            'overlay0': colors.get('comment', '#565f89'),
            'overlay1': colors.get('dark5', '#737aa2'),
            'blue': colors.get('blue', '#7aa2f7'),
            'lavender': colors.get('purple', '#bb9af7'),
            'sapphire': colors.get('cyan', '#7dcfff'),
            'sky': colors.get('cyan', '#7dcfff'),
            'teal': colors.get('teal', '#1abc9c'),
            'green': colors.get('green', '#9ece6a'),
            'yellow': colors.get('yellow', '#e0af68'),
            'peach': colors.get('orange', '#ff9e64'),
            'maroon': colors.get('red1', '#db4b4b'),
            'red': colors.get('red', '#f7768e'),
            'mauve': colors.get('purple', '#bb9af7'),
            'pink': colors.get('magenta', '#ff007c')
        }
    
    # Dracula theme
    elif theme_name == "dracula":
        return {
            'base': colors.get('bg', '#282a36'),
            'mantle': colors.get('bg', '#282a36'),
            'crust': colors.get('bg', '#282a36'),
            'text': colors.get('fg', '#f8f8f2'),
            'subtext0': colors.get('comment', '#6272a4'),
            'subtext1': colors.get('fg', '#f8f8f2'),
            'surface0': colors.get('current_line', '#44475a'),
            'surface1': colors.get('selection', '#44475a'),
            'surface2': colors.get('selection', '#44475a'),
            'overlay0': colors.get('comment', '#6272a4'),
            'overlay1': colors.get('comment', '#6272a4'),
            'blue': colors.get('cyan', '#8be9fd'),
            'lavender': colors.get('purple', '#bd93f9'),
            'sapphire': colors.get('cyan', '#8be9fd'),
            'sky': colors.get('cyan', '#8be9fd'),
            'teal': colors.get('cyan', '#8be9fd'),
            'green': colors.get('green', '#50fa7b'),
            'yellow': colors.get('yellow', '#f1fa8c'),
            'peach': colors.get('orange', '#ffb86c'),
            'maroon': colors.get('red', '#ff5555'),
            'red': colors.get('red', '#ff5555'),
            'mauve': colors.get('purple', '#bd93f9'),
            'pink': colors.get('pink', '#ff79c6')
        }
    
    # Default/unknown theme - try to use colors as-is
    else:
        print(f"⚠️  Warning: Unknown theme '{theme_name}', using direct color mapping")
        return colors


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_palette(palette: Dict[str, str], theme_name: str) -> bool:
    """Validate that a palette has all required colors"""
    missing_colors = REQUIRED_COLORS - set(palette.keys())
    
    if missing_colors:
        print(f"❌ Error: Palette '{theme_name}' is missing required colors: {missing_colors}")
        return False
    
    # Validate color format (should be hex colors)
    for color_name, color_value in palette.items():
        if not isinstance(color_value, str):
            print(f"❌ Error: Color '{color_name}' in '{theme_name}' is not a string")
            return False
        
        if not color_value.startswith('#'):
            print(f"⚠️  Warning: Color '{color_name}' in '{theme_name}' doesn't start with '#': {color_value}")
    
    return True


# ============================================================================
# PALETTE LOADING
# ============================================================================

def load_palette(theme_name: str) -> Optional[Dict[str, str]]:
    """Load a color palette from JSON file"""
    palette_file = PALETTES_DIR / f"{theme_name}.json"
    
    if not palette_file.exists():
        print(f"❌ Error: Palette file not found: {palette_file}")
        return None
    
    try:
        with open(palette_file, 'r') as f:
            colors = json.load(f)
        
        # Validate palette
        if not validate_palette(colors, theme_name):
            return None
        
        return colors
    
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {palette_file}: {e}")
        return None
    except Exception as e:
        print(f"❌ Error loading palette {theme_name}: {e}")
        return None


def discover_palettes() -> List[str]:
    """Auto-discover available palette files"""
    if not PALETTES_DIR.exists():
        print(f"❌ Error: Palettes directory not found: {PALETTES_DIR}")
        return []
    
    palettes = []
    for palette_file in PALETTES_DIR.glob("*.json"):
        theme_name = palette_file.stem
        palettes.append(theme_name)
    
    return sorted(palettes)


# ============================================================================
# THEME GENERATORS
# ============================================================================

def generate_waybar(theme_name: str, mapped: Dict[str, str]) -> str:
    """Generate Waybar CSS theme"""
    return f"""/* {theme_name.title()} */
@define-color base   {mapped['base']};
@define-color mantle {mapped['mantle']};
@define-color crust  {mapped['crust']};

@define-color text     {mapped['text']};
@define-color subtext0 {mapped['subtext0']};
@define-color subtext1 {mapped['subtext1']};

@define-color surface0 {mapped['surface0']};
@define-color surface1 {mapped['surface1']};
@define-color surface2 {mapped['surface2']};

@define-color overlay0 {mapped['overlay0']};
@define-color overlay1 {mapped['overlay1']};

@define-color blue     {mapped['blue']};
@define-color lavender {mapped['lavender']};
@define-color sapphire {mapped['sapphire']};
@define-color sky      {mapped['sky']};
@define-color teal     {mapped['teal']};
@define-color green    {mapped['green']};
@define-color yellow   {mapped['yellow']};
@define-color peach    {mapped['peach']};
@define-color maroon   {mapped['maroon']};
@define-color red      {mapped['red']};
@define-color mauve    {mapped['mauve']};
@define-color pink     {mapped['pink']};

* {{
  border: none;
  font-family: "Ubuntu Nerd Font Propo";
  font-size: 15px;
  font-weight: 600;
  min-height: 0;
  margin: 0;
  padding: 0;
}}

window#waybar {{
  background: transparent;
  color: @text;
}}

tooltip {{
  background: @base;
  border: 1px solid @surface1;
  border-radius: 8px;
  padding: 6px;
}}

tooltip label {{
  color: @text;
}}

#workspaces {{
  background: alpha(@base, 0.8);
  border-radius: 12px;
  padding: 3px 9px;
  margin: 4px 7px;
}}

#workspaces button {{
  padding: 3px 11px;
  margin: 0 2px;
  border: 1px solid @surface1;
  background: alpha(@surface0, 0.8);
  color: @text;
  border-radius: 8px;
  transition: all 200ms ease;
}}

#workspaces button.active {{
  border-radius: 100px;
  border: 1px solid @mauve;
  color: @crust;
  background: @mauve;
  min-width: 47px;
  font-size: 15px;
}}

#clock {{
  background: @blue;
  color: @crust;
  font-size: 17px;
  font-weight: 600;
  padding: 6px 18px;
  margin: 4px 8px;
  border-radius: 14px;
}}

#custom-arch {{
  font-size: 18px;
  padding: 6px 14px;
  margin-left: 12px;
  margin-right: 8px;
  min-height: 32px;
  color: @mauve;
  background: transparent;
  border-radius: 12px;
  transition: all 200ms ease;
}}

#custom-arch:hover {{
  background: alpha(@mauve, 0.2);
  color: @mauve;
}}

#cpu {{
  background: @green;
  color: @crust;
  padding: 3px 11px;
  margin: 4px 3px;
  border-radius: 8px;
}}

#memory {{
  background: @yellow;
  color: @crust;
  padding: 3px 11px;
  margin: 4px 3px;
  border-radius: 8px;
}}

#pulseaudio {{
  background: @mauve;
  color: @crust;
  padding: 3px 11px;
  margin: 4px 3px;
  border-radius: 8px;
}}

#pulseaudio.muted {{
  background: @surface1;
  color: @overlay1;
}}

#network {{
  background: @sky;
  color: @crust;
  padding: 3px 11px;
  margin: 4px 6px;
  border-radius: 8px;
}}

#network.disconnected {{
  background: @surface1;
  color: @red;
}}

#custom-notification {{
  background: @pink;
  color: @crust;
  margin-right: 6px;
  padding: 3px 11px;
  margin: 4px 12px 4px 3px;
  border-radius: 8px;
  font-size: 16px;
}}

#custom-notification.notification {{
  color: #f38ba8;
  text-shadow: 0 0 6px rgba(243, 139, 168, 0.6);
}}

#custom-notification.dnd-notification {{
  background: @maroon;
  color: @crust;
}}

#mode {{
  background: @red;
  color: @crust;
  padding: 4px 12px;
  margin: 4px 6px;
  border-radius: 8px;
  font-weight: 700;
}}
"""


def generate_swaync(theme_name: str, mapped: Dict[str, str]) -> str:
    """Generate SwayNC CSS theme"""
    return f"""/* {theme_name.title()} Colors */
@define-color base   {mapped['base']};
@define-color mantle {mapped['mantle']};
@define-color crust  {mapped['crust']};

@define-color text     {mapped['text']};
@define-color subtext0 {mapped['subtext0']};
@define-color subtext1 {mapped['subtext1']};

@define-color surface0 {mapped['surface0']};
@define-color surface1 {mapped['surface1']};
@define-color surface2 {mapped['surface2']};

@define-color overlay0 {mapped['overlay0']};
@define-color overlay1 {mapped['overlay1']};

@define-color blue     {mapped['blue']};
@define-color lavender {mapped['lavender']};
@define-color sapphire {mapped['sapphire']};
@define-color sky      {mapped['sky']};
@define-color teal     {mapped['teal']};
@define-color green    {mapped['green']};
@define-color yellow   {mapped['yellow']};
@define-color peach    {mapped['peach']};
@define-color maroon   {mapped['maroon']};
@define-color red      {mapped['red']};
@define-color mauve    {mapped['mauve']};
@define-color pink     {mapped['pink']};

* {{
  font-family: "Ubuntu Nerd Font Propo";
  font-weight: 600;
  font-size: 14px;
}}

.control-center {{
  background: alpha(@base, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 2px solid alpha(@mauve, 0.4);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
  margin: 10px;
  padding: 0;
}}

.control-center .notification-row:focus,
.control-center .notification-row:hover {{
  background: alpha(@surface1, 0.6);
  border-radius: 12px;
}}

.widget-title {{
  background: alpha(@mauve, 0.3);
  backdrop-filter: blur(10px);
  color: @text;
  font-size: 18px;
  font-weight: 700;
  border-radius: 12px;
  margin: 12px;
  padding: 12px;
  border: 1px solid alpha(@mauve, 0.5);
}}

.widget-title > button {{
  background: alpha(@pink, 0.8);
  color: @crust;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 700;
  border: none;
  box-shadow: 0 4px 12px alpha(@pink, 0.4);
  transition: all 200ms ease;
}}

.widget-title > button:hover {{
  background: @pink;
  box-shadow: 0 6px 16px alpha(@pink, 0.6);
  transform: translateY(-2px);
}}

.widget-dnd {{
  background: alpha(@surface0, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  margin: 12px;
  padding: 12px;
  border: 1px solid alpha(@surface2, 0.5);
}}

.widget-dnd > label {{
  color: @text;
  font-weight: 600;
}}

.widget-dnd > switch {{
  background: alpha(@surface2, 0.8);
  border-radius: 20px;
  border: none;
  min-width: 50px;
  min-height: 26px;
}}

.widget-dnd > switch:checked {{
  background: @mauve;
  box-shadow: 0 4px 12px alpha(@mauve, 0.4);
}}

.widget-dnd > switch slider {{
  background: @text;
  border-radius: 50%;
  border: none;
}}

.notification {{
  background: alpha(@surface0, 0.7);
  backdrop-filter: blur(15px);
  border-radius: 12px;
  margin: 8px 12px;
  padding: 0;
  border: 1px solid alpha(@surface2, 0.5);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  transition: all 200ms ease;
}}

.notification:hover {{
  background: alpha(@surface1, 0.8);
  border-color: alpha(@mauve, 0.6);
  transform: translateX(-4px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}}

.notification-content {{
  background: transparent;
  padding: 12px;
  border-radius: 12px;
}}

.notification-default-action {{
  background: transparent;
  padding: 0;
  margin: 0;
}}

.summary {{
  color: @text;
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 4px;
}}

.body {{
  color: @subtext0;
  font-size: 13px;
  font-weight: 500;
}}

.time {{
  color: @overlay1;
  font-size: 11px;
  font-weight: 600;
  margin-top: 4px;
}}

.notification-icon {{
  min-width: 48px;
  min-height: 48px;
  margin-right: 12px;
  border-radius: 10px;
}}

.app-icon {{
  color: @mauve;
}}

.notification-action {{
  background: alpha(@mauve, 0.3);
  color: @text;
  border-radius: 8px;
  margin: 6px;
  padding: 8px 12px;
  border: 1px solid alpha(@mauve, 0.4);
  font-weight: 600;
  transition: all 200ms ease;
}}

.notification-action:hover {{
  background: alpha(@mauve, 0.5);
  border-color: @mauve;
  box-shadow: 0 4px 12px alpha(@mauve, 0.3);
}}

.close-button {{
  background: alpha(@red, 0.8);
  color: @crust;
  border-radius: 8px;
  padding: 6px 10px;
  margin: 8px;
  border: none;
  font-size: 16px;
  font-weight: 700;
  box-shadow: 0 4px 12px alpha(@red, 0.4);
  transition: all 200ms ease;
}}

.close-button:hover {{
  background: @red;
  box-shadow: 0 6px 16px alpha(@red, 0.6);
  transform: scale(1.1);
}}

.notification.critical {{
  border: 2px solid @red;
  background: alpha(@red, 0.15);
}}

.notification.critical .summary {{
  color: @red;
}}

scrollbar {{
  background: transparent;
  width: 8px;
}}

scrollbar slider {{
  background: alpha(@mauve, 0.5);
  border-radius: 8px;
  min-height: 40px;
}}

scrollbar slider:hover {{
  background: alpha(@mauve, 0.7);
}}

.blank-window {{
  background: alpha(@base, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 2px solid alpha(@mauve, 0.4);
}}

.widget-label {{
  color: @subtext0;
  font-size: 16px;
  margin: 20px;
}}
"""


def generate_rofi(theme_name: str, colors: Dict[str, str]) -> str:
    """Generate Rofi theme"""
    mapped = get_mapped_colors(theme_name, colors)
    
    return f"""configuration {{
    show-icons: false;
}}

* {{
    bg:     {mapped['base']};
    bg-alt: {mapped['mantle']};
    fg:     {mapped['text']};
    accent: {mapped['mauve']};
    green:  {mapped['green']};
    red:    {mapped['red']};
    selected: {mapped['mauve']};
    background: {mapped['base']};
    background-alt: {mapped['surface0']};
    foreground: {mapped['text']};
    urgent: {mapped['red']};
    active: {mapped['green']};

    font: "JetBrainsMono Nerd Font 12";
}}

window {{
    transparency: "real";
    location: center;
    anchor: center;
    fullscreen: false;
    width: 640px;
    padding: 0px;
    border: 0px solid;
    border-radius: 18px;
    border-color: @selected;
    background-color: @background;
}}

mainbox {{
    enabled: true;
    spacing: 12px;
    margin: 0px;
    padding: 20px;
    border: 0px solid;
    border-radius: 0px;
    background-color: transparent;
    children: [ "inputbar", "listview" ];
}}

inputbar {{
    enabled: true;
    spacing: 15px;
    margin: 0px;
    padding: 0px;
    border: 0px;
    border-radius: 0px;
    background-color: transparent;
    text-color: @foreground;
    children: [ "textbox-prompt-colon", "prompt" ];
}}

textbox-prompt-colon {{
    enabled: true;
    expand: false;
    str: "";
    padding: 12px 15px;
    border-radius: 100%;
    background-color: @urgent;
    text-color: @background;
    font: "feather bold 20";
    vertical-align: 0.5;
    horizontal-align: 0.5;
}}

prompt {{
    enabled: true;
    padding: 12px 20px;
    border-radius: 100%;
    background-color: @active;
    text-color: @background;
    font: "JetBrainsMono Nerd Font 12";
    vertical-align: 0.5;
    horizontal-align: 0.5;
}}

listview {{
    enabled: true;
    columns: 5;
    lines: 1;
    cycle: true;
    dynamic: true;
    scrollbar: false;
    layout: vertical;
    reverse: false;
    fixed-height: true;
    fixed-columns: true;
    spacing: 12px;
    margin: 0px 0px 0px -10px;
    padding: 0px;
    border: 0px solid;
    border-radius: 0px;
    background-color: transparent;
    text-color: @foreground;
    cursor: "default";
}}

element {{
    enabled: true;
    margin: 0px;
    padding: 0px;
    border-radius: 100%;
    background-color: @background-alt;
    text-color: @foreground;
    cursor: pointer;
    orientation: vertical;
}}

element-text {{
    font: "feather bold 28";
    background-color: transparent;
    text-color: inherit;
    cursor: inherit;
    horizontal-align: 0.5;
    vertical-align: 0.5;
    padding: 45px;
}}

element selected.normal {{
    background-color: @accent;
    text-color: @background;
}}
"""


def generate_btop(theme_name: str, colors: Dict[str, str]) -> str:
    """Generate Btop theme"""
    mapped = get_mapped_colors(theme_name, colors)
    
    return f"""theme[main_bg]="{mapped['crust']}"
theme[main_fg]="{mapped['text']}"
theme[title]="{mapped['pink']}"
theme[hi_fg]="{mapped['mauve']}"
theme[selected_bg]="{mapped['surface2']}"
theme[selected_fg]="{mapped['pink']}"
theme[inactive_fg]="{mapped['overlay0']}"
theme[graph_text]="{mapped['subtext1']}"
theme[meter_bg]="{mapped['base']}"
theme[proc_misc]="{mapped['pink']}"
theme[cpu_box]="{mapped['mauve']}"
theme[mem_box]="{mapped['green']}"
theme[net_box]="{mapped['blue']}"
theme[proc_box]="{mapped['yellow']}"
theme[div_line]="{mapped['surface1']}"
theme[temp_start]="{mapped['green']}"
theme[temp_mid]="{mapped['yellow']}"
theme[temp_end]="{mapped['red']}"
theme[cpu_start]="{mapped['blue']}"
theme[cpu_mid]="{mapped['mauve']}"
theme[cpu_end]="{mapped['pink']}"
theme[free_start]="{mapped['mauve']}"
theme[free_mid]="{mapped['pink']}"
theme[free_end]="{mapped['maroon']}"
theme[cached_start]="{mapped['sky']}"
theme[cached_mid]="{mapped['lavender']}"
theme[cached_end]="{mapped['mauve']}"
theme[available_start]="{mapped['peach']}"
theme[available_mid]="{mapped['yellow']}"
theme[available_end]="{mapped['green']}"
theme[used_start]="{mapped['red']}"
theme[used_mid]="{mapped['peach']}"
theme[used_end]="{mapped['yellow']}"
theme[download_start]="{mapped['green']}"
theme[download_mid]="{mapped['sky']}"
theme[download_end]="{mapped['blue']}"
theme[upload_start]="{mapped['yellow']}"
theme[upload_mid]="{mapped['peach']}"
theme[upload_end]="{mapped['red']}"
theme[process_start]="{mapped['blue']}"
theme[process_mid]="{mapped['lavender']}"
theme[process_end]="{mapped['mauve']}"
"""


def generate_cava(theme_name: str, colors: Dict[str, str]) -> str:
    """Generate Cava config"""
    mapped = get_mapped_colors(theme_name, colors)
    grad = [mapped['mauve'], mapped['pink'], mapped['red'], mapped['peach'], mapped['yellow'], mapped['green']]
    
    return f"""[general]
framerate = 60
bars = 0
bar_width = 2
bar_spacing = 1

[input]
method = pulse
source = auto

[output]
method = ncurses
channels = stereo
mono_option = average
reverse = 0

[color]
gradient = 1
gradient_count = 6
gradient_color_1 = '{grad[0]}'
gradient_color_2 = '{grad[1]}'
gradient_color_3 = '{grad[2]}'
gradient_color_4 = '{grad[3]}'
gradient_color_5 = '{grad[4]}'
gradient_color_6 = '{grad[5]}'

[smoothing]
monstercat = 1
waves = 0
gravity = 100
ignore = 0
"""


def generate_alacritty(theme_name: str, colors: Dict[str, str]) -> str:
    """Generate Alacritty theme"""
    mapped = get_mapped_colors(theme_name, colors)
    
    return f"""[colors.primary]
background = '{mapped['base']}'
foreground = '{mapped['text']}'

[colors.cursor]
text = '{mapped['base']}'
cursor = '{mapped['pink']}'

[colors.selection]
text = '{mapped['base']}'
background = '{mapped['pink']}'

[colors.normal]
black = '{mapped['surface1']}'
red = '{mapped['red']}'
green = '{mapped['green']}'
yellow = '{mapped['yellow']}'
blue = '{mapped['blue']}'
magenta = '{mapped['pink']}'
cyan = '{mapped['teal']}'
white = '{mapped['subtext1']}'

[colors.bright]
black = '{mapped['surface2']}'
red = '{mapped['red']}'
green = '{mapped['green']}'
yellow = '{mapped['yellow']}'
blue = '{mapped['blue']}'
magenta = '{mapped['pink']}'
cyan = '{mapped['teal']}'
white = '{mapped['subtext0']}'
"""


def generate_kitty(theme_name: str, colors: Dict[str, str]) -> str:
    """Generate Kitty theme"""
    mapped = get_mapped_colors(theme_name, colors)
    
    return f"""foreground {mapped['text']}
background {mapped['base']}
selection_foreground {mapped['base']}
selection_background {mapped['pink']}
cursor {mapped['pink']}
cursor_text_color {mapped['base']}
url_color {mapped['pink']}
active_border_color {mapped['lavender']}
inactive_border_color {mapped['overlay0']}
bell_border_color {mapped['yellow']}
active_tab_foreground {mapped['crust']}
active_tab_background {mapped['mauve']}
inactive_tab_foreground {mapped['text']}
inactive_tab_background {mapped['mantle']}
tab_bar_background {mapped['crust']}
color0 {mapped['surface1']}
color8 {mapped['surface2']}
color1 {mapped['red']}
color9 {mapped['red']}
color2  {mapped['green']}
color10 {mapped['green']}
color3  {mapped['yellow']}
color11 {mapped['yellow']}
color4  {mapped['blue']}
color12 {mapped['blue']}
color5  {mapped['pink']}
color13 {mapped['pink']}
color6  {mapped['teal']}
color14 {mapped['teal']}
color7  {mapped['subtext1']}
color15 {mapped['subtext0']}
"""


def generate_theme_menu(theme_name: str, colors: Dict[str, str]) -> str:
    """Generate theme switcher menu for Rofi"""
    mapped = get_mapped_colors(theme_name, colors)
    
    return f"""configuration {{
	modi:                       "drun";
    show-icons:                 false;
    display-drun:               "󰏘";
	drun-display-format:        "{{name}}";
}}

* {{
    bg:     {mapped['base']};
    bg-alt: {mapped['mantle']};
    fg:     {mapped['text']};
    accent: {mapped['mauve']};
    surface: {mapped['surface0']};
    
    background: {mapped['base']};
    background-alt: {mapped['surface0']};
    foreground: {mapped['text']};
    selected: {mapped['mauve']};
    
    font: "Ubuntu Nerd Font 13";
}}

window {{
    transparency:                "real";
    location:                    center;
    anchor:                      center;
    fullscreen:                  false;
    width:                       450px;
    x-offset:                    0px;
    y-offset:                    0px;

    enabled:                     true;
    margin:                      0px;
    padding:                     0px;
    border:                      0px solid;
    border-radius:               12px;
    border-color:                @selected;
    background-color:            @background;
    cursor:                      "default";
}}

mainbox {{
    enabled:                     true;
    spacing:                     0px;
    margin:                      0px;
    padding:                     0px;
    border:                      0px solid;
    border-radius:               0px 0px 0px 0px;
    border-color:                @selected;
    background-color:            transparent;
    children:                    [ "inputbar", "listview" ];
}}

inputbar {{
    enabled:                     true;
    spacing:                     10px;
    margin:                      0px;
    padding:                     15px;
    border:                      0px solid;
    border-radius:               12px 12px 0px 0px;
    border-color:                @selected;
    background-color:            @selected;
    text-color:                  @background;
    children:                    [ "prompt", "entry" ];
}}

prompt {{
    enabled:                     true;
    background-color:            inherit;
    text-color:                  inherit;
}}

entry {{
    enabled:                     true;
    background-color:            inherit;
    text-color:                  inherit;
    cursor:                      text;
    placeholder:                 "Search themes...";
    placeholder-color:           inherit;
}}

listview {{
    enabled:                     true;
    columns:                     1;
    lines:                       7;
    cycle:                       true;
    dynamic:                     true;
    scrollbar:                   false;
    layout:                      vertical;
    reverse:                     false;
    fixed-height:                true;
    fixed-columns:               true;
    
    spacing:                     5px;
    margin:                      0px;
    padding:                     10px;
    border:                      0px solid;
    border-radius:               0px;
    border-color:                @selected;
    background-color:            transparent;
    text-color:                  @foreground;
    cursor:                      "default";
}}

element {{
    enabled:                     true;
    spacing:                     10px;
    margin:                      0px;
    padding:                     10px;
    border:                      0px solid;
    border-radius:               8px;
    border-color:                @selected;
    background-color:            transparent;
    text-color:                  @foreground;
    cursor:                      pointer;
}}

element normal.normal {{
    background-color:            @background;
    text-color:                  @foreground;
}}

element selected.normal {{
    background-color:            @selected;
    text-color:                  @background;
}}

element-text {{
    background-color:            transparent;
    text-color:                  inherit;
    highlight:                   inherit;
    cursor:                      inherit;
    vertical-align:              0.5;
    horizontal-align:            0.0;
}}
"""


# ============================================================================
# THEME GENERATION
# ============================================================================

def generate_theme(theme_name: str, verbose: bool = False) -> bool:
    """Generate all theme files for a given theme"""
    if verbose:
        print(f"📦 Generating theme: {theme_name}")
    
    # Load palette
    colors = load_palette(theme_name)
    if not colors:
        return False
    
    # Get mapped colors
    mapped = get_mapped_colors(theme_name, colors)
    
    # Create theme directory
    theme_dir = THEMES_DIR / theme_name
    theme_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate each theme file
    theme_files = {
        "waybar.css": generate_waybar(theme_name, mapped),
        "swaync.css": generate_swaync(theme_name, mapped),
        "rofi.rasi": generate_rofi(theme_name, colors),
        "btop.theme": generate_btop(theme_name, colors),
        "cava": generate_cava(theme_name, colors),
        "alacritty-theme.toml": generate_alacritty(theme_name, colors),
        "kitty-theme.conf": generate_kitty(theme_name, colors),
        "theme-switcher-menu.rasi": generate_theme_menu(theme_name, colors),
    }
    
    # Write files
    for filename, content in theme_files.items():
        file_path = theme_dir / filename
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            if verbose:
                print(f"  ✓ {filename}")
        except Exception as e:
            print(f"  ❌ Error writing {filename}: {e}")
            return False
    
    if verbose:
        print(f"✅ {theme_name} generated successfully\n")
    
    return True


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Generate theme files for Hyprland dotfiles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      # Generate all themes
  %(prog)s -t tokyo-night       # Generate only Tokyo Night
  %(prog)s -l                   # List available palettes
  %(prog)s -v                   # Verbose output
        """
    )
    
    parser.add_argument(
        '-t', '--theme',
        help='Generate only the specified theme'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List available palette files'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Only validate palettes without generating themes'
    )
    
    args = parser.parse_args()
    
    # Ensure directories exist
    PALETTES_DIR.mkdir(parents=True, exist_ok=True)
    THEMES_DIR.mkdir(parents=True, exist_ok=True)
    
    # List palettes
    if args.list:
        palettes = discover_palettes()
        print("Available palettes:")
        print("=" * 40)
        for palette in palettes:
            print(f"  • {palette}")
        print(f"\nTotal: {len(palettes)} palettes")
        return 0
    
    # Discover available themes
    if args.theme:
        themes = [args.theme]
        print(f"🎨 Generating theme: {args.theme}\n")
    else:
        themes = discover_palettes()
        if not themes:
            print("❌ No palette files found in:", PALETTES_DIR)
            return 1
        print(f"🎨 Found {len(themes)} themes to generate\n")
    
    # Validate only
    if args.validate:
        print("Validating palettes...\n")
        all_valid = True
        for theme in themes:
            colors = load_palette(theme)
            if colors:
                print(f"✅ {theme}: Valid")
            else:
                all_valid = False
        
        return 0 if all_valid else 1
    
    # Generate themes
    success_count = 0
    fail_count = 0
    
    for theme in themes:
        if generate_theme(theme, verbose=args.verbose):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print("=" * 50)
    print(f"✅ Successfully generated: {success_count}/{len(themes)} themes")
    if fail_count > 0:
        print(f"❌ Failed: {fail_count} themes")
        return 1
    
    print("\n🎉 All themes generated successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())