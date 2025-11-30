import os
import sys
import time
import subprocess
import glob
import platform
import shutil
from tools import config
from tools.ui import UI

class Builder:
    def __init__(self, args):
        self.args = args
        self.ui = UI(skip_intro=args.fast)
        self.system = "LINUX"
        self.emulator = config.EMU_PATHS["LINUX"]
        self._detect_os()

        # Paths logic
        if self.args.debug:
            self.current_obj_dir = config.OBJ_DIR_DBG
            self.rom_path = os.path.join(config.DEBUG_OUT, config.ROM_NAME)
        else:
            self.current_obj_dir = config.OBJ_DIR_REL
            self.rom_path = config.ROM_NAME

    def _detect_os(self):
        uname = platform.uname().release
        if "microsoft" in uname.lower():
            self.system = "WSL"
            self.emulator = config.EMU_PATHS["WSL"]
        elif platform.system() == "Windows":
             self.system = "WIN" 
             self.emulator = config.EMU_PATHS["WIN"]

    def _ensure_dirs(self):
        if not os.path.exists(self.current_obj_dir):
            os.makedirs(self.current_obj_dir)
        if self.args.debug and not os.path.exists(config.DEBUG_OUT):
            os.makedirs(config.DEBUG_OUT)

    def _run_cmd(self, cmd):
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            return True, ""
        except subprocess.CalledProcessError as e:
            return False, e.output.decode()

    def build_project(self):
        self._ensure_dirs()
        c = config.Colors
        
        # Clear screen logic
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[?25l") # Hide cursor
        
        if not self.args.fast: self.ui.animate_intro()
        else: self.ui.render()

        sources = glob.glob(f"{config.SRC_DIR}/*.asm") + glob.glob("*.asm")
        if not sources:
            print("\033[?25h")
            print(f"\n{c.ERR}❌ No .asm files found.{c.RESET}")
            sys.exit(1)

        objects = []
        files_compiled = 0
        total_steps = len(sources) + 2 
        current_step = 0

        # 1. COMPILATION
        debug_flag = "-E -DDEBUG" if self.args.debug else ""
        
        for src in sources:
            filename = os.path.basename(src)
            obj_path = os.path.join(self.current_obj_dir, filename.replace(".asm", ".o"))
            objects.append(obj_path)

            # Check timestamp
            needs_compile = self.args.force or not os.path.exists(obj_path) or \
                            os.path.getmtime(src) > os.path.getmtime(obj_path)

            if needs_compile:
                self.ui.info(f"Compiling {filename}...")
                self.ui.set_progress(current_step, total_steps)
                
                cmd = f"{config.ASM} {debug_flag} -I{config.INC_DIR}/ -o {obj_path} {src}"
                success, err = self._run_cmd(cmd)
                
                if not success:
                    print("\033[?25h")
                    print(f"\n{c.ERR}❌ ERROR in {filename}:{c.RESET}\n{err}")
                    sys.exit(1)
                
                files_compiled += 1
                if not self.args.fast: time.sleep(0.02)
            
            current_step += 1

        # 2. LINKING (Smart)
        needs_link = files_compiled > 0 or not os.path.exists(self.rom_path) or self.args.force

        if needs_link:
            self.ui.info("Linking objects...")
            self.ui.set_progress(current_step, total_steps)
            
            map_flags = ""
            if self.args.debug:
                base = self.rom_path.replace('.gb', '')
                map_flags = f"-n {base}.sym -m {base}.map"

            cmd = f"{config.LINK} {map_flags} -o {self.rom_path} {' '.join(objects)}"
            success, err = self._run_cmd(cmd)
            if not success:
                print("\033[?25h")
                print(f"\n{c.ERR}❌ LINKER ERROR:{c.RESET}\n{err}")
                sys.exit(1)
            current_step += 1

            # 3. FIXING
            self.ui.info("Fixing Header...")
            self.ui.set_progress(total_steps, total_steps)
            self._run_cmd(f"{config.FIX} -v -p 0 {self.rom_path}")
            self.ui.info(f"SUCCESS! Built {self.rom_path}")
        else:
            self.ui.info(f"Up to date. No changes.")
            self.ui.set_progress(1.0, 1.0)
        
        print("\033[?25h") # Show cursor
        print("\n") 

    def run_emulator(self):
        c = config.Colors
        print(f"{c.DARK}➤ Launching Emulator ({self.system})...{c.RESET}")
        print(f"{c.DARK}  ROM: {self.rom_path}{c.RESET}")
        subprocess.Popen(f"{self.emulator} {self.rom_path} > /dev/null 2>&1", shell=True)

    def clean(self):
        if os.path.exists("obj"): shutil.rmtree("obj")
        if os.path.exists(config.DEBUG_OUT): shutil.rmtree(config.DEBUG_OUT)
        print(f"{config.Colors.GREEN}✔ Objects cleaned.{config.Colors.RESET}")

    def fclean(self):
        self.clean()
        if os.path.exists(config.ROM_NAME): 
            os.remove(config.ROM_NAME)
            print(f"{config.Colors.GREEN}✔ Removed Release ROM{config.Colors.RESET}")