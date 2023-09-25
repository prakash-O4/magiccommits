import http.client
import json
import socket
from http.client import HTTPResponse

from magiccommits.src.exception.error import NetworkError
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

test_diff_pref = """
diff --git a/app/processing.py b/app/processing.py
index 7c8d39f..f2a1a67 100644
--- a/app/processing.py
+++ b/app/processing.py
@@ -1,8 +1,12 @@
 # Performance Improvement in Data Processing
 
+from functools import lru_cache
 import time
 
-def process_data(data):
+@lru_cache(maxsize=None)
+def cached_process_data(data):
     # Existing data processing code
-    result = complex_data_processing(data)
+    if data in processed_data_cache:
+        return processed_data_cache[data]
+    result = complex_data_processing(data)
     return result
 
+processed_data_cache = {}
 
 def complex_data_processing(data):
     # Existing complex processing logic
@@ -14,6 +18,9 @@ def complex_data_processing(data):
     return result
 
 def main():
+    # Prepopulate cache for frequently used data
+    for data in commonly_used_data:
+        cached_process_data(data)
     start_time = time.time()
     data = load_large_dataset()
     result = process_data(data)
@@ -21,6 +28,7 @@ def main():
     end_time = time.time()
     print("Processing time: {:.2f} seconds".format(end_time - start_time))
 
+commonly_used_data = [1, 2, 3, 4, 5]  # Add frequently used data here
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

test_prompt = """Generate a concise Git commit message in the present tense based on the provided git diff. 
Your commit message should not be detailed technical message, it should be simple summary of the provided git diff.
Please exclude any superfluous information, such as translation details. Your entire response will be directly used as the git commit message.

Message language: English
Maximum Commit Message Length: 80 characters

Choose a type from the type-to-description JSON below that best describes the git diff:

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
}

Choose a emoji from the emoji-to-description JSON below that best describes the git diff:

{
 "📚": "Documentation only changes",
    "💎": "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)",
    "📦": "A code change that neither fixes a bug nor adds a feature",
    "🚀": "A code change that improves performance",
    "🚨": "Adding missing tests or correcting existing tests",
    "🛠": "Changes that affect the build system or external dependencies",
    "⚙️": "Changes to our CI configuration files and scripts",
    "♻️": "Other changes that don't modify src or test files",
    "🗑": "Reverts a previous commit",
    "✨": "A new feature",
    "🐛": "A bug fix"
}
The output response must be in format:
<type>(<optional scope>): <commit message> <emoji>
"""

test_diff_doc = """
@@ -1,6 +1,8 @@
 # Utility Functions
 
 def calculate_average(numbers):

-    Calculate the average of a list of numbers.
+    Calculate the average of a list of numbers.
+
+    :param numbers: A list of numbers.
+    :type numbers: list of int or float
     :return: The average of the numbers.
     :rtype: float

@@ -8,7 +10,10 @@ def calculate_average(numbers):
     return sum(numbers) / len(numbers)
 
 
+def validate_email(email):
+    
+    Validate an email address.
 
-def validate_email(email):
+    :param email: The email address to validate.
+    :type email: str
     :return: True if the email is valid, False otherwise.
     :rtype: bool

"""
def https_post(hostname, path, headers, json_data, timeout, proxy=None):
    post_content = json.dumps(json_data)
    connection = http.client.HTTPSConnection(hostname, timeout=timeout)

    if proxy:
        connection.set_tunnel(proxy)

    headers["Content-Type"] = "application/json"
    headers["Content-Length"] = str(len(post_content))

    try:
        connection.request("POST", path, post_content, headers)
        response: HTTPResponse = connection.getresponse()
        response_data = response.read()
        connection.close()
    except Exception as e:
        if not has_internet_connection():
            raise NetworkError({"message": f"Are you connected to Internet?"})
        raise NetworkError({"message": f"Error making POST request: {str(e)}"})

    return {
        "response": response,
        "data": response_data.decode("utf-8")
    }


def has_internet_connection():
    try:
        # Attempt to connect to Google's DNS server (8.8.8.8) on port 53 (DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True  # If successful, there is internet connectivity
    except OSError:
        pass
    return False

def create_chat_completion(api_key, json_data, timeout, proxy=None):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    result = https_post(
        "api.openai.com",
        "/v1/chat/completions",
        headers,
        json_data,
        timeout,
        proxy
    )

    response = result["response"]
    data = result["data"]
    if not response.status or response.status < 200 or response.status > 299:
        error_message = {"error_type": f"OpenAI API Error: {response.status} - {response.reason}"}
        if data:
            error_message['message'] = json.loads(data)['error']['message']
        if response.status == 500:
            error_message += "\n\nCheck the API status: https://status.openai.com"
        raise NetworkError(error_message)

    return json.loads(data)


def sanitize_message(message):
    return message.strip().replace("\n", "").replace("\r", "").rstrip(".")


def generate_commit_message(api_key, model, locale, diff, completions, max_length, type,max_token ,timeout, proxy=None):
    try:
        system_message = generate_prompt(locale, max_length, type)  # Define generate_prompt function
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": diff},
        ]

        json_data = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "max_tokens": max_token,
            "stream": False,
            "n": completions,
        }

        completion = create_chat_completion(api_key, json_data, timeout, proxy)
        sanitized_messages = [sanitize_message(choice["message"]["content"]) for choice in completion["choices"] if
                              choice.get("message", {}).get("content")]
        return list(set(sanitized_messages))
    
    except Exception as e:
        raise e