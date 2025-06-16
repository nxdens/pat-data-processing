# `PatDataStructure` Class

The `PatDataStructure` class is used to track individual participant game data across the 24 game levels.

---

### `__init__(self, file_path=None, dry_run=False, save_dir=None)`

Initializes a `PatDataStructure` instance with respective parameters. The `file_path` parameter indicates where the raw data is. Set `dry_run` to true for tracing information. `save_dir` is currently not used in the code base. 

PatDataStucture stores information for each tick (the time at which a new frame is drawn) of the game. This information includes the location of the player and each of the three AI agents, the average distance from the player to the uncollected coins on board, the number of coins the player has collected, the number of keys the player has collected. As the processing of the data is happening, the data structure also stores information related to where the coins are located and the ticks at which the player / one of the agents has collected a coin. The data is stored level by level.

List of all the variables defined in `__init__`:

* `self.file_path` – `str | None`  
* `self.dry_run` – `bool`  
* `self.logger` – `logging.Logger`  
* `self.data_folder_path` – `str`  
* `self.save_dir` – `str | None`  
* `self.TOTAL_LEVELS` – `int`  

* `self.current_level` – `int`  
* `self.player_coins` – `int`  
* `self.e1_coins` – `int`  
* `self.e2_coins` – `int`  
* `self.e3_coins` – `int`  
* `self.starting_coins` – `int`  
* `self.current_key` – `str`  
* `self.loc_of_player` – `tuple[int, int]`  
* `self.loc_of_e1` – `tuple[int, int]`  
* `self.loc_of_e2` – `tuple[int, int]`  
* `self.loc_of_e3` – `tuple[int, int]`  
* `self.coin_index` – `int`  
* `self.num_coins_picked_up` – `int`  
* `self.coin_picked_up` – `bool`  

* `self.computed_data` – `np.ndarray[object]`  
* `self.player_locs` – `np.ndarray[object]`  
* `self.e1_locs` – `np.ndarray[object]`  
* `self.e2_locs` – `np.ndarray[object]`  
* `self.e3_locs` – `np.ndarray[object]`  
* `self.player_avg_distance` – `np.ndarray[object]`  
* `self.player_level_score` – `np.ndarray[object]`  
* `self.tick_coin_picked_up` – `np.ndarray[object]`  
* `self.tick_keys_pressed` – `np.ndarray[object]`  
* `self.tick_keys_binary` – `np.ndarray[object]`  
* `self.locations_of_coins` – `np.ndarray[object]`  
* `self.coins_key_presses` – `np.ndarray[object]`  
* `self.coin_ticks` – `np.ndarray[object]`  
* `self.player_coin_ticks` – `np.ndarray[object]`  
* `self.all_ticks` – `np.ndarray[object]`


---

### `init_level_stucture(self, level: int)`

Initializes an empty data structure for the passed in game level. An empty data structure refers is when all the attributes consist of empty Pythons lists for the corresponding passed in level.

---

### `convert_to_np_array(self, level: int)`

Converts the passed in level's attributes, which are Python lists containing the participant's game data for that level, to NumPy arrays. This is for more efficient storage / computation. 

---

### `group_levels(self) -> dict`

Groups levels into separate folders which correspond to a block. This method searches for a break in the contiguity of the levels as this break indicates the next block. 

Within the game, 

* levels `1-2` are part of the **first** block, 
* levels `4–7` are part of the **second** block, 
* levels `10–11` are part of the **third** block, 
* levels `13–16` are part of the **fourth** block, 
* levels `19–20` are part of the **fifth** block, 
* levels `22–25` are part of the **sixth** block, 
* levels `28–29` are part of the **seventh** block, and 
* levels `31–34` are part of the **eighth** block

There are no levels 3, 8–9, 12, 17–18, 21, 26–27, or 30, and the breakage there signifies the end of the grouping and the lead on to the next group. Gaps in the level sequence are a transition between block types (game, post-block questionnaire, post-game assessment).

The blocks that contain solely **two levels are the neutral blocks**. 

This structure is mirrored in the naming of the folders, where each folder is labeled using the pattern levels_start_to_end. For example, levels_1_to_2, levels_4_to_7, and so on.

Returns a dictionary mapping each level to its corresponding folder name.

---

### `save_level_data(self, level: int, path=None)`

Saves level-specific data to an `.npz` file within the corresponding folder.

The data includes:
```python
npz_file_path,
computed_data=self.computed_data[level],
player_locs=self.player_locs[level],
e1_locs=self.e1_locs[level],
e2_locs=self.e2_locs[level],
e3_locs=self.e3_locs[level],
player_avg_distance=self.player_avg_distance[level],
player_level_score=self.player_level_score[level],
tick_coin_picked_up=self.tick_coin_picked_up[level],
tick_keys_pressed=self.tick_keys_pressed[level],
tick_keys_binary=self.tick_keys_binary[level],
locations_of_coins=self.locations_of_coins[level],
coins_key_presses=self.coins_key_presses[level],
coin_ticks=self.coin_ticks[level],
player_coin_ticks=self.player_coin_ticks[level],
all_ticks=self.all_ticks[level],
```

---

### `save_data(self, path: str = None)`

Saves all levels' data by calling `save_level_data()` for each level at the path defined by the `path` parameter. 

---

### `load_data(self, root_folder: str)`

Loads all `.npz` files from the files saved by `save_data`, filling each attribute with the data within the `.npz` file. 

```python
self.computed_data[level] = data["computed_data"]
self.player_locs[level] = data["player_locs"]
self.e1_locs[level] = data["e1_locs"]
self.e2_locs[level] = data["e2_locs"]
self.e3_locs[level] = data["e3_locs"]
self.player_avg_distance[level] = data[
    "player_avg_distance"
]
self.player_level_score[level] = (
    data["player_level_score"],
)
self.tick_coin_picked_up[level] = data[
    "tick_coin_picked_up"
]
self.tick_keys_pressed[level] = data["tick_keys_pressed"]
self.tick_keys_binary[level] = data["tick_keys_binary"]
self.locations_of_coins[level] = data["locations_of_coins"]
self.coins_key_presses[level] = data["coins_key_presses"]
self.coin_ticks[level] = data["coin_ticks"]
self.player_coin_ticks[level] = data["player_coin_ticks"]
self.all_ticks[level] = data["all_ticks"]
```

---

### `add_data(self, target_var: list, level: int, input_data)`

Appends the data to respective level’s passed in field. `target_var` is the specific field we're trying to add the data to, `level` is the index at which to store this data, and `input_data` is what's going to be added in. 

---

### `reset_vars(self)`

Resets temporary game variables to 0.

The temporary game variables are:
```python
self.total_keys_pressed
self.keys_pressed_last_window
self.player_coins
self.e1_coins
self.e2_coins
self.e3_coins
self.start_window_flag
self.coin_index
self.num_coins_picked_up
```

---