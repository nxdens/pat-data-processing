# `Compile_Answers.py` 

Parses participant game responses and end-of-game survey data. Folders are structured like `PAT001`, `PAT002`, etc.

---

### `get_participant_answers(folder, randomization, structures, id=0)`

Parses the `data.json` file in a participant's folder and extracts the participant's question responses and final coin tallies for all actors.

The method uses the participant’s ID to look up their assigned structure and unrolls the block/question template accordingly.

The method eturns a list of rows with the format:  
`[PAT_ID, Question Type, Block Type, Question, Answer]`

---

### `find_folders(start)`

Searches from the given root directory for folders that contain `data.json`. Skips known bad folders.

The method returns a list of paths to valid PAT folders.

**This method is currently unused**

---

### `main(path="PAT_round2/", output_path="temp_PAT_variables.csv", dry_run=False)`

Loads randomization information for the participant from `rand.yaml`, loads block/question structure from `structure.json`, calls `find_folders()` to extract paths of participant folders, calls `get_participant_answers()` to parse and format the data, converts the output into a pandas DataFrame, and unless `dry_run=True`, saves the DataFrame to CSV.

The method returns the final DataFrame.