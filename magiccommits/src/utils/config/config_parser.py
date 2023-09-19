import re
from typing import Union
from magiccommits.src.exception.error import error

class ConfigParser:

    def parse_OPENAI_KEY(key: str) -> str:
        if not key:
            error('Please set your OpenAI API key via `mc config set OPENAI_KEY=<your token>`')
        if not key.startswith('sk-'):
            error('Must start with "sk-"')
        return key

    def parse_locale(locale: str) -> str:
        if not locale:
            return 'en'
        if not re.match(r'^[a-z-]+$', locale, re.IGNORECASE):
            error('Must be a valid locale (letters and dashes/underscores). You can consult the list of codes in: https://wikipedia.org/wiki/List_of_ISO_639-1_codes')
        return locale
    

    def parse_generate(count: str) -> int:
        if not count:
            return 4
        if not re.match(r'^\d+$', count):
            error('Must be an integer')
        parsed = int(count)
        if parsed <= 0 or parsed > 5:
            error('Must be between 1 and 5')
        return parsed

    def parse_type(commit_type: str) -> str:
        if not commit_type:
            return 'conventional'
        if commit_type not in ['', 'conventional','conventional-emoji','message','message-emoji']:
            error('"Invalid commit type. Options: conventional, conventional-emoji, message, message-emoji."')
        return commit_type

    def parse_proxy(url: str) -> Union[str, None]:
        if not url or len(url) == 0:
            return 'http'
        if not re.match(r'^https?:\/\/', url):
            error('Must be a valid URL')
        return url

    def parse_model(model: str) -> str:
        if not model or len(model) == 0:
            return 'gpt-3.5-turbo'
        return model

    def parse_timeout(timeout: str) -> int:
        if not timeout:
            return 10000
        if not re.match(r'^\d+$', timeout):
            error('Must be an integer')
        parsed = int(timeout)
        if parsed < 500:
            error('Must be greater than 500ms')
        return parsed

    def parse_max_length(max_length: str) -> int:
        if not max_length:
            return 50
        if not re.match(r'^\d+$', max_length):
            error('Must be an integer')
        parsed = int(max_length)
        if parsed < 20:
            error('Must be greater than 20 characters')
        return parsed
    
    def parse_max_token(max_token: str) -> int:
        if not max_token:
            return 200
        if not re.match(r'^\d+$', max_token):
            error('Must be an integer')
        parsed = int(max_token)
        if parsed < 10:
            error('Must be greater than 10 tokens')
        return parsed
    
    def parse_copy_commit(copy_commit: str) -> str:
        if not copy_commit:
            return 'True'  
        copy_commit = str(copy_commit).lower()  
        if copy_commit == 'true':
            return 'True'
        elif copy_commit == 'false':
            return 'False'
        else:
            raise error("Input must be 'True' or 'False'")
        