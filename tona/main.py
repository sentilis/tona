import os
import sys
import uvicorn
import click

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from tona.app import app
from tona.config import Config


@click.command(name="web")
@click.pass_context
@click.option("--config", "-c", type=click.STRING)
def cli_web(ctx, config):
    config = Config(config)
    app.state.config = config
    uvicorn.run("app:app", host=config.server_host, port=config.server_port,
                log_level=config.log_level, reload=config.server_reload)

@click.group()
@click.pass_context
def cli(ctx):
    pass


cli.add_command(cli_web)

def main():
    cli(obj={'argv': sys.argv})


if __name__ == "__main__":
    main()
