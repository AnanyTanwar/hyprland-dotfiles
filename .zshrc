# ============================================================================
# P10k Configuration (COMMENTED OUT - Using Starship for theme testing)
# ============================================================================
# Uncomment these lines to switch back to Powerlevel10k:
#
# if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
#   source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
# fi
# source ~/.powerlevel10k/powerlevel10k.zsh-theme
# [[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh

# ============================================================================
# Starship Prompt (ACTIVE - for theme testing)
# ============================================================================
# Comment this line out to switch back to P10k:
eval "$(starship init zsh)"

# ============================================================================
# History
# ============================================================================
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000

# ============================================================================
# Options
# ============================================================================
setopt autocd extendedglob
bindkey -e
zstyle :compinstall filename '/home/chadakt/.zshrc'

# ============================================================================
# Tools
# ============================================================================

# Zoxide
eval "$(zoxide init zsh)"

# FzF
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# Completion
autoload -Uz compinit
compinit

# ============================================================================
# Aliases
# ============================================================================
alias clear="clear && printf \"\""
alias ls="exa -l"

# ============================================================================
# Path
# ============================================================================
export PATH="$HOME/.local/bin:$PATH"

# ============================================================================
# Quick Theme Switcher
# ============================================================================
# Uncomment to add a quick alias for theme switching:
# alias theme="~/.config/theme-switcher/scripts/switcher.sh"
