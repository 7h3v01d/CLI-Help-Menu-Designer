import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="mycli",
        description="A sample CLI tool",
        formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(prog, width=80)
    )
    parser.add_argument("-v, --verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Your code here
    print(args)

if __name__ == "__main__":
    main()
