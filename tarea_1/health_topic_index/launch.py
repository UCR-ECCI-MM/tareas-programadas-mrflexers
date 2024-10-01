import subprocess
import os
import sys


def main():
    # Determine the path to your Streamlit app file (e.g., main.py)
    app_path = os.path.join(os.path.dirname(__file__), "app.py")

    # Construct the command to run Streamlit
    command = [sys.executable, "-m", "streamlit", "run", app_path] + sys.argv[1:]

    # Launch Streamlit using subprocess
    subprocess.run(command)


if __name__ == "__main__":
    main()
