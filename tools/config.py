# --- PROJECT METADATA ---
PROJECT_NAME = "MY GAMEBOY GAME"
ROM_NAME     = "game.gb"

# --- PATHS ---
SRC_DIR      = "src"
INC_DIR      = "inc"
OBJ_DIR_REL  = "obj/release"
OBJ_DIR_DBG  = "obj/debug"
DEBUG_OUT    = "debug"

# --- TOOLS ---
ASM  = "rgbasm"
LINK = "rgblink"
FIX  = "rgbfix"

# --- EMULATORS ---
EMU_PATHS = {
    "WSL":   "/mnt/c/Emulators/bgb/bgb.exe",
    "LINUX": "sameboy",
    "WIN":   "C:\\Emulators\\bgb\\bgb.exe"
}

# --- VISUALS (COLORS) ---
class Colors:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    GREEN  = "\033[38;5;119m" 
    DARK   = "\033[38;5;22m"  
    FRAME  = "\033[38;5;240m" 
    ERR    = "\033[38;5;196m" 
    WARN   = "\033[38;5;214m" 
    BLUE   = "\033[38;5;75m"

# --- TUI SETTINGS ---
SCREEN_W = 74 
SCREEN_H = 16

LOGO = [
    "  ██████   █████  ███    ███ ███████     ██████   ██████  ██    ██ ",
    " ██       ██   ██ ████  ████ ██          ██   ██ ██    ██  ██  ██  ",
    " ██   ███ ███████ ██ ████ ██ █████       ██████  ██    ██   ████   ",
    " ██    ██ ██   ██ ██  ██  ██ ██          ██   ██ ██    ██    ██    ",
    "  ██████  ██   ██ ██      ██ ███████     ██████   ██████     ██    "
]