import pathlib
from datetime import datetime
import shutil
import typer
from core.m_logger import run_log, error_log
import json

month_map = {
    1: "01January",
    2: "02February",
    3: "03March",
    4: "04April",
    5: "05May",
    6: "06June",
    7: "07July",
    8: "08August",
    9: "09September",
    10: "10October",
    11: "11November",
    12: "12December",
}


def organize_files(cdir: pathlib.Path, destination: pathlib.Path, mv_cp: str, verbose: bool = False):
    files_dict = {}
    count = 0
    fail_count = 0

    for file in cdir.iterdir():
        try:
            if file.is_dir():
                continue
            # get the modified date of the file
            modified_date = file.stat().st_mtime
            # convert the modified date to a readable format
            modified_date = datetime.fromtimestamp(modified_date)
            # get the year and month of the modified date
            year = modified_date.year
            month = modified_date.month

            # create a folder name based on the year and month
            year_folder = destination / str(year)
            month_folder = year_folder / f"{month_map.get(month, 'unknown')}{year}"
            month_folder.mkdir(parents=True, exist_ok=True)

            if mv_cp == "mv":
                # move the file to the folder
                shutil.move(file, month_folder)
            else:
                # copy the file to the folder
                shutil.copy(file, month_folder)

            if verbose:
                typer.echo(f"{file} -> {month_folder}")
            # store the file in the dictionary
            if month_folder.name in files_dict:
                files_dict[month_folder.name].append(str(file))
            else:
                files_dict[month_folder.name] = [str(file)]

        except Exception as e:
            error_log.error("Failed to organize file: %s", file)
            error_log.error("Error: %s", e)
            fail_count += 1

        count += 1

    run_log.info("Files organized successfully. Total files: %s", count)
    if fail_count > 0:
        run_log.warning(
            "Total files failed to organize: %s Check error logs for details",
            fail_count,
        )
    typer.echo(f"Files organized successfully. Total files: {count}")

    with open(destination / "files.json", "w") as j_file:
        json.dump(files_dict, j_file, indent=4)
