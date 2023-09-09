import http.client
import json
import ssl
from http.client import HTTPResponse
from typing import Dict, Any, Optional, List

from magiccommits.src.utils.prompt import generate_prompt


test_diff = """
diff --git a/app/main.py b/app/main.py
index e5f1a12..4c8a2f7 100644
--- a/app/main.py
+++ b/app/main.py
@@ -1,5 +1,9 @@
 # MyApp - Main Application
 
 import requests
+from my_new_feature import process_new_data
 
 def fetch_data(url):
     response = requests.get(url)
     data = response.json()
     return data
 
 def main():
     data = fetch_data("https://api.example.com/data")
+    processed_data = process_new_data(data)
+    if processed_data:
+        print("New feature result:", processed_data)
+
 if __name__ == "__main__":
     main()
"""
test_api_key = "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"
test_locale = "en"
test_completions = 5
test_max_length = 80
test_type = "conventional"
test_timeout = 600

test_prompt = """Generate a concise git commit message for the given code diff. Consider the following specifications:

1. The commit message should be written in the present tense and in English.
2. The commit message must not exceed 80 characters in length.
3. Exclude anything unnecessary such as translation. Your entire response will be passed directly into git commits.

Given JSON for emojis:
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
}

Given JSON for types and their descriptions:
{
    "docs": "Documentation only changes",
    "style": "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)",
    "refactor": "A code change that neither fixes a bug nor adds a feature",
    "perf": "A code change that improves performance",
    "test": "Adding missing tests or correcting existing tests",
    "build": "Changes that affect the build system or external dependencies",
    "ci": "Changes to CI configuration files and scripts",
    "chore": "Other changes that don't modify src or test files",
    "revert": "Reverts a previous commit",
    "feat": "A new feature",
    "fix": "A bug fix"
}
The output response must be in format:
<type>(<optional scope>): <commit message> <emoji>
"""

def https_post(
    hostname: str,
    path: str,
    headers: Dict[str, str],
    json_data: Any,
    timeout: int,
    proxy: Optional[str] = None
) -> Dict[str, Any]:
    post_content = json.dumps(json_data).encode('utf-8')
    
    conn = http.client.HTTPSConnection(hostname, context=ssl.SSLContext())
    if proxy:
        conn = http.client.HTTPSConnection(hostname, context=ssl.SSLContext())
    
    conn.request(
        'POST',
        path,
        body=post_content,
        headers={
            **headers,
            'Content-Type': 'application/json',
            'Content-Length': str(len(post_content))
        }
    )
    
    response: HTTPResponse = conn.getresponse()
    data = response.read().decode('utf-8')
    conn.close()
    
    return {
        'response': response,
        'data': data
    }

def create_chat_completion(
    api_key: str,
    json_data: Dict[str, Any],
    timeout: int,
    proxy: Optional[str] = None
) -> Dict[str, Any]:
    response_data = https_post(
        'api.openai.com',
        '/v1/chat/completions',
        {
            'Authorization': f'Bearer {api_key}'
        },
        json_data,
        timeout,
        proxy
    )

    response = response_data['response']
    data = response_data['data']
    
    if not response.status or response.status < 200 or response.status > 299:
        error_message = f'OpenAI API Error: {response.status} - {response.reason}'
        
        if data:
            error_message += f'\n\n{data}'
        
        if response.status == 500:
            error_message += '\n\nCheck the API status: https://status.openai.com'
        
        raise Exception(error_message)
    
    return json.loads(data)

def sanitize_message(message: str) -> str:
    return message.strip().replace('\n', '').replace('\r', '').replace(r'(\w)\.$', r'\1')

def deduplicate_messages(messages: List[str]) -> List[str]:
    return list(set(messages))

def generate_commit_message(
    api_key: str,
    model: str,  # Assuming TiktokenModel is a string
    locale: str,
    diff: str,
    completions: int,
    max_length: int,
    commit_type: str,  # Assuming CommitType is a string
    timeout: int
) -> List[str]:
    try:
        completion = create_chat_completion(
            api_key,
            {
                'model': model,
                'messages': [
                    {
                        'role': 'system',
                        'content': test_prompt
                    },
                    {
                        'role': 'user',
                        'content': diff
                    }
                ],
                'temperature': 0.7,
                'top_p': 1,
                'frequency_penalty': 0,
                'presence_penalty': 0,
                'max_tokens': 200,
                'stream': False,
                'n': completions
            },
            timeout,
            "https",
        )

        return deduplicate_messages(
            [sanitize_message(choice['message']['content']) for choice in completion['choices'] if choice['message']['content']]
        )
    except Exception as error:
        if isinstance(error, ConnectionError):
            raise Exception(f'Error connecting to {error.hostname}. Are you connected to the internet?')
        
        raise error


commit = generate_commit_message(test_api_key,"gpt-3.5-turbo",test_locale,test_diff,test_completions,test_max_length,test_type,test_timeout)
for c in commit:
    print(c)