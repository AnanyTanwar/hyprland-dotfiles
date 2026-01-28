#!/usr/bin/env python3

import json
from pathlib import Path

BASE_DIR = Path.home() / ".config" / "theme-switcher"
PALETTES_DIR = BASE_DIR / "palettes"
THEMES_DIR = BASE_DIR / "themes"

def load_palette(theme_name):
    palette_file = PALETTES_DIR / f"{theme_name}.json"
    with open(palette_file, 'r') as f:
        return json.load(f)

def get_mapped_colors(theme_name, colors):
    if theme_name.startswith("catppuccin"):
        return {
            'base': colors['base'], 'mantle': colors['mantle'], 'crust': colors['crust'],
            'text': colors['text'], 'subtext0': colors['subtext0'], 'subtext1': colors['subtext1'],
            'surface0': colors['surface0'], 'surface1': colors['surface1'], 'surface2': colors['surface2'],
            'overlay0': colors['overlay0'], 'overlay1': colors['overlay1'],
            'blue': colors['blue'], 'lavender': colors['lavender'], 'sapphire': colors['sapphire'],
            'sky': colors['sky'], 'teal': colors['teal'], 'green': colors['green'],
            'yellow': colors['yellow'], 'peach': colors['peach'], 'maroon': colors['maroon'],
            'red': colors['red'], 'mauve': colors['mauve'], 'pink': colors['pink']
        }
    elif theme_name == "rose-pine":
        return {
            'base': colors['base'], 'mantle': colors['surface'], 'crust': colors['base'],
            'text': colors['text'], 'subtext0': colors['subtle'], 'subtext1': colors['subtle'],
            'surface0': colors['surface'], 'surface1': colors['overlay'], 'surface2': colors['highlight_med'],
            'overlay0': colors['muted'], 'overlay1': colors['subtle'],
            'blue': colors['pine'], 'lavender': colors['iris'], 'sapphire': colors['foam'],
            'sky': colors['foam'], 'teal': colors['foam'], 'green': colors['foam'],
            'yellow': colors['gold'], 'peach': colors['gold'], 'maroon': colors['love'],
            'red': colors['love'], 'mauve': colors['iris'], 'pink': colors['rose']
        }
    elif theme_name == "nord":
        return {
            'base': colors['nord0'], 'mantle': colors['nord1'], 'crust': colors['nord0'],
            'text': colors['nord4'], 'subtext0': colors['nord4'], 'subtext1': colors['nord5'],
            'surface0': colors['nord1'], 'surface1': colors['nord2'], 'surface2': colors['nord3'],
            'overlay0': colors['nord3'], 'overlay1': colors['nord4'],
            'blue': colors['nord10'], 'lavender': colors['nord15'], 'sapphire': colors['nord8'],
            'sky': colors['nord8'], 'teal': colors['nord7'], 'green': colors['nord14'],
            'yellow': colors['nord13'], 'peach': colors['nord12'], 'maroon': colors['nord11'],
            'red': colors['nord11'], 'mauve': colors['nord15'], 'pink': colors['nord15']
        }
    elif theme_name == "gruvbox":
        return {
            'base': colors['bg'], 'mantle': colors['bg0'], 'crust': colors['bg'],
            'text': colors['fg'], 'subtext0': colors['fg2'], 'subtext1': colors['fg1'],
            'surface0': colors['bg1'], 'surface1': colors['bg2'], 'surface2': colors['bg3'],
            'overlay0': colors['bg4'], 'overlay1': colors['gray'],
            'blue': colors['blue'], 'lavender': colors['purple'], 'sapphire': colors['aqua'],
            'sky': colors['aqua'], 'teal': colors['aqua'], 'green': colors['green'],
            'yellow': colors['yellow'], 'peach': colors['orange'], 'maroon': colors['red'],
            'red': colors['red'], 'mauve': colors['purple'], 'pink': colors['purple']
        }
    elif theme_name == "tokyo-night":
        return {
            'base': colors['bg'], 'mantle': colors['bg_dark'], 'crust': colors['bg_dark'],
            'text': colors['fg'], 'subtext0': colors['fg_dark'], 'subtext1': colors['fg'],
            'surface0': colors['bg_highlight'], 'surface1': colors['terminal_black'], 'surface2': colors['dark3'],
            'overlay0': colors['comment'], 'overlay1': colors['dark5'],
            'blue': colors['blue'], 'lavender': colors['purple'], 'sapphire': colors['cyan'],
            'sky': colors['cyan'], 'teal': colors['teal'], 'green': colors['green'],
            'yellow': colors['yellow'], 'peach': colors['orange'], 'maroon': colors['red1'],
            'red': colors['red'], 'mauve': colors['purple'], 'pink': colors['magenta']
        }
    elif theme_name == "dracula":
        return {
            'base': colors['bg'], 'mantle': colors['bg'], 'crust': colors['bg'],
            'text': colors['fg'], 'subtext0': colors['comment'], 'subtext1': colors['fg'],
            'surface0': colors['current_line'], 'surface1': colors['selection'], 'surface2': colors['selection'],
            'overlay0': colors['comment'], 'overlay1': colors['comment'],
            'blue': colors['cyan'], 'lavender': colors['purple'], 'sapphire': colors['cyan'],
            'sky': colors['cyan'], 'teal': colors['cyan'], 'green': colors['green'],
            'yellow': colors['yellow'], 'peach': colors['orange'], 'maroon': colors['red'],
            'red': colors['red'], 'mauve': colors['purple'], 'pink': colors['pink']
        }
    return {}

def generate_waybar(theme_name, mapped):
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

def generate_swaync(theme_name, mapped):
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

def generate_rofi(theme_name, colors):
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

def generate_btop(theme_name, colors):
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

def generate_cava(theme_name, colors):
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
def generate_alacritty(theme_name, colors):
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

def generate_kitty(theme_name, colors):
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

def generate_theme_menu(theme_name, colors):
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

def main():
    themes = ["catppuccin-mocha", "catppuccin-latte", "rose-pine", "nord", "gruvbox", "tokyo-night", "dracula"]
    
    for theme in themes:
        print(f"Generating {theme}...")
        colors = load_palette(theme)
        mapped = get_mapped_colors(theme, colors)
        theme_dir = THEMES_DIR / theme
       
        with open(theme_dir / "rofi.rasi", 'w') as f:
            f.write(generate_rofi(theme, colors))
        
        with open(theme_dir / "btop.theme", 'w') as f:
            f.write(generate_btop(theme, colors))
        
        with open(theme_dir / "cava", 'w') as f:
            f.write(generate_cava(theme, colors))
        
        with open(theme_dir / "alacritty-theme.toml", 'w') as f:
            f.write(generate_alacritty(theme, colors))
        
        with open(theme_dir / "kitty-theme.conf", 'w') as f:
            f.write(generate_kitty(theme, colors))
        
        with open(theme_dir / "waybar.css", 'w') as f:
            f.write(generate_waybar(theme, mapped))
        
        with open(theme_dir / "swaync.css", 'w') as f:
            f.write(generate_swaync(theme, mapped))
        
        with open(theme_dir / "theme-switcher-menu.rasi", 'w') as f:
            f.write(generate_theme_menu(theme, colors))
        
        print(f"✓ {theme} generated")
    
    print("\n✓ All themes generated!")

if __name__ == "__main__":
    main()