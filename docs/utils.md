# `Utils.py` 

Provides global constants, utility functions, and shared logic for PAT data processing. 

Also contains nonessential [`PatInfo`](#patinfo-class) class.

---

### Constants

* `PROJECT_ROOT`  --  dynamically resolves the path to the root of the project using `os.path.abspath(__file__)`, this is for consistent access to shared resources such as `data/`
* `BLOCKTYPES`  --  full list of experimental block condition labels, covering both coin and speed manipulations across neutral, post-manipulation, and post-block phases, along with the `"End of game questions"` block.
* `COINTYPES` --  used to reference coin counts per actor (`"player coins"`, `"e1 coins"`, `"e2 coins"`, `"e3 coins"`)
* `SHORT_BLOCKTYPES`  --  shorthand labels for the conditions (`"coin positive"`, `"coin negative"`, `"speed positive"`, `"speed negative"`)
* `COINBLOCKS`  --  `BLOCKTYPES` that contain only coin-based manipulations (both positive and negative).  
* `NEUTRALKEYS`  --  neutral `BLOCKTYPES` 
* `STATSTYPES`  -- names of GMM-derived metrics used to summarize gameplay behavior (`gmm average`, `gmm std`, `gmm area under the curve`, along with average and std values for each third of the session)
* `QUESTIONTYPES`  --  list of in-game and post-game questionnaire items (emotional state questions (e.g., `"Confident?"`, `"Frustrated?"`), gameplay assessments, and fairness/enjoyment ratings)

Below constants are further described in [compile_questionnaires.md](compile_questionnaires.md):

* `DEMOGRAPHIC_COLS` --  demographic variables (e.g., age, gender, race, education).
* `SWBS_COLS` – Social Well-Being Scale (**has subscales**)  
* `RIC_COLS` – Race in Context (**has subscales**)  
* `EDS_COLS` – Everyday Discrimination Scale  
* `CSE_COLS` – Collective Self-Esteem Scale (**has subscales**)  
* `SWLS_COLS` – Satisfaction With Life Scale  
* `MSPSS_COLS` – Multidimensional Scale of Perceived Social Support (**has subscales**)
* `CHRONIC_STRAINS_COLS` – Chronic Strains Scale

---

### `load_data(compiled_csv, questionaire_path, pat_data_path)`

`compiled_csv` is the file containing coin data for all participants, `questionnaire_path` is the file containing the questionnaire data, `pat_data_path` is the directory in which the participants' game data is stored. 

This method loads and prepares questionnaire and game data, extracts and stores the question description, logs missing values, and iterates over each participant to create a list of `PatInfo` objects, each containing that participant’s full game and questionnaire data. 

Returns list of `PatInfo` instances, missing values per column, raw questionnaire dataframe, coin data, and original question text. 

---

### `configure_logging(logging_level, filename)`

`logging_level` refers to the level (i.e. `"DEBUG"`, `"INFO"`, `"WARNING"`) and `filename` is the name of the file to which the logs will be appended to. 

The method converts the string log level to its corresponding numeric value, validates the log level and raises a `ValueError` if invalid, configures a logger that writes to `filename` parameter and the console (via standard error stream), uses a timestamped log format, and appends log entries (rather than overwriting existing logs). The logs are saved in `/logs/`. 

---

### `replace_with_parentheses_value(s)`

Extracts the first substring enclosed in parentheses from `s` and replaces the entire `(value)` with `value`. 

Returns a tuple containing the modified string and the extracted value. 

If no parentheses are found, returns the original string and `None` as a tuple

---

### `dict_append_or_create_list(dict, key, value)`

Appends a value to a list in a dictionary or creates a new list if the key doesn't exist.

---

## `PatInfo` Class

Contains participant's game + questionnaire data. This class is not essential. 

---

### `__init__(self, pat_id, questionaire_data, pat_coin_data, pat_game_root)`

Initializes a `PatInfo` object for a participant using their `pat_id` and associated questionnaire and coin data. 

`pat_game_data` is the path to the root directory containing individual participant folders named by ID (`PAT001`, `PAT002`, `PAT003`, etc.), each of which contain subfolders labeled with timestamps inside which are the actual game data in `data.json` files.

---

### `extract_number(s)`

Extracts the numeric aspect of a PAT id (e.g. `"PAT_001"`  -->  `1`).  

Returns the extracted int if found, otherwise returns `None`.

---

### `get_pat_data()`

Locates and loads participant game data based on the provided `self.pat_id` attribute set in `__init__`

This method filters the questionnaire and coin data for that participant and loads their raw game data from disk using `PatDataStructure`.  

If no data is found, sets `self.hasPAT = False`.

---

### `process_struct_data()`

If `self.pat_data_struct`, this method appends computed GMM features to the participant's coin-level dataframe.  

For each level with coin data, this method copies the original row and inserts gameplay stats into the main `self.pat_data` dataframe.

---

### `make_step(step_intervals, level_ticks)`

Creates a cumulative step function which transitions from 0 to 1 at each coin pick up tick. 

Used to transform coin pick up events into a step-based representation for scoring.  

Returns a NumPy array representing the step function.

---

### `compute_real_score(level)`

Uses step function for score calculation and extracts the ticks at which a coin was picked up and all ticks for the passed in level. Creates a cumulative step function using `self.make_step()` to mark coin pick ups, and incorporates it to the score.

Returns a tuple containing the final score as an array, the level tick timestamps, and the coin pick up ticks. 

---

### `compute_gmm_features()`

Computes GMM-derived metrics for game levels in a participant's session.  

For each level, this method extracts level summary stats like weighted averages, standard deviations, and area under the curve.  

Returns a list of tuples containing stats per level.

---

### `weighted_avg_and_std(values, weights)`

Calculates the weighted average and standard deviation of passed in NumPy array `values` using corresponding passed in `weights`.  

Returns a tuple `(average, std_dev)`.

---

### `compute_gmm_stats(score, levelTicks)`

Calculates metrics from passed in `score`:
* Weighted average and standard deviation
* Averages and standard deviations of each third of the session
* Area under the curve

Returns a tuple of:

* `weighted_average`
* `first_third_avg`
* `second_third_avg`
* `third_third_avg`
* `weighted_std`
* `first_third_std`
* `second_third_std`
* `third_third_std`
* `area`

---

### `get_order()`

Extracts the ordered list of game block types from the `Question Type` column in the raw PAT dataframe.  

Removes parentheses from condition labels from every third value in the `Question Type` column and stores the result in `self.order`.

---

### `aggregate_question_responses()`

Aggregates questionnaire and coin data by condition block type.  

Fills `self.pat_dict_data` nested dictionary with values for each combination of `BLOCKTYPES` × (`QUESTIONTYPES` + `STATSTYPES`).  

Used to structure raw data for analysis and wrangling.

---

### `get_neutrals()`

Extracts and stores blocks labeled with “(neutral)” from `self.pat_dict_data` into `self.neutrals`

---
