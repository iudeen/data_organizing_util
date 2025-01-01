from datetime import datetime
import pathlib

import typer

import core.m_logger

from typing_extensions import Annotated

from core.organizer import organize_files

cwd = str(pathlib.Path().cwd().absolute())

app = typer.Typer()


@app.command()
def main(
    source: Annotated[
        pathlib.Path,
        typer.Option(prompt="Enter the directory to organize files"),
    ] = cwd,
    destination: Annotated[
        pathlib.Path,
        typer.Option(
            prompt="Enter the destination folder. We will use source directory by default..."
        ),
    ] = cwd,
    mv_cp: Annotated[
        str,
        typer.Option(prompt="Enter 'mv' to move files or 'cp' to copy files",),
    ] = "mv",
):
    if not source.exists() or not source.is_dir():
        typer.pause("The given source does not exist or is not a valid folder, please check your input...Press any key to exit.")
        typer.Abort()
    if not destination.exists() or not destination.is_dir():
        create_dest = typer.confirm("The given destination does not exist. Do you want create?", abort=True)
        if create_dest:
            destination.mkdir(parents=True)
        else:
            typer.Abort()
    core.m_logger.run_log.info("Starting the file organization process at %s", datetime.now())
    organize_files(source, destination, mv_cp)
    core.m_logger.run_log.info("Ending the file organization process at %s", datetime.now())
    typer.confirm("Do you want to exit?", abort=True)

