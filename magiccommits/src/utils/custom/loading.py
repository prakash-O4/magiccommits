import time
import click
import threading

class Loading:
    def __init__(self,message) -> None:
        self.isLoading = False
        self.loading_thread = None
        self.message = 'Loading...' if message is None else message

    def start(self):
        if not self.isLoading:
            self.isLoading = True
            self.loading_thread = threading.Thread(target=self._animate_loading)
            self.loading_thread.start()

    def stop(self,is_forced: bool = False):
        if self.isLoading:
            self.isLoading = False
            if self.loading_thread:
                self.loading_thread.join()
            click.secho(" Done!",dim=True) if not is_forced else click.echo(' \n')

    def _animate_loading(self):
        click.echo(click.style(self.message, dim=True), nl=False)
        animation = "|/-\\"
        i = 0
        while self.isLoading:
            click.echo(animation[i % len(animation)], nl=False)
            time.sleep(0.1)
            click.echo("\b", nl=False)
            i += 1