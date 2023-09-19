import subprocess
import time
from magiccommits.src.exception.error import error

def assert_git_repo():
    try:
        # Run the 'git rev-parse --show-toplevel' command using subprocess
        result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # If the command is successful, return the top-level directory path
        return result.stdout.strip()

    except subprocess.CalledProcessError:
        # If the command failed, raise a KnownError exception
        raise error('The current directory must be a git repository!')


def get_staged_diff():
    diff_cached = ['diff', '--cached', '--diff-algorithm=minimal', '--ignore-space-change']
    
    # Run the 'git diff --cached --name-only' command to get staged files
    result_files = subprocess.run(['git', *diff_cached, '--name-only'], stdout=subprocess.PIPE, text=True, check=True)
    files = result_files.stdout.strip().split('\n')

    if not files:
        return None

    # Run the 'git diff --cached' command to get the staged diff
    result_diff = subprocess.run(['git', *diff_cached], stdout=subprocess.PIPE, text=True, check=True)
    diff = result_diff.stdout
    return {
        'files': files,
        'diff': diff,
    }

def get_detected_message(files):
    if len(files) == 1:
        return f"Detected {len(files):,} staged file"
    else:
        return f"Detected {len(files):,} staged files"
    

def add_commit_message(message) -> bool:
    if message is not None:
        try:
            subprocess.run(['git','commit','-m',message])
            return True
        except Exception:
            return False
    else:
        return False
def is_repo_dirty():
    try:
        # Run the "git status" command
        output = subprocess.check_output(['git', 'status', '--porcelain']).decode('utf-8').strip()

        # Check if the output contains any lines indicating changes
        return bool(output)
    except subprocess.CalledProcessError:
        # Handle any errors if the 'git status' command fails
        print("Error running 'git status'")
        return False