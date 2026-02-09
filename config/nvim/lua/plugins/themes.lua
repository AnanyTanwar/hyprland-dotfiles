return {
    -- Catppuccin (default)
    {
        "catppuccin/nvim",
        name = "catppuccin",
        priority = 1000,
        config = function()
            require("catppuccin").setup({
                flavour = "mocha",  -- latte, frappe, macchiato, mocha
                transparent_background = true,
                integrations = {
                    cmp = true,
                    gitsigns = true,
                    nvimtree = true,
                    treesitter = true,
                    telescope = true,
                }
            })
        end
    },

    -- Tokyo Night
    {
        "folke/tokyonight.nvim",
        lazy = true,
        opts = {
            style = "night",  -- storm, moon, night
            transparent = true,
        }
    },

    -- Dracula
    {
        "Mofiqul/dracula.nvim",
        lazy = true,
        config = function()
            require("dracula").setup({
                transparent_bg = true,
            })
        end
    },

    -- Rose Pine
    {
        "rose-pine/neovim",
        name = "rose-pine",
        lazy = true,
        config = function()
            require("rose-pine").setup({
                variant = "main",  -- auto, main, moon, dawn
                disable_background = true,
            })
        end
    },

    -- Gruvbox
    {
        "ellisonleao/gruvbox.nvim",
        lazy = true,
        config = function()
            require("gruvbox").setup({
                transparent_mode = true,
            })
        end
    },

    -- Nord
    {
        "shaunsingh/nord.nvim",
        lazy = true,
        config = function()
            vim.g.nord_disable_background = true
        end
    },
}
