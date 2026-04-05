# Assignment 4 - GitHub 

# author: Kyra Menai Hamilton

# import the modules we need for this assignment.

from pathlib import Path
import subprocess
import sys

REPO_DIR = Path(r"D:\Data_Analytics\Modules\web-services-and-applications\assignments") # To minimise errors (that I kept getting) I decided to use an absolute path to the repository directory, which is the directory where the file I want to modify is located. This way, I can be sure that the script will work regardless of where it's run from.
FILE_NAME = "assignment04-github.txt"
OLD_TEXT = "Round 2"
NEW_TEXT = "Kyra"

def run(cmd):
    subprocess.run(cmd, cwd=REPO_DIR, check=True) # Runs the code with the current working directory set to the repository directory, and checks for errors. If an error occurs, it will raise a CalledProcessError.

def main():
    file_path = REPO_DIR / FILE_NAME  # constructs the full path to the file I want to modify by combining the repository directory with the file name. https://stackoverflow.com/questions/41836988/git-push-via-gitpython; https://www.youtube.com/watch?v=4q_6t69k7f0; 

    if not file_path.exists():
        print(f"File not found: {file_path}") 
        sys.exit(1) # checks if the file exists. If it doesn't = prints an error message.

    original_text = file_path.read_text(encoding="utf-8")
    updated_text = original_text.replace(OLD_TEXT, NEW_TEXT)    # Reads the content of the file, replaces all occurrences of the old text with the new text, and stores the updated content. If there are no occurrences of the old text, the updated text will be the same as the original text.

    if updated_text == original_text:
        print("No replacements were needed.") # If file has already been modified, message will print in terminal. 
        return

    file_path.write_text(updated_text, encoding="utf-8") # https://textbooks.cs.ksu.edu/cc410/z-examples/01-hello-real-world/04-python/03-git-commit-push/index.html; https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository

    run(["git", "add", FILE_NAME])
    run(["git", "commit", "-m", f'Replace "{OLD_TEXT}" with "{NEW_TEXT}"'])
    run(["git", "push", "origin", "main"])

if __name__ == "__main__":
    main()
    
# END