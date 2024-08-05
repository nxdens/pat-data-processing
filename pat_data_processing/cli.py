"""CLI interface for pat_data_processing project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""

import os
import glob
import pat_data_processing.Utils as Utils
import pat_data_processing.ComputeScore as ComputeScore
import argparse
import logging
from datetime import datetime

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m pat_data_processing` and `$ pat_data_processing `.

    This is the program's entry point.
    """
    parser = argparse.ArgumentParser(description="PAT Data Structure Configuration")
    parser.add_argument("path",action="store", help="Path to the PAT_ID folders")
    parser.add_argument(
        "--dry_run", action="store_true", help="Enable dry run mode"
    )
    cmd_args = parser.parse_args()
    current_directory = os.path.dirname(__file__)

    logs_path = cmd_args.path

    data_files = glob.glob(os.path.join(logs_path, "**", "data.json"), recursive=True)
    # Current date and time
    current_datetime = datetime.now()

    # Format the date and time
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M")

    Utils.Utils.configure_logging("INFO", f"{formatted_datetime}_Compute.log")
    logger = logging.getLogger("processing")
    
    logger.info("Starting to parse data files located at %s", logs_path)
    logger.info("Found %d data files", len(data_files))
    for file in data_files:
        logger.info("Starting to parse %s", file)
        json_parser = ComputeScore.PAT_JSON_parser(file_path=file, dry_run=cmd_args.dry_run)
        json_parser.run()
        logger.info("Done with %s", file)

if __name__ == "__main__":  # pragma: no cover
    main()