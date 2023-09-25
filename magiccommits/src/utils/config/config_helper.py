import os
import configparser
from typing import Dict, List, Tuple

from magiccommits.src.exception.error import error
from magiccommits.src.utils.config.config_parser import ConfigParser
from magiccommits.src.utils.config.config_response import ConfigResponse


CONFIG_SECTION = "CONFIG"


# Mocking the 'fileExists' and 'error' functions
def fileExists(path: str) -> bool:
    return os.path.exists(path)


config_parsers = {
    'OPENAI_KEY': ConfigParser.parse_OPENAI_KEY,
    'locale': ConfigParser.parse_locale,
    'generate': ConfigParser.parse_generate,
    'type': ConfigParser.parse_type,
    'proxy': ConfigParser.parse_proxy,
    'model': ConfigParser.parse_model,
    'timeout': ConfigParser.parse_timeout,
    'max_length': ConfigParser.parse_max_length,
    'max_token': ConfigParser.parse_max_token,
    'copy_commit': ConfigParser.parse_copy_commit,
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

def get_config(cli_config: Tuple = None, internal: bool = False) -> ConfigResponse:
    config = read_config_file()
    parsed_config = {}

    if(internal):
        for key in config_parsers.keys():
            value = config.get(key)
            parsed_config[key] = True if value == 'True' else False if value == 'False' else config_parsers[key](value)
    else:
        for key in config_parsers.keys():
            parser = config_parsers[key]
            value = None
            if cli_config:
                if key in cli_config:
                    value = config.get(key)
                    parsed_config[key] = True if value == 'True' else False if value == 'False' else parser(value)
    
        for c_config in cli_config:
            if c_config not in parsed_config:
                raise error(f'{c_config.capitalize()} not found.')
    return ConfigResponse(parsed_config)
    

# Mocking 'setConfigs' function
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


