# `Utils.py` 

Provides global constants, utility functions, and shared logic for the project.

---

### Constants

- `PROJECT_ROOT`: The root path of the project directory.
- `BLOCKTYPES`: List of full block type strings (e.g. `"coin: neutral -> positive (neutral)"`)
- `COINTYPES`: List of strings denoting each actors' coins.
- `SHORT_BLOCKTYPES`: Simplified block names.
- `QUESTIONTYPES`: Columns of Excel sheet.
- `NEUTRALKEYS`: Neutral `BLOCKTYPES`.
- `STATSTYPES`: Names of GMM features.
- `DEMOGRAPHIC_COLS`, `SWBS_COLS`, `RIC_COLS`, `EDS_COLS`, `CSE_COLS`, `SWLS_COLS`, `MSPSS_COLS`, `CHRONIC_STRAINS_COLS`: Column ranges parsed from `questionnaire_column_descriptions.csv`.

---

### `load_data(compiled_csv, questionaire_path, pat_data_path)`

Loads and prepares questionnaire and gameplay data.

Returns list of `PatInfo` instances, missing values per column, raw questionnaire dataframe, coin data, and original question text

---

### `configure_logging(logging_level, filename)`

Configures logging via passed in logging level string and name of log file to save in `/logs/`

---

### `replace_with_parentheses_value(s)`

Extracts and replaces a value within parentheses in a string.  

---

### `dict_append_or_create_list(dict, key, value)`

Appends a value to a list in a dictionary or creates a new list if the key doesn't exist.

---

## `PatInfo` Class

Contains participant's game + questionnaire data.

### `__init__(...)`
Initializes a `PatInfo` object with raw question/coin data.

---

### Methods

- `extract_number(s)`: Extracts PAT ID
- `get_pat_data()`: Loads participant data
- `process_struct_data()`: Appends GMM features into the dataframe
- `compute_gmm_features()`: Computes GMM-derived gameplay metrics.
- `make_step(step_intervals, level_ticks)`: Cumulative step function, transitions from 0 to 1 at each coin pick up tick.
- `compute_real_score(level)`: Uses step function to for score calculation.
- `compute_gmm_features()`: Iterates through and calculates leel stats.
- `weighted_avg_and_std(values, weights)`: Returns weighted average and std dev.
- `compute_gmm_stats(score, ticks)`: Computes stats for three thirds and area under curve.
- `get_order()`: Parses question type order from `Question Type` column.
- `aggregate_question_responses()`: Aggregates coin/question answers per block.
- `get_neutrals()`: Extracts all neutral block values.

---
