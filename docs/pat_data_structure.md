# `PatDataStructure` Class

The `PatDataStructure` class is used to track inidivual participant game data across all 36 levels.

---

### `__init__(self, file_path=None, dry_run=False, save_dir=None)`

Initializes a `PatDataStructure` instance with respective parameters. 

---

### `init_level_stucture(self, level: int)`

Initializes an empty data structure for the passed in game level.

---

### `convert_to_np_array(self, level: int)`

Converts passed in game level data into corresponding NumPy arrays, which leads to more efficient storage / computation. 

---

### `group_levels(self) -> dict`

Groups levels into separate folders which correspond to a block. 

---

### `save_level_data(self, level: int, path=None)`

Saves level-specific data to an `.npz` file within the corresponding folder.

---

### `save_data(self, path: str = None)`

Saves all levels' data by calling `save_level_data()` for each level.

---

### `load_data(self, root_folder: str)`

Loads all `.npz` files from the files saved by `save_data`, populating each field.

---

### `add_data(self, target_var: list, level: int, input_data)`

Appends passed in data to passed in level’s passed in field.

---

### `reset_vars(self)`

Resets temporary game variables to 0.

---