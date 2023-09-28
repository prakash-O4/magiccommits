import http.client
import json
import socket
from http.client import HTTPResponse

from magiccommits.src.exception.error import NetworkError
from magiccommits.src.utils.prompt import generate_prompt


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