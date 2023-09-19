import click

#local import
from magiccommits.src.exception.error_handler import handleError
from magiccommits.src.utils.config.config import set_configs, get_config
from magiccommits.src.utils.custom.loading import Loading
from magiccommits.src.utils.git import assert_git_repo, get_detected_message, get_staged_diff
from magiccommits.src.utils.style import format_response, multiple_answers
from magiccommits.src.utils.test import generate_commit_message

@click.group(invoke_without_command=True)
# @click.option('--f', default=False, type=bool)
@click.option('-t','--ticket',help='Set the ticket number')
@click.version_option(version='1.0.0',help='Current version of magiccommit')
@click.pass_context
@handleError
def cli(ctx,ticket):
    """This is the main command group."""
    if(ctx.invoked_subcommand is None):
        loading = Loading('Generating Commits.. ')
        try:
            # check if git is initialized or not
            assert_git_repo()
            # get the git diff of the current project
            diff =  get_staged_diff()
            if(diff is None):
                click.secho('No stage files detected.',fg='red')
            else:
                click.secho(get_detected_message(diff['files']),fg='green')
                # get all the value from the config file i.e .mc file in the '~' directory
                config = get_config(internal=True)
                loading.start()
                # generate commit
                commit = generate_commit_message(config.OPENAI_KEY,config.model,config.locale,diff['diff'],config.generate,config.max_length,config.type,config.max_token,config.timeout)
                loading.stop()
                multiple_answers(commit_message=commit,ticket=ticket,copy_commit=config.copy_commit)
        except Exception as e: 
            loading.stop(is_forced=True)
            raise Exception()
    else:
        pass

@cli.command('config', short_help='Configuration for magiccommit')
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


