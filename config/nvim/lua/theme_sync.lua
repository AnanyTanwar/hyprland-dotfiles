local M = {}

local theme_file = vim.fn.expand("~/.config/theme-switcher/.current-theme")

local theme_map = {
  ["catppuccin-mocha"] = function()
    vim.g.catppuccin_flavour = "mocha"
    return "catppuccin"
  end,
  ["catppuccin-latte"] = function()
    vim.g.catppuccin_flavour = "latte"
    return "catppuccin"
  end,
  ["tokyo-night"] = "tokyonight",
  ["gruvbox"] = "gruvbox",
  ["nord"] = "nord",
  ["dracula"] = "dracula",
  ["rose-pine"] = "rose-pine",
}

function M.apply()
  local f = io.open(theme_file, "r")
  if not f then
    pcall(vim.cmd.colorscheme, "catppuccin")
    return
  end

  local theme = f:read("*l")
  f:close()

  local mapped = theme_map[theme]
  if not mapped then return end

  local scheme = type(mapped) == "function" and mapped() or mapped

  vim.schedule(function()
    pcall(vim.cmd.colorscheme, scheme)
  end)
end

-- After lazy finishes loading plugins
vim.api.nvim_create_autocmd("User", {
  pattern = "LazyDone",
  callback = function()
    M.apply()
  end,
})

-- When coming back to Neovim (WIN+T -> Alt+Tab)
vim.api.nvim_create_autocmd("FocusGained", {
  callback = function()
    M.apply()
  end,
})

return M
