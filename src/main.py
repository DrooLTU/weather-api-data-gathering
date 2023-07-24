import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from fetch import fetch_coroutine

if __name__ == "__main__":
    fetch_coroutine.main()