from datetime import datetime
import pathlib
from typing import Optional

import typer

from date_organizer_util.core import m_logger

from typing_extensions import Annotated

from date_organizer_util.core.organizer import organize_files

from enum import Enum


class MoveCopy(str, Enum):
    mv = "move"
    cp = "copy"


app = typer.Typer()


def get_cwd() -> str:
    return str(pathlib.Path().cwd().absolute())


@app.command()
def main(
    source: Annotated[Optional[pathlib.Path], typer.Option()] = None,
    destination: Annotated[Optional[pathlib.Path], typer.Option()] = None,
    strat: Annotated[MoveCopy, typer.Option()] = MoveCopy.mv,
):
    if not source:
        source = typer.prompt("Enter the directory to organize files", default=get_cwd(), type=pathlib.Path)

    if not source.exists() or not source.is_dir():
        typer.pause(
            "The given source does not exist or is not a valid folder, please check your input...Press any key to exit."
        )
        raise typer.Abort()

    if not destination:
        destination = typer.prompt(
            "Enter the destination folder. We will use source directory by default...",
            default=source,
            type=pathlib.Path,
        )

    if not destination.exists() or not destination.is_dir():
        create_dest = typer.confirm("The given destination does not exist. Do you want create?", abort=True)
        if create_dest:
            destination.mkdir(parents=True)
        else:
            raise typer.Abort()

    proceed = typer.confirm(f"You have selected to {strat.value}. Do you want to proceed?", abort=True)
    if not proceed:
        raise typer.Abort()

    m_logger.run_log.info("Starting the file organization process at %s", datetime.now())
    organize_files(source, destination, strat.name)
    m_logger.run_log.info("Ending the file organization process at %s", datetime.now())
    typer.confirm("Do you want to exit?", abort=True)
    raise typer.Exit(0)
