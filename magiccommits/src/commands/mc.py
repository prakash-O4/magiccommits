import click

#local import
from magiccommits.src.utils.config.config_helper import  get_config
from magiccommits.src.utils.custom.loading import Loading
from magiccommits.src.utils.git import (
    assert_git_repo,
    get_detected_message,
    get_staged_diff,
    stage_change,
)
from magiccommits.src.utils.style import multiple_answers
from magiccommits.src.utils.open_ai_commit import generate_commit_message

@click.option('-t','--ticket',help='Set the ticket number')
@click.option('-a','--add',is_flag=True, flag_value=True,help='Perform git add . operation')
def mc(ctx,ticket,add,update):
    if(ctx.invoked_subcommand is None):
        loading = Loading('⌛ Generating Commits.. ')
        try:
            # check if git is initialized or not
            assert_git_repo()
            # get the git diff of the current project
            if(add):
                stage_change(True)
            elif(update):
                stage_change(False)
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
            raise e
    else:
        pass