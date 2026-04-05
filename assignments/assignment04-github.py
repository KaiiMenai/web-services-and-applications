# Assignment 4

# author: Kyra Menai Hamilton

# import the modules we need for this assignment.

from pathlib import Path
import subprocess
import sys

REPO_DIR = Path(r"D:\Data_Analytics\Modules\web-services-and-applications\assignments") # To minimise errors (that I kept getting) I decided to use an absolute path to the repository directory, which is the directory where the file I want to modify is located. This way, I can be sure that the script will work regardless of where it's run from.
FILE_NAME = "assignment04-github.txt"
OLD_TEXT = "Andrew"
NEW_TEXT = "Kyra"

def run(cmd):
    subprocess.run(cmd, cwd=REPO_DIR, check=True) # runs the code with the current working directory set to the repository directory, and checks for errors. If an error occurs, it will raise a CalledProcessError.

def main():
    file_path = REPO_DIR / FILE_NAME  # constructs the full path to the file I want to modify by combining the repository directory with the file name.

    if not file_path.exists():
        print(f"File not found: {file_path}") 
        sys.exit(1) # checks if the file exists. If it doesn't = prints an error message.

    original_text = file_path.read_text(encoding="utf-8")
    updated_text = original_text.replace(OLD_TEXT, NEW_TEXT)    # Reads the content of the file, replaces all occurrences of the old text with the new text, and stores the updated content. If there are no occurrences of the old text, the updated text will be the same as the original text.

    if updated_text == original_text:
        print("No replacements were needed.")
        return

    file_path.write_text(updated_text, encoding="utf-8")

    run(["git", "add", FILE_NAME])
    run(["git", "commit", "-m", f'Replace "{OLD_TEXT}" with "{NEW_TEXT}"'])
    run(["git", "push", "origin", "main"])

if __name__ == "__main__":
    main()