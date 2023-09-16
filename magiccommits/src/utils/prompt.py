from typing import Dict

# Define a custom type for CommitType
CommitType = str
EmojiType =str

# Define commit type formats and messages in Python
commit_type_formats: Dict[CommitType, str] = {
    'conventional': '<type>(<optional scope>): <commit message> <emoji>',
}

# Function to specify commit format
def specify_commit_format(commit_type: CommitType) -> str:
    return f"Your response should include the selected emoji and the corresponding <type> for the git diff.\nThe output response must be in format:\n{commit_type_formats[commit_type]}"

emoji_types: Dict[EmojiType, str] = {
    'conventional': """Select an emoji from the given options that best represents the git diff type:

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
}
# Define commit types and descriptions
commit_types: Dict[CommitType, str] = {
    'conventional': """Now, choose a type from the type-to-description JSON below that best describes the git diff:

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
}

# Function to generate the prompt
def generate_prompt(locale: str, max_length: int, commit_type: CommitType, emoji_type: EmojiType) -> str:
    prompt_parts = [
        'Generate a concise Git commit message in the present tense based on the provided git diff. Your commit message should be comprehensive, descriptive, adhere to Git commit message best practices, and offer enough context for clear comprehension of the code changes.',
        f"Message language: {locale}",
        f"Maximum Commit Message Length: {max_length} characters",
        "Please exclude any superfluous information, such as translation details. Your entire response will be directly used as the git commit message.",
        emoji_types[emoji_type],
        commit_types[commit_type],
        specify_commit_format(commit_type)
    ]
    # Remove empty parts and join the lines
    prompt = '\n'.join(filter(None, prompt_parts))
    return prompt

#Example usage
locale = "English"
max_length = 80
commit_type = "conventional"
emoji_type = "conventional"
prompt = generate_prompt(locale, max_length, commit_type,emoji_type)
print(prompt)
