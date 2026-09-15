import sys
from pathlib import Path
def main():
    if len(sys.argv) < 2:
        raise Exception("No config provided.")
    timer_path: Path = Path(sys.argv[1])
    

if __name__ == "__main__":
    main()