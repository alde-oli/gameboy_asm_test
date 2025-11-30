import sys
import time
import math
from tools import config

class UI:
    def __init__(self, skip_intro=False):
        self.logo_y = 3.0 if skip_intro else -len(config.LOGO)
        self.target_y = 3
        self.message = "Initializing..."
        self.progress = 0.0
        self.is_rainbow = skip_intro
        self.frame_counter = 0
        
    def _rgb(self, r, g, b): 
        return f"\033[38;2;{r};{g};{b}m"

    def _rainbow_color(self, offset):
        r = int(math.sin(offset) * 127 + 128)
        g = int(math.sin(offset + 2) * 127 + 128)
        b = int(math.sin(offset + 4) * 127 + 128)
        return self._rgb(r, g, b)

    def info(self, text):
        self.message = text
        self.render()

    def set_progress(self, current, total):
        self.progress = current / total if total > 0 else 0
        self.render()

    def render(self):
        sys.stdout.write("\033[H") 
        buffer = []
        c = config.Colors
        w = config.SCREEN_W
        
        buffer.append(f"  {c.FRAME}╔{'═' * w}╗{c.RESET}")
        
        for y in range(config.SCREEN_H):
            line_content = ""
            raw_len = 0 
            logo_row = y - int(self.logo_y)
            
            # 1. Logo Layer
            if 0 <= logo_row < len(config.LOGO):
                raw_line = config.LOGO[logo_row]
                pad_len = max(0, (w - len(raw_line)) // 2)
                padding_left = " " * pad_len
                colored_logo = ""
                for i, char in enumerate(raw_line):
                    if char != " ":
                        if self.is_rainbow: 
                            colored_logo += self._rainbow_color(i * 0.1 + self.frame_counter * 0.2) + char
                        else: 
                            colored_logo += c.DARK + char
                    else: 
                        colored_logo += " "
                line_content += padding_left + colored_logo
                raw_len += len(padding_left) + len(raw_line)
            
            # 2. Text Layers
            elif y == self.target_y + len(config.LOGO) + 2:
                text = config.PROJECT_NAME
                pad = max(0, (w - len(text)) // 2)
                line_content = " " * pad + f"{c.BOLD}{c.GREEN}{text}{c.RESET}"
                raw_len = pad + len(text)
            elif y == self.target_y + len(config.LOGO) + 4:
                text = self.message
                if len(text) > w - 4: text = text[:w-5] + "..."
                pad = max(0, (w - len(text)) // 2)
                line_content = " " * pad + f"{c.DARK}{text}{c.RESET}"
                raw_len = pad + len(text)
            elif y == self.target_y + len(config.LOGO) + 6:
                bar_width = 40
                filled = int(self.progress * bar_width)
                filled = min(filled, bar_width)
                bar_vis = f"[{'▓' * filled}{'░' * (bar_width - filled)}]"
                pad = max(0, (w - 42) // 2)
                line_content = " " * pad + f"{c.GREEN}{bar_vis}{c.RESET}"
                raw_len = pad + 42

            remaining = max(0, w - raw_len)
            line_content += " " * remaining
            buffer.append(f"  {c.FRAME}║{c.RESET}{line_content}{c.FRAME}║{c.RESET}")
            
        buffer.append(f"  {c.FRAME}╚{'═' * w}╝{c.RESET}")
        print("\n".join(buffer))
        self.frame_counter += 1

    def animate_intro(self):
        while self.logo_y < self.target_y:
            self.logo_y += 0.5 
            self.render()
            time.sleep(0.02)
        self.is_rainbow = True
        for _ in range(10): 
            self.render()
            time.sleep(0.01)