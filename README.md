<!-- YoRHa archive -->
```
▸ YoRHa // ARCHIVE — GAMEBOY_ASM_TEST
```

A Game Boy assembly sandbox: a hello-world ROM plus a small Python build tool with a terminal UI around the RGBDS toolchain.

| UNIT DATA | |
|---|---|
| Type | Personal project |
| Stack | Game Boy assembly · RGBDS · Python |
| Status | □ ARCHIVED · experiment |

## ▸ Overview
`src/hello-world.asm` includes `inc/hardware.inc` (hardware register definitions). `build.py` assembles, links and fixes the ROM with `rgbasm`, `rgblink` and `rgbfix` and can launch it in an emulator (`sameboy` on Linux, bgb on Windows / WSL, paths in `tools/config.py`).

## ▸ Usage
```bash
python3 build.py            # build (default)
python3 build.py run        # build and launch the emulator
python3 build.py debug      # debug build and run
python3 build.py clean      # or fclean
```
Options: `--fast` (skip animation), `--force` (rebuild), `--debug`. Requires RGBDS on the PATH.

---
<sub>▸ Archived by UNIT ALDE-OLI · [profile](https://github.com/alde-oli)</sub>
