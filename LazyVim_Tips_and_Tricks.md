
# 🧠 LazyVim Tips & Tricks Cheat Sheet

## 📁 Jump Between Open Files

### Buffers (default in LazyVim)
- `:bnext`, `:bn` → Next buffer  
- `:bprev`, `:bp` → Previous buffer  
- `:b <num>` → Go to buffer by number  
- `:ls` → List all buffers  
- `<S-h>` / `<S-l>` → Previous/Next buffer (LazyVim mapped)  
- `<leader><Tab>` → Last-used buffer toggle  

### Telescope buffer switch
- `<leader><space>` → Fuzzy buffer switcher via Telescope  

### Tabs
- `gt` / `gT` → Next/previous tab  
- `:tabnext`, `:tabprev` → Tab navigation  

### Window splits
- `<C-w>w` → Cycle splits  
- `<C-w>h/j/k/l` → Move between splits  

---

## 🗂 Jump Back to File Explorer

### Neo-tree (default in LazyVim)
- `<leader>e` → Focus or toggle file explorer  
- `\` → Toggle Neo-tree  
- `<C-w>h` → Focus left (Neo-tree split)  

### NvimTree (if used)
- `:NvimTreeFocus` → Jump back to explorer  
- `<C-w>h` → Window move  

---

## 💾 Enable Autosave in LazyVim

### Option 1: Plugin-Based (auto-save.nvim)
Create `~/.config/nvim/lua/plugins/auto-save.lua`:
```lua
return {
  "Pocco81/auto-save.nvim",
  config = function()
    require("auto-save").setup({
      enabled = true,
      execution_message = { message = function() return "" end },
      trigger_events = {"InsertLeave", "TextChanged"},
    })
  end,
}
```

### Option 2: Built-in Autocmd (no plugin)
```lua
vim.api.nvim_create_autocmd({"InsertLeave", "TextChanged"}, {
  pattern = "*",
  callback = function()
    if vim.bo.modifiable and vim.bo.buftype == "" then
      vim.cmd("silent! write")
    end
  end,
})
```

---

## 💬 Comment/Uncomment Blocks

### Normal Mode
- `gcc` → Comment/uncomment line

### Visual Mode
- `gc` → Toggle line comments  
- `gb` → Toggle block comments (if supported)

### Motion Examples
- `gc3j` → Comment 3 lines down  
- `gc}` → Comment to end of paragraph

---

## 🆕 Create an Empty File in Explorer

### Neo-tree
- `<leader>e` → Open explorer  
- `a` → Create file  
- `A` → Create directory

### NvimTree
- Open explorer → press `a` → enter filename

---

## ✂️ Cut a Block of Code (Visual Mode)

1. Select code using `v`, `V`, or `<C-v>`  
2. Press `d` or `x` → Cuts (deletes and copies)  
3. Use `p` or `P` to paste elsewhere  

### Avoid overwriting clipboard:
- `"_d` → Cut without copying

---

## 🔍 Find in Current File

### Telescope (LazyVim default)
- `<leader>/` → Search within current buffer  
- `<leader>sg` → Search project-wide (live grep)  
- `<leader>sf` → Find files

### Vim-native search
- `/` → Search forward  
- `?` → Search backward  
- `n` / `N` → Jump to next/prev match
