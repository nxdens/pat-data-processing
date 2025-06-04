# cli.py

Provides a command-line interface.

---

### `main()`

Main entry point for the CLI. Parses command-line arguments and conditionally runs the requested stages.

Arguments:
- `--json`          |  `-j`  |  Enable JSON Parsing
- `--dry_run`       |  `-z`  |  Enable dry run mode
- `--compile`       |  `-c`  |  Enable compiling json data into a single csv
- `--wrangle`       |  `-w`  |  Enable wrangling previous stages. Must be run with previous stages or data must already exist.
- `--questionaire`  |  `-q`  |  Enable questionaire data processing
- `--all`           |  `-a`  |  Enable all steps
- `--debug`         |  `-d`  |  Enable debug mode

---

### Example Usage

```bash
python -m pat_data_processing /path/to/data --all