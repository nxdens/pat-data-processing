# `PatJsonParser` Class

The `PatJsonParser` class parses the raw game data which comes in the form of JSON files. This data is converted into structured arrays. These arrays contain information at each tick of number of coins collected, number of key presses, etc. along with the broader location of coins. The information is processed, saved, and visualized in order to analyze further.

---

### `__init__(self, file_path, dry_run=False)`

Initializes a new instance of the `PatJsonParser`. `file_path`specifies the path to the JSON file containing the raw data. Set `dry_run` to true for tracing information.

`self.data` contains the Parsed JSON content, `self.this_file`tracks the current JSON file file path being parsed, `self.store_data` is the instance of `PatDataStructure` responsible for managing the current JSON's data, `self.window_length` manages the windowed statistics.

`total_keys_pressed`, `keys_pressed_last_window`, `start_window_tick`, `current_tick`, and `keys_pressed_this_window` are state variables. 

---

### `run(self)`

The driver method for processing the JSON data. 

The loop searches for the next level, calls `step_into_round()`, computes metrics, such as Euclidean and Gaussian distances, saves the data to an `.npz` file for each level, and saves visualizations of key presses and average distance to coins.

---

### `step_into_round(self, round_value)`

Processes game data within a round within a level tick by tick. This method tracks coin pickups, stores the actors' locations, counts key presses, and computes metrics per window through method calls.

The method appends the computed values to `computed_data`.

---

### `store_actor_locs(self, tick_value)`

Stores each actors' (player and the three AI agents) locations per ticks by extracting coordinates and appending `(x, y)` to `PatDataStructure`'s list.

---

### `update_actor_coins(self, tick_value)`

Calls `add_coin()` to store the coin count for each respective actor.

---

### `add_coin(self, coin_value, which_user)`

Increments the respective actor's coin count if there has been a change in the number of coins collected, adds the location of the coin collected with the corresponding tick and level, to the coin_ticks variable. It also adds this information to the variable storing which tick the respective actor collects a coin. 

---

### `count_key_presses(self, new_key)`

If a new key is pressed, logs a 1, increments the variable tracking the number of keys pressed, and stores the tick and level at which the key was pressed.

Otherwise, logs a 0.

Returns updated `total_keys_pressed`.

---

### `draw_graph(self)`

Produces scatter plots for key press count across the ticks per level. The x-axis indicates the ticks and the y-axis is the number of keys pressed in the tick window. 

These graphs are saved to `Keys pressed graphs/`.

---

### `picked_up_binary_mask(self)`

Generates a 30-element binary mask where `0` indicates the respective coin has been picked up and `1` indicates the coin is available to be collected.

This is appended to `tick_coin_picked_up`. 

---

### `calc_euc_dist(self)`

Calculates the Euclidean distance between the player and the remaining (i.e. uncollected) coins for each tick. Applies `tick_coin_picked_up` mask and stores average distance per tick in `player_avg_distance`.

---

### `calc_gaussian_dist(self, masks_new_dim, player_dists, level)`

Calculates the probabilistic scores for each actor’s proximity to the uncollected coins using Gaussian model.

Normalizes actor scores across all coins and the method resulsts in a `player_level_score`.

---

### `avg_dist_graphs(self)`

Produces plots of the average distance from player to the uncollected coins at each tick. The plots also includes when key presses and coin pick ups occur. A green line indicates a coin was picked up by the player and a red line indicates a coin was picked up by an AI agent. 

These plots are saved to `Average distance to coins graphs/`.
