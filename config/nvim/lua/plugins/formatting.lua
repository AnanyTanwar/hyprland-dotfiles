return {
	{
		"WhoIsSethDaniel/mason-tool-installer.nvim",
		config = function()
			require("mason-tool-installer").setup({
				ensure_installed = {
					"stylua",
					"clang-format",
					"black",
					"prettier",
				},
			})
		end,
	},

	{
		"stevearc/conform.nvim",
		event = { "BufReadPre", "BufNewFile" },
		config = function()
			local conform = require("conform")

			conform.setup({
				formatters_by_ft = {
					lua = { "stylua" },
					c = { "clang_format" },
					cpp = { "clang_format" },
					python = { "black" },
					javascript = { "prettier" },
					html = { "prettier" },
					css = { "prettier" },
				},

				format_on_save = {
					timeout_ms = 2000,
					lsp_fallback = true,
				},
			})

			vim.keymap.set("n", "<leader>gf", function()
				conform.format({ async = true, lsp_fallback = true })
			end, { desc = "Format Code" })
		end,
	},
}
