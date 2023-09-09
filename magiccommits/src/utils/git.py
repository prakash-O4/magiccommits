import subprocess
from magiccommits.src.exception.error import error

def assert_git_repo():
    try:
        # Run the 'git rev-parse --show-toplevel' command using subprocess
        result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # If the command is successful, return the top-level directory path
        return result.stdout.strip()

    except subprocess.CalledProcessError:
        # If the command failed, raise a KnownError exception
        raise error('The current directory must be a Git repository!')


def get_staged_diff(exclude_files=None):
    diff_cached = ['diff', '--cached', '--diff-algorithm=minimal']
    
    # Run the 'git diff --cached --name-only' command to get staged files
    result_files = subprocess.run(['git', *diff_cached, '--name-only', *exclude_files], stdout=subprocess.PIPE, text=True, check=True)
    files = result_files.stdout.strip().split('\n')

    if not files:
        return None

    # Run the 'git diff --cached' command to get the staged diff
    result_diff = subprocess.run(['git', *diff_cached, *exclude_files], stdout=subprocess.PIPE, text=True, check=True)
    diff = result_diff.stdout

    return {
        'files': files,
        'diff': diff,
    }