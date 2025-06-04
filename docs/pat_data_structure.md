# `PatDataStructure` Class

The `PatDataStructure` class is used to track inidivual participant game data across all 24 levels.

---

### `__init__(self, file_path=None, dry_run=False, save_dir=None)`

Initializes a `PatDataStructure` instance with respective parameters. The `file_path` parameter indicates where the raw data is. Set `dry_run` to true for tracing information. `save_dir` is currently not used in the code base. 

PatDataStucture stores information for each tick (a specified unit of time) of the game. This information includes the location of the player and each of the three AI agents, the average distance from the player to the uncollected coins on board, the number of coins the player has collected, the number of keys the player has collected. As the processing of the data is happening, the data structure also stores information related to where the coins are located and the ticks at which the player / one of the agents has collected a coin. The data is stored level by level.

---

### `init_level_stucture(self, level: int)`

Initializes an empty data structure for the passed in game level.

---

### `convert_to_np_array(self, level: int)`

Converts passed in game level data into corresponding NumPy arrays, which leads to more efficient storage / computation. 

---

### `group_levels(self) -> dict`

Groups levels into separate folders which correspond to a block. This method searches for a break in the contiguity of the levels as this break indicates the next block. Within the game, levels 1-2 are part of the first block, levels 4–7 are part of the second block, levels 10–11 are part of the third block, levels 13–16 are part of the fourth block, levels 19–20 are part of the fifth block, levels 22–25 are part of the sixth block, levels 28–29 are part of the seventh block, and levels 31–34 are part of the eighth block. There are no levels 3, 8–9, 12, 17–18, 21, 26–27, or 30, and the breakage there signifies the end of the grouping and the lead on to the next group. The blocks that contain solely two levels are the neutral blocks. 

This structure is mirrored in the naming of the folders, where each folder is labeled using the pattern levels_<start>_to_<end>. For example, levels_1_to_2, levels_4_to_7, and so on.

---

### `save_level_data(self, level: int, path=None)`

Saves level-specific data to an `.npz` file within the corresponding folder.

---

### `save_data(self, path: str = None)`

Saves all levels' data by calling `save_level_data()` for each level. There are four main folders, each labeled with the specific condition. Within 

---

### `load_data(self, root_folder: str)`

Loads all `.npz` files from the files saved by `save_data`, populating each field.


---

### `add_data(self, target_var: list, level: int, input_data)`

Appends the data to respective level’s passed in field. `target_var` is the specific field we're trying to add the data to, `level` is the index at which to store this data, and `input_data` is what's going to be added in. 

---

### `reset_vars(self)`

Resets temporary game variables to 0.

---