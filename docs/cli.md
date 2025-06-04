# cli.py

Provides a command-line interface.

---

### `main()`

Main entry point for the CLI. Parses command-line arguments and conditionally runs the requested stages.

**Arguments:**

- `--json`, `-j`   &nbsp;&nbsp;--- Enable JSON Parsing
- `--dry_run`, `-z`   &nbsp;&nbsp;--- Enable dry run mode
- `--compile`, `-c`   &nbsp;&nbsp;--- Enable compiling json data into a single csv
- `--wrangle`, `-w`   &nbsp;&nbsp;--- Enable wrangling previous stages. Must be run with previous stages or data must already exist.
- `--questionaire`, -q`   &nbsp;&nbsp;--- Enable questionaire data processing
- `--all`, `-a`   &nbsp;&nbsp;--- Enable all steps
- `--debug`, `-d`   &nbsp;&nbsp;--- Enable debug mode

---

### Example Usage

`python -m pat_data_processing /path/to/data --all`
