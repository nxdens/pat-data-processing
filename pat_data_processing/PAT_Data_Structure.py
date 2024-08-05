import numpy as np
import os


class PAT_Data_Structure:
    def __init__(self, file_path, dry_run=False, *args, **kwargs) -> None:
        self.file_path = file_path # file path should be a PAT_ID directory
        self.dry_run = dry_run
        # folder inside self.file_path to store the data
        self.data_folder_path = os.path.join(self.file_path, "all_data")
        os.makedirs(self.data_folder_path, exist_ok=True)

        self.TOTAL_LEVELS = 36

        # temp variables 
        self.current_level = 0
        self.player_coins = 0
        self.e1_coins = 0
        self.e2_coins = 0
        self.e3_coins = 0
        self.starting_coins = 0
        self.current_key = ""
        self.loc_of_player = (0, 0)
        self.loc_of_e1 = (0, 0)
        self.loc_of_e2 = (0, 0)
        self.loc_of_e3 = (0, 0)
        self.coin_index = 0
        self.num_coins_picked_up = 0
        self.coin_picked_up = False

        # data that will be stored in the npz file
        
        self.computed_data = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.player_locs = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.e1_locs = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.e2_locs = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.e3_locs = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.player_avg_distance = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.player_level_score = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.tick_coin_picked_up = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.tick_keys_pressed = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.tick_keys_binary = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.locations_of_coins = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.coins_key_presses = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.coin_ticks = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.player_coin_ticks = np.empty((self.TOTAL_LEVELS), dtype=object)
        self.all_ticks = np.empty((self.TOTAL_LEVELS), dtype=object)

    def init_level_stucture(self, level: int):
        self.computed_data[level] = []
        self.player_locs[level] = []
        self.e1_locs[level] = []
        self.e2_locs[level] = []
        self.e3_locs[level] = []
        self.player_avg_distance[level] = []
        self.player_level_score[level] = []
        self.tick_coin_picked_up[level] = []
        self.tick_keys_pressed[level] = []
        self.tick_keys_binary[level] = []
        self.locations_of_coins[level] = []
        self.coins_key_presses[level] = []
        self.coin_ticks[level] = []
        self.player_coin_ticks[level] = []
        self.all_ticks[level] = []

    def convert_to_np_array(self, level: int):
        self.computed_data[level] = np.array(self.computed_data[level])
        self.player_locs[level] = np.array(self.player_locs[level])
        self.e1_locs[level] = np.array(self.e1_locs[level])
        self.e2_locs[level] = np.array(self.e2_locs[level])
        self.e3_locs[level] = np.array(self.e3_locs[level])
        self.player_avg_distance[level] = np.array(self.player_avg_distance[level])
        self.player_level_score[level] = np.array(self.player_level_score[level])
        self.tick_coin_picked_up[level] = np.array(self.tick_coin_picked_up[level])
        self.tick_keys_pressed[level] = np.array(self.tick_keys_pressed[level])
        self.tick_keys_binary[level] = np.array(self.tick_keys_binary[level])
        self.locations_of_coins[level] = np.array(self.locations_of_coins[level])
        self.coins_key_presses[level] = np.array(self.coins_key_presses[level])
        self.coin_ticks[level] = np.array(self.coin_ticks[level])
        self.player_coin_ticks[level] = np.array(self.player_coin_ticks[level])
        self.all_ticks[level] = np.array(self.all_ticks[level])

    def group_levels(self):
        groups = []
        group_start = 1

        for level in range(1, self.TOTAL_LEVELS + 1):
            if self.computed_data[level - 1] is None:
                if level - 1 != group_start:
                    groups.append((group_start, level - 1))
                group_start = level
            elif level == self.TOTAL_LEVELS:
                groups.append((group_start, level))

        level_to_folder = {}
        for start, end in groups:
            folder_name = f"levels_{start}_to_{end-1}"
            for level in range(start, end + 1):
                level_to_folder[level] = folder_name

        return level_to_folder

    def save_level_data(self, level):
        groupings = self.group_levels()

        if self.computed_data[level] is not None:
            folder_name = groupings[level]
            if folder_name:
                level_directory = os.path.join(self.data_folder_path, folder_name)
                os.makedirs(level_directory, exist_ok=True)
                npz_file_path = os.path.join(level_directory, f"level_{level}_data.npz")

            np.savez(
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
            )

    def save_data(self):
        if self.dry_run:
            return
        for level in range(self.TOTAL_LEVELS):
            self.save_level_data(level)

    def load_data(self, root_folder: str):
        """loads data from the root_folder.
        root folder must contain subfolders for each level.

        Args:
            root_folder (str): folder containing the subfolders for each level block
        """
        if not os.path.exists(root_folder):
            root_folder = os.path.join(self.file_path)
        for folder_name in os.listdir(root_folder):
            folder_path = os.path.join(root_folder, folder_name)
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith(".npz"):
                        level = int(file.split("_")[1])
                        file_path = os.path.join(folder_path, file)

                        with np.load(file_path) as data:
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

    def add_data(self, target_var: list, level: int, input_data):
        if len(target_var) > level:
            target_var[level].append(input_data)
        else:
            target_var.append(input_data)

    def reset_vars(self):
        self.total_keys_pressed = 0
        self.keys_pressed_last_window = 0
        self.player_coins = 0
        self.e1_coins = 0
        self.e2_coins = 0
        self.e3_coins = 0
        self.start_window_flag = 0
        self.coin_index = 0
        self.num_coins_picked_up = 0
