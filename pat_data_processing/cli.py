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
from pat_data_processing.Utils import PROJECT_ROOT
import pat_data_processing.Compute_Score as Compute_Score
import pat_data_processing.Compile_Answers as Compile_Answers
from pat_data_processing.Wrangle_Data import DataWrangler
import pat_data_processing.Compile_Questionnaires as Compile_Questionnaires
import argparse
import logging
from datetime import datetime
from tqdm import tqdm


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m pat_data_processing` and `$ pat_data_processing `.

    This is the program's entry point.
    """
    # Current date and time
    current_datetime = datetime.now()

    # Format the date and time
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M")

    Utils.configure_logging("INFO", f"{formatted_datetime}_Compute.log")
    logger = logging.getLogger("processing")

    parser = argparse.ArgumentParser(description="PAT Data Structure Configuration")
    parser.add_argument(
        "path",
        action="store",
        help="Path to the data folder containing PAT folders and questionaire files",
    )
    parser.add_argument(
        "--dry_run", "-z", action="store_true", help="Enable dry run mode"
    )
    parser.add_argument("--json", "-j", action="store_true", help="Enable JSON Parsing")
    parser.add_argument(
        "--compile",
        "-c",
        action="store_true",
        help="Enable compiling json data into a single csv",
    )
    parser.add_argument(
        "--wrangle",
        "-w",
        action="store_true",
        help="Enable wrangling previous stages. Must be run with previous stages or data must already exist.",
    )
    parser.add_argument(
        "--questionaire",
        "-q",
        action="store_true",
        help="Enable questionaire data processing",
    )

    parser.add_argument("--all", "-a", action="store_true", help="Enable all steps")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")

    cmd_args = parser.parse_args()
    current_directory = os.path.dirname(__file__)

    # get args
    debug = cmd_args.debug
    data_path = cmd_args.path
    parse_json = cmd_args.json
    compile_data = cmd_args.compile
    wrangle_data = cmd_args.wrangle
    compile_questionaire = cmd_args.questionaire
    all_steps = cmd_args.all

    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    logger.info(f"Running with args: {cmd_args}")

    data_files = glob.glob(os.path.join(data_path, "**", "data.json"), recursive=True)
    logger.debug("Searching: %s", os.path.join(data_path, "**", "data.json"))
    logger.info("Found %d data files", len(data_files))
    if parse_json or all_steps:
        logger.info("Starting to parse data files located at %s", data_path)
        logger.info("Found %d data files", len(data_files))
        for file in (pbar := tqdm(data_files, desc="Parsing JSON files")):
            logger.info("Starting to parse %s", file)
            pbar.set_description(f"Processing {file}")
            json_parser = Compute_Score.PatJsonParser(
                file_path=file, dry_run=cmd_args.dry_run
            )
            json_parser.run()
            logger.info("Done with %s", file)

    # compile answers
    if compile_data or all_steps:
        logger.info("Starting to compile answers")
        logger
        compiled_data = Compile_Answers.main(
            data_path,
            output_path=os.path.join(data_path, "temp_PAT_variables.csv"),
            dry_run=cmd_args.dry_run,
        )
        logger.info("Done compiling answers")

    if compile_questionaire or all_steps:
        logger.info("Starting to compile questionaire data")
        Compile_Questionnaires.main(data_path)
        logger.info("Done compiling questionaire data")

    # wrangle data
    if wrangle_data or all_steps:
        logger.info("Starting to wrangle data")
        data_wrangler = DataWrangler(data_path=data_path, dry_run=cmd_args.dry_run)
        data_wrangler.run_wrangling()
        logger.info("Done wrangling data")

    # other stuff
    # DataList, null_counts, Questionaire_data, pat_coin_data, Question_descriptions = (
    #     Utils.load_data()
    # )

    if not (parse_json or compile_data or wrangle_data or all_steps):
        logger.info("No steps selected. Exiting...")
        return


if __name__ == "__main__":  # pragma: no cover
    main()
