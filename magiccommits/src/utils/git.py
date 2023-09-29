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
        raise error('The current directory must be a git repository!')


def get_current_branch():
    try:
        branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()
        return branch_name
    except Exception:
        return None

def get_staged_diff():
    diff_cached = ['diff', '--cached', '--diff-algorithm=minimal', '--ignore-space-change']
    
    # Run the 'git diff --cached --name-only' command to get staged files
    result_files = subprocess.run(['git', *diff_cached, '--name-only'], stdout=subprocess.PIPE, text=True, check=True)
    files = result_files.stdout.strip().split('\n')
    if not files or files == ['']:
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
        return f"💡 Detected {len(files):,} staged file"
    else:
        return f"💡 Detected {len(files):,} staged files"

def stage_change(add:bool):
    try:
        if(add):
            subprocess.run(['git', 'add', '.'], check=True)
        else:
            subprocess.run(['git', 'add', '--update'], check=True)
    except subprocess.CalledProcessError:
        raise error("Error: Couldn't stage the changes. Please try to stage them manually using 'git add'.")
   

def add_commit_message(message) -> bool:
    if message is not None:
        try:
            subprocess.run(['git','commit','-m',message],check=True)
            return True
        except Exception:
            return False
    else:
        return False
    
def push_to_origin() -> bool:
    try:
        branch_name = get_current_branch()
        if(branch_name is not None):
            subprocess.run(['git','push','origin',branch_name],check=True)
            return True
        else: return False
    except Exception:
        return False

# Run 'git status --porcelain' to get the status of the repository
# result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True)

# Split the output into lines and filter staged files (status starts with "A", "M", "R", etc.)
# staged_files = [line for line in result.stdout.splitlines() if line.startswith(('A', 'M', 'R', 'C', 'D'))]

# Count the number of staged files
# number_of_staged_files = len(staged_files)

# return number_of_staged_files