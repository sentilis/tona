from dotenv import load_dotenv
import os
import uvicorn
import click
from tona.core import Config

@click.command(name="web")
@click.pass_context
@click.option("--envfile", "-e", type=click.STRING, help="Envrionment file e.g -e .env")
def cli_web(ctx, envfile):
    if envfile and os.path.exists(envfile):
        load_dotenv(envfile)
    config = Config()
    uvicorn.run("server:app", host=config.server_host, port=config.server_port,
                log_level=config.log_level, reload=config.server_reload)

@click.group()
@click.pass_context
def cli(ctx):
    pass


cli.add_command(cli_web)

def main():
    cli()


if __name__ == "__main__":
    main()
