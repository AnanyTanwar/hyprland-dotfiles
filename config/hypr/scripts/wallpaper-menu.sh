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

# Support common image formats
shopt -s nullglob
entries=""
count=0

for img in "$WALLDIR"/*.{png,jpg,jpeg,webp,bmp}; do
  [[ -f "$img" ]] || continue
  name="$(basename "$img")"
  thumb="$CACHE/$name.png"

  # Generate thumbnail if doesn't exist
  if [ ! -f "$thumb" ]; then
    magick "$img" -resize 400x400^ -gravity center -extent 400x400 -quality 90 "$thumb" 2>/dev/null
  fi

  # Mark current wallpaper with star
  if [[ "$img" == "$CURRENT" ]]; then
    entries+="⭐ $name\x00icon\x1f$thumb\n"
  else
    entries+="$name\x00icon\x1f$thumb\n"
  fi
  
  ((count++))
done

# Exit gracefully if no wallpapers
if [ $count -eq 0 ]; then
  notify-send "Wallpaper Menu 🖼️" "No images found in $WALLDIR" -u normal
  exit 1
fi

# Add random option at top
entries="🎲 Random Wallpaper\x00icon\x1f$HOME/.config/rofi/icons/random.png\n$entries"

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
chosen=$(echo "$chosen" | sed 's/^⭐ //' | xargs)

# Handle random selection
if [[ "$chosen" == "🎲 Random Wallpaper" ]]; then
  wallpapers=("$WALLDIR"/*.{png,jpg,jpeg,webp,bmp})
  chosen=$(basename "${wallpapers[RANDOM % ${#wallpapers[@]}]}")
  notify-send "Random Wallpaper! 🎲" "Selected: $chosen" -u low -t 3000
fi

WALLPATH="$WALLDIR/$chosen"

# Set wallpaper with swww
if command -v swww &> /dev/null; then
  swww img "$WALLPATH" \
    --transition-type grow \
    --transition-pos 0.925,0.977 \
    --transition-duration 1.5 \
    --transition-fps 60
    
  # Save current wallpaper
  echo "$WALLPATH" > "$CURRENT_WALL"
  
  # Success notification with preview
  notify-send "Wallpaper Changed! 🎨" "$chosen" \
    -u low \
    -t 3000 \
    -i "$WALLPATH"
else
  notify-send "Error ❌" "swww not found!" -u critical
fi
