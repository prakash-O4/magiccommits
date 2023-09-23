from typing import Dict

# Define a custom type for CommitType
CommitType = str

# Define commit type formats and messages in Python
commit_type_formats: Dict[CommitType, str] = {
    'conventional': '<type>(<optional scope>): <commit message>',
    'conventional-emoji': '<type>(<optional scope>): <commit message> <emoji>',
    'message': '<commit message>',
    'message-emoji': '<commit message> <emoji>',
}

# Function to specify commit format
def specify_commit_format(commit_type: CommitType) -> str:
    return f"The output response must be in format:\n{commit_type_formats[commit_type]}"

emoji_types = """Select the emoji based on the generated commit <type> from the given dictionary
{
    "docs": "📚",
    "style": "💎",
    "refactor": "📦",
    "perf": "🚀",
    "test": "🚨",
    "build": "🛠",
    "ci": "⚙️",
    "chore": "♻️",
    "revert": "🗑",
    "feat": "✨",
    "fix": "🐛"
}"""

# Define commit types and descriptions
commit_types: Dict[CommitType, str] =  """Choose a type from the type-to-description JSON below that best describes the git diff:
{
    "docs": "Documentation only changes",
    "style": "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)",
    "refactor": "A code change that neither fixes a bug nor adds a feature",
    "perf": "A code change that improves performance",
    "test": "Adding missing tests or correcting existing tests",
    "build": "Changes that affect the build system or external dependencies",
    "ci": "Changes to our CI configuration files and scripts",
    "chore": "Other changes that don't modify src or test files",
    "revert": "Reverts a previous commit",
    "feat": "A new feature",
    "fix": "A bug fix"
}"""


# Function to generate the prompt
def generate_prompt(locale: str, max_length: int, commit_type: CommitType) -> str:
    prompt_parts = [
        'Generate a concise Git commit message in the present tense based on the provided git diff. Your commit message should not be detailed technical message, it should be simple summary of the provided git diff.',
        f"Message language of all commits should be in: {locale}",
        f"Each commit message should have maximum {max_length} characters in it.",
        "Please exclude any superfluous information, such as translation details. Your entire response will be directly used as the git commit message.",
        commit_types,
        emoji_types if commit_type != "message" else "",
        specify_commit_format(commit_type)
    ]
    # Remove empty parts and join the lines
    prompt = '\n'.join(filter(None, prompt_parts))
    return prompt

#Example usage
# locale = "English"
# max_length = 80
# commit_type = "conventional"
# emoji_type = "conventional"
# prompt = generate_prompt(locale, max_length, commit_type)
#print(specify_commit_format('message-emoji'))
