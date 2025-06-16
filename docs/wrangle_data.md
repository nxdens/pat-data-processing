# `DataWrangler` Class

Processes compiled participant data, questionnaire responses, and metrics.

---

### `__init__(self, data_path, dry_run=False)`

Initializes with paths to compiled data, questionnaire data, and game-level `.npz` data. 

Raises errors if expected files are not found. Also loads the full list of participant data by calling [`load_data()`](utils.md#load_datacompiled_csv-questionaire_path-pat_data_path).

---

### `run_wrangling(self)`

Runs `wrangle_data()`, `wrangle_diffs()`, `add_acc()`, and `save_all()`

---

### `wrangle_data(self)`

Creates a DataFrame that contains coin scores + GMM features, questionnaire answers, and merged subscale scores from `questionaire_scores.csv`, which is stored in `self.PAT_df`.

---

### `wrangle_diffs(self)`

Calculates differences -- subtracts post-manipulation from neutral block scores and adds diff and ratio columns comparing positive and negative conditions. This is stored in `self.PAT_diffed_df`.

---

### `add_acc(self)`

Calculates coin collection accuracy  -- determines which actor collected the most coins in each block, determines whether the player collected the most coins, determines whether the player correctly guessed who got the most coins. This is stored in `self.PAT_acc_df`.

---

### `most_responses_correct_apply(response)`

Returns `True` if participant believes they have collected the most coins and `False` otherwise.

---

### `save_all(self)`

If not in dry run mode, saves `pat_compiled_sheet_<DATE>.csv`, `pat_compiled_sheet_diffed_<DATE>.csv`, and `pat_diffes_with_accuracy_<DATE>.csv`


