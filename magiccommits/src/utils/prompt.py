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
    return f"The output response must be in format:\n{commit_type_formats[commit_type]}"

emoji_types: Dict[EmojiType, str] = {
    'conventional': """Choose an emoji from the given json which best fits the given diff type:
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
    'conventional': """Choose a type from the type-to-description JSON below that best describes the git diff:
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
        'Generate a concise git commit message written in present tense for the following code diff with the given specifications below:',
        f"Message language: {locale}",
        f"Commit message must be a maximum of {max_length} characters.",
        "Exclude anything unnecessary such as translation. Your entire response will be passed directly into git commit.",
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
