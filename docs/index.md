# PAT - GPN Lab

Code for analyzing data from game that studies privilege, bias, and decisionmaking. 

---

## Contents

* [PAT Data Structure](pat_data_structure.md) 
    * Data structure in which PAT game data is stored
    * Parameters of initialization are file_path (str), dry_run (bool), and save_dir (str)
    * Information about the individual's game is stored on a level-by-level basis
    * Data is stored as Python lists which are then converted to numpy arrays for ease in storage and computation
    * Levels are grouped based on breakage in contiguity
    * Data is saved into `.npz` files
    * There are temporary variables within the game which can be reset to 0

* [CLI Interface](cli.md) 
    * Command-line usage and arguments for running the application
    * Commands for JSON parsing, enabling dry run mode, compiling the JSON into a single CSV, wrangling previous stages, enabling questionnaire data processing, enabling all steps, enabling debug mode

* [Compute Score](compute_score.md)
    * Parses through the raw game data (stored in JSON files) 
    * Stores information of each tick level by level
    * Generates metrics such as coin pick ups and key presses

* [Compile Answers](compile_answers.md)
    * Formats participant responses from questionnaire responses 
    * Uses randomization and structure information to determine block ordering
    * Outputs a CSV where each row contains `PAT_ID`, `Question Type`, `Block Type`, `Question`, and `Score`

* [Compile Questionnaires](compile_questionnaires.md) 
    * Calclates scores:
        * `EDS` — Everyday Discrimination Scale
        * `SWBS` — Social Well-Being Scale (with subscales)
        * `RiC` — Race in Context interactions
        * `CSE` — Collective Self-Esteem Scale (with subscales)
        * `SWLS` — Satisfaction With Life Scale
        * `MSPSS` — Multidimensional Scale of Perceived Social Support (with subscales)
        * `Chronic Strains` — cumulative life stressors
    * Outputs total and subscale scores (if `subscales=True`) per participant
    * Drops raw columns by default unless `drop_cols=False`

* [Wrangle Data](wrangle_data.md) 
    * Combines together datasets and calculates differences
    * Combines game responses, questionnaire scores, and coin performance data into one DataFrame
        * Calculates participant's changes across conditions for each block
        * Derives performance-based accuracy scores (e.g., whether participants correctly identified who collected the most coins)
        * Outputs three versions of the data if `dry_run=True`
            * `pat_compiled_sheet_<date>.csv` — raw merged dataset
            * `pat_compiled_sheet_diffed_<date>.csv` — includes calculated differences and ratios
            * `pat_diffes_with_accuracy_<date>.csv` — adds perception accuracy correctness flags

* [Utilities](utils.md) 
    * Contains constants and helper functions such as:
        * `BLOCKTYPES`  -  speed and coin, neutral --> positive, neutral --> negative, neutral / post-manipulation / post-block
        * `COINTYPES`  -  coin and speed, positive and negative
        * `COINBLOCKS`  -  BLOCKTYPES excluding post-block
        * `QUESTIONTYPES`  -  actors' coins and the questions the participant was asked
        * `NEUTRALKEYS`  -  the neutral BLOCKTYPES
        * `STATSTYPES`  -  Gaussian matrix metrics
        * `DEMOGRAPHIC_COLS`, `SWBS_COLS`, `RIC_COLS`, `EDS_COLS`, `CSE_COLS`, `SWLS_COLS`, `MSPSS_COLS`, `CHRONIC_STRAINS_COLS`  -  demographic and scale cols
        * `load_data(compiled_csv="../question_answers_round_3_with_coins.csv", questionaire_path="../data/CGHP Study - Questionnaires_July 22, 2024_08.16.csv", pat_data_path="../data/PAT",)`  -  loads and prepares questionnaire and gameplay data
        * `configure_logging(logging_level, filename)`  -  configures logging via passed in logging level string and name of log file to save in `/logs/`
        * `replace_with_parentheses_value(s)`  -  extracts the first substring enclosed in parentheses from `s` and replaces the entire `(value)` with `value`
        * `dict_append_or_create_list(dict, key, value)`  -  appends a value to a list in a dictionary or creates a new list if the key doesn't exist
    
    * And contains the nonessential `PatInfo` Class:
        * Contains a participant's data profile, including questionnaire responses and game data and metrics
        * Loads and processes the data through GMM computation and questionnaire response organization
        * Methods for coin performance analysis, step functions calculation, and raw and derived data aggregation

* [Block Randomization](rand_yaml.md)  
    * Maps each participant to one of eight counterbalancing block sequences (`structure0`–`structure7`)

* [Structure JSON](structure_json.md)  
    * Defines the layout of each block and the sequence of blocks for each randomized structure used