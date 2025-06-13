# `Compile_Answers.py` 

The PAT task has two advantage blocks and two disadvantage blocks. The advantage and disadvantage blocks are further broken down into speed or coin. The blocks are randomized with a counterbalanced block design. Each block has two neutral rounds, an inter-trial questionnaire, four rounds based on the condition, an inter-trial questionnaire, and a post-block questionnaire. After the four blocks, there is a postgame assessment. There are 36 total rounds, 24 of those rounds are game rounds and the rest are questionnaire rounds (either inter-trial or post-block).

The data is stored under `PAT_round2/` where each immediate subfolder is labeled `PATXXX` with the digit denoting the participant's unique ID. Within the subfolder, there is a directory labeled with a timestamp and within there is the participant's corresponding `data.json` file. Below is a visual of the structure:

```
PAT_round2/
├── PAT001/
│   └── [timestamp]/
│       └── data.json
├── PAT002/
│   └── [timestamp]/
│       └── data.json
...
```

---

### `get_participant_answers(folder, randomization, structures, id=0)`

Parses the `data.json` file in a participant's folder and extracts the participant's question responses and final coin tallies for all actors.

The method uses the participant’s ID to look up their assigned structure and unrolls the block/question template accordingly.

The method returns a list of rows with the format:  
`[PAT_ID, Question Type, Block Type, Question, Answer]`

---

### `find_folders(start)`

Searches from the given root directory for folders that contain `data.json`. Skips known bad folders.

The method returns a list of paths to valid PAT folders.

**This method is currently unused**

---

### `main(path="PAT_round2/", output_path="temp_PAT_variables.csv", dry_run=False)`

The `path` parameter contains a directory in which there are folders labeled `PATXXX`. 

The `output_path` is the name of the file to which the processed data will be written to. 

This method loads randomization information for the participant from `rand.yaml`, loads block/question structure from `structure.json`, calls `find_folders()` to extract paths of participant folders, calls `get_participant_answers()` to parse and format the data, converts the output into a pandas DataFrame, and unless `dry_run=True`, saves the DataFrame to CSV.

This method returns a final DataFrame with columns `["PAT_ID", "Block Type", "Question Type", "Question", "Score"]`