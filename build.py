#!/usr/bin/env python3
import sys
import argparse
from tools.builder import Builder
from tools.config import Colors

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument("--fast", action="store_true", help="Skip animation")
    parser.add_argument("--force", action="store_true", help="Force rebuild")
    parser.add_argument("--debug", action="store_true", help="Debug mode")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("build")
    subparsers.add_parser("run")
    subparsers.add_parser("debug")
    subparsers.add_parser("clean")
    subparsers.add_parser("fclean")

    args = parser.parse_args()
    if args.command is None: args.command = "build"

    try:
        builder = Builder(args)

        if args.command == "clean":
            builder.clean()
        elif args.command == "fclean":
            builder.fclean()
        elif args.command == "run":
            builder.build_project()
            builder.run_emulator()
        elif args.command == "debug":
            args.debug = True 
            builder = Builder(args) 
            builder.build_project()
            builder.run_emulator()
        elif args.command == "build":
            builder.build_project()

    except KeyboardInterrupt:
        print("\033[?25h") # Show cursor
        print(f"\n{Colors.WARN}⚠ Cancelled.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print("\033[?25h")
        print(f"\n{Colors.ERR}❌ ERROR:{Colors.RESET} {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
