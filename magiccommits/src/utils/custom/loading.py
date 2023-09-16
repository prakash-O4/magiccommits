import time
import click
import threading

class Loading:
    def __init__(self) -> None:
        self.isLoading = False
        self.loading_thread = None

    def start(self):
        if not self.isLoading:
            self.isLoading = True
            self.loading_thread = threading.Thread(target=self._animate_loading)
            self.loading_thread.start()

    def stop(self):
        if self.isLoading:
            self.isLoading = False
            if self.loading_thread:
                self.loading_thread.join()
            click.echo(" Done!")

    def _animate_loading(self):
        click.echo(click.style("Loading... ", dim=True), nl=False)
        animation = "|/-\\"
        i = 0
        while self.isLoading:
            click.echo(animation[i % len(animation)], nl=False)
            time.sleep(0.1)
            click.echo("\b", nl=False)
            i += 1