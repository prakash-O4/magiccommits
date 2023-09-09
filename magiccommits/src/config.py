import os
import re
import configparser
import time
import click
from typing import Dict, Callable, List, Union, Tuple

from magiccommits.src.exception.error_handler import handleError
from magiccommits.src.exception.error import error

CONFIG_SECTION = "CONFIG"

TiktokenModel = str
TiktokenModelList = List[TiktokenModel]

# Mocking the 'fileExists' and 'error' functions
def fileExists(path: str) -> bool:
    return os.path.exists(path)


# Mocking 'configParsers' functions
def parse_OPENAI_KEY(key: str) -> str:
    if not key:
        error('Please set your OpenAI API key via `aicommits config set OPENAI_KEY=<your token>`')
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
        return 1
    if not re.match(r'^\d+$', count):
        error('Must be an integer')
    parsed = int(count)
    if parsed <= 0 or parsed > 5:
        error('Must be between 1 and 5')
    return parsed

def parse_type(commit_type: str) -> str:
    if not commit_type:
        return ''
    if commit_type not in ['', 'conventional']:
        error('Invalid commit type')
    return commit_type

def parse_proxy(url: str) -> Union[str, None]:
    if not url or len(url) == 0:
        return None
    if not re.match(r'^https?:\/\/', url):
        error('Must be a valid URL')
    return url

def parse_model(model: str) -> TiktokenModel:
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

# Mapping parsers to corresponding functions
config_parsers: Dict[str, Callable[[str], Union[str, int]]] = {
    'OPENAI_KEY': parse_OPENAI_KEY,
    'locale': parse_locale,
    'generate': parse_generate,
    'type': parse_type,
    'proxy': parse_proxy,
    'model': parse_model,
    'timeout': parse_timeout,
    'max-length': parse_max_length
}

# Mocking 'configPath'
config_path = os.path.join(os.path.expanduser("~"), '.mc')

# Mocking 'readConfigFile' function
def read_config_file() -> Dict[str, str]:
    config_exists = fileExists(config_path)
    config_value = {}
    if not config_exists:
        return config_value
    config_parser = configparser.ConfigParser()
    config_parser.optionxform = str
    config_parser.read(config_path)

    for section in config_parser.sections():
        config_value = dict(config_parser[section])
    return config_value

# Mocking 'getConfig' function
@handleError
def get_config(cli_config: Tuple = None) -> Dict[str, Union[str, int]]:
    loading()
    config = read_config_file()
    parsed_config = {}

    for key in config_parsers.keys():
        parser = config_parsers[key]
        value = None
        if cli_config:
            if key in cli_config:
                value = config.get(key)
                parsed_config[key] = parser(value)
    
    for c_config in cli_config:
        if c_config not in parsed_config:
            click.echo(click.style(f'{c_config.capitalize()} not found.', fg='red'))
    return parsed_config
    

# Mocking 'setConfigs' function
@handleError
def set_configs(key_values: List[Tuple[str, str]]):
    config = read_config_file()
    
    for key, value in key_values:
        if key not in config_parsers:
            error(f'Invalid config property: {key}')
        parsed = config_parsers[key](value)
        config[key] = parsed
    with open(config_path, 'w') as config_file:
        config_parser = configparser.ConfigParser()
        config_parser.add_section(CONFIG_SECTION)
        config_parser.optionxform = str
        for section, values in config.items():
            config_parser.set(section=CONFIG_SECTION, option=section,value=values)
        config_parser.write(config_file)


def loading():
    click.echo(click.style("Loading...",dim=True), nl=False)
    
    animation = "|/-\\"
    
    for _ in range(10):
        for char in animation:
            click.echo(char, nl=False)
            time.sleep(0.1)
            click.echo("\b", nl=False)  # Move the cursor back
    
    click.echo(" Done!")
