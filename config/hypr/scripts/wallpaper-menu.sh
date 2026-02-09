#!/bin/bash
WALLDIR="$HOME/Pictures/wallpapers"
CACHE="$HOME/.cache/wallpapers"
CURRENT_WALL="$HOME/.cache/current_wallpaper"
mkdir -p "$CACHE"

# Get current wallpaper
CURRENT=""
if [ -f "$CURRENT_WALL" ]; then
    CURRENT=$(cat "$CURRENT_WALL")
fi

# Support common image formats - including subdirectories
shopt -s nullglob
entries=""
count=0

# Search in main directory and subdirectories
while IFS= read -r -d '' img; do
  name="$(basename "$img")"
  folder="$(basename "$(dirname "$img")")"
  
  cache_name="${folder}_${name}"
  thumb="$CACHE/${cache_name}.png"
  
  # Generate thumbnail if doesn't exist
  if [ ! -f "$thumb" ]; then
    magick "$img" -resize 400x400^ -gravity center -extent 400x400 -quality 90 "$thumb" 2>/dev/null
  fi
  
  # Display name with folder
  if [[ "$folder" == "wallpapers" ]]; then
    display_name="$name"
  else
    display_name="[$folder] $name"
  fi
  
  # Mark current wallpaper with star
  if [[ "$img" == "$CURRENT" ]]; then
    entries+="⭐ $display_name\x00icon\x1f$thumb\n"
  else
    entries+="$display_name\x00icon\x1f$thumb\n"
  fi
  ((count++))
done < <(find "$WALLDIR" -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.webp" -o -iname "*.bmp" \) -print0)

# Exit gracefully if no wallpapers
if [ $count -eq 0 ]; then
  notify-send "Wallpaper Menu 🖼️" "No images found in $WALLDIR" -u normal
  exit 1
fi

# Show rofi menu
chosen=$(printf "%b" "$entries" | rofi \
  -dmenu \
  -show-icons \
  -p "󰸉 Select Wallpaper ($count available)" \
  -theme "$HOME/.config/rofi/wallpaper.rasi" \
  -selected-row 0 \
  -markup-rows)

[ -z "$chosen" ] && exit 0

# Clean the choice
chosen=$(echo "$chosen" | sed 's/^⭐ //' | sed 's/^\[.*\] //' | xargs)

# Find the actual file path
WALLPATH=$(find "$WALLDIR" -type f -name "$chosen" | head -1)

# Set wallpaper with swww
if command -v swww &> /dev/null; then
  swww img "$WALLPATH" \
    --transition-type grow \
    --transition-pos 0.925,0.977 \
    --transition-duration 1.5 \
    --transition-fps 60
  
  echo "$WALLPATH" > "$CURRENT_WALL"
  
  notify-send "Wallpaper Changed! 🎨" "$chosen" \
    -u low \
    -t 3000 \
    -i "$WALLPATH"
else
  notify-send "Error ❌" "swww not found!" -u critical
fi
