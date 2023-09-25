import click

#local import
from magiccommits.src.exception.error_handler import handleError
from magiccommits.src.utils.config.config_helper import set_configs, get_config
from magiccommits.src.utils.style import format_response
@click.command('config', short_help='Configuration for magiccommit')
@click.argument('mode',type=click.Choice(['get','set']))
@click.argument('key_value',nargs=-1)
@handleError
def config(mode,key_value):
    """Set your configuration value for the magic commit [Learn More]"""
    if(mode == 'get'):
        all_value=False
        if(len(key_value)==0):
            all_value=True
        config_value =  get_config(key_value,internal=all_value)
        format_response(config_value.all())
    elif(mode == 'set'): 
        value = []
        if len(key_value) == 0:
            click.secho("Enter value in mc config set key=value",fg='red')
        else:
            for kv in key_value:
                splitted_text = str(kv).strip().split("=")
                if(len(splitted_text) > 1):
                    value.append((splitted_text[0],splitted_text[1]))
                    set_configs(value)
                else:
                    click.secho("The key must be in the format key=value.",fg='red')
                    break