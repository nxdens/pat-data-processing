import json
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import logging
from pat_data_processing.PAT_Data_Structure import PatDataStructure
from tqdm import tqdm

ACTORS = ["player", "e1", "e2", "e3"]
actor_key_mapping = {
    "player": "player position",
    "e1": "enemy1 position",
    "e2": "enemy2 position",
    "e3": "enemy3 position",
}
UNI_COV = np.array([[[6000, 0], [0, 6000]]])
DET_UNI_COV = np.linalg.det(UNI_COV)
INV_UNI_COV = np.linalg.inv(UNI_COV)


class PatJsonParser:
    def __init__(self, file_path, dry_run=False, *args, **kwargs):
        with open(file_path) as json_file:
            self.data = json.load(json_file)

        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing PAT_JSON_parser")
        self.this_file = file_path

        self.store_data = PatDataStructure(
            file_path=os.path.dirname(self.this_file), dry_run=dry_run
        )

        self.window_length = [1000, 1004]

        # state variables These stay here
        self.total_keys_pressed = 0
        self.keys_pressed_last_window = 0
        self.start_window_tick = 0
        self.current_tick = 0
        self.keys_pressed_this_window = 0

    def run(self):
        self.starting_coins = 30

        for level_key, level_value in self.data.items():
            if "level" in level_key:
                extract_level_num = level_key.split(" ")
                self.level_index = int(extract_level_num[1])
                self.store_data.init_level_stucture(level=self.level_index)

            # step into round if it is a game round
            if isinstance(level_value, dict):
                for __, round_value in level_value.items():
                    if isinstance(round_value, dict):
                        self.step_into_round(round_value)
                        self.store_data.reset_vars()
                        self.store_data.convert_to_np_array(level=self.level_index)

        self.calc_euc_dist()

        json_path = os.path.join(os.path.dirname(self.this_file), "coin_locations.json")
        with open(json_path, "w") as json_file:
            json.dump(
                self.store_data.locations_of_coins,
                json_file,
                default=lambda x: x.tolist(),
            )

        self.draw_graph()
        self.avg_dist_graphs()

        self.store_data.save_data()

        self.logger.info("Done with file %s", self.this_file)
        # self.store_data.load_data(self.store_data.file_path)

    def step_into_round(self, round_value):
        for _, tick_value in round_value.items():
            if isinstance(tick_value, dict):
                self.current_tick = int(tick_value["tick"])
                self.store_data.add_data(
                    target_var=self.store_data.all_ticks,
                    level=self.level_index,
                    input_data=self.current_tick,
                )

                self.store_actor_locs(tick_value=tick_value)

                if self.start_window_tick == 0 and self.keys_pressed_last_window == 0:
                    self.start_window_tick = self.current_tick
                    self.keys_pressed_last_window = self.total_keys_pressed

                self.update_actor_coins(tick_value)
                self.count_key_presses(tick_value["keys pressed"])

                self.picked_up_binary_mask()

                within_window = (
                    self.current_tick - self.start_window_tick >= self.window_length[0]
                    and self.current_tick - self.start_window_tick
                    <= self.window_length[1]
                )

                if within_window:
                    self.keys_pressed_this_window = (
                        self.total_keys_pressed - self.keys_pressed_last_window
                    )
                    self.start_window_tick = self.current_tick

                    list_to_add = [
                        self.start_window_tick,
                        self.store_data.player_coins,
                        self.store_data.e1_coins,
                        self.store_data.e2_coins,
                        self.store_data.e3_coins,
                        self.keys_pressed_this_window,
                    ]

                    self.store_data.add_data(
                        target_var=self.store_data.computed_data,
                        level=self.level_index,
                        input_data=list_to_add,
                    )

        self.keys_pressed_this_window = (
            self.total_keys_pressed - self.keys_pressed_last_window
        )
        self.start_window_tick = self.current_tick

        list_to_add = [
            self.start_window_tick,
            self.store_data.player_coins,
            self.store_data.e1_coins,
            self.store_data.e2_coins,
            self.store_data.e3_coins,
            self.keys_pressed_this_window,
        ]

        self.store_data.add_data(
            target_var=self.store_data.computed_data,
            level=self.level_index,
            input_data=list_to_add,
        )

    def store_actor_locs(self, tick_value):
        for actor in ACTORS:
            key = actor_key_mapping[actor]
            loc_temp = tick_value[key]
            x_str, y_str = loc_temp.strip("()").split(",")
            x = float(x_str.strip())
            y = float(y_str.strip())
            setattr(self, f"loc_of_{actor}", (x, y))
            if actor == "player":
                self.store_data.add_data(
                    target_var=self.store_data.player_locs,
                    level=self.level_index,
                    input_data=(x, y),
                )
                self.store_data.loc_of_player = (x, y)
            elif actor == "e1":
                self.store_data.add_data(
                    target_var=self.store_data.e1_locs,
                    level=self.level_index,
                    input_data=(x, y),
                )
                self.store_data.loc_of_e1 = (x, y)
            elif actor == "e2":
                self.store_data.add_data(
                    target_var=self.store_data.e2_locs,
                    level=self.level_index,
                    input_data=(x, y),
                )
                self.store_data.loc_of_e2 = (x, y)
            elif actor == "e3":
                self.store_data.add_data(
                    target_var=self.store_data.e3_locs,
                    level=self.level_index,
                    input_data=(x, y),
                )

                self.store_data.loc_of_e3 = (x, y)

    def update_actor_coins(self, tick_value):
        for actor_index, game_actor in enumerate(ACTORS):
            self.add_coin(
                coin_value=int(tick_value[game_actor + " coins"]),
                which_user=actor_index,
            )

    def add_coin(self, coin_value: int, which_user: int):
        if which_user == 0:
            if self.store_data.player_coins != coin_value:
                self.store_data.player_coins += 1
                self.store_data.add_data(
                    target_var=self.store_data.locations_of_coins,
                    level=self.level_index,
                    input_data=self.store_data.loc_of_player,
                )
                self.store_data.add_data(
                    target_var=self.store_data.coin_ticks,
                    level=self.level_index,
                    input_data=self.current_tick,
                )
                self.store_data.add_data(
                    target_var=self.store_data.player_coin_ticks,
                    level=self.level_index,
                    input_data=self.current_tick,
                )
                self.coin_picked_up = True
                self.store_data.num_coins_picked_up += 1

        elif which_user == 1:
            if self.store_data.e1_coins != coin_value:
                self.store_data.e1_coins += 1
                self.store_data.add_data(
                    target_var=self.store_data.locations_of_coins,
                    level=self.level_index,
                    input_data=self.store_data.loc_of_e1,
                )
                self.store_data.add_data(
                    target_var=self.store_data.coin_ticks,
                    level=self.level_index,
                    input_data=self.current_tick,
                )
                self.coin_picked_up = True
                self.store_data.num_coins_picked_up += 1

        elif which_user == 2:
            if self.store_data.e2_coins != coin_value:
                self.store_data.e2_coins += 1
                self.store_data.add_data(
                    target_var=self.store_data.locations_of_coins,
                    level=self.level_index,
                    input_data=self.store_data.loc_of_e2,
                )
                self.store_data.add_data(
                    target_var=self.store_data.coin_ticks,
                    level=self.level_index,
                    input_data=self.current_tick,
                )
                self.coin_picked_up = True
                self.store_data.num_coins_picked_up += 1

        elif which_user == 3:
            if self.store_data.e3_coins != coin_value:
                self.store_data.e3_coins += 1
                self.store_data.add_data(
                    target_var=self.store_data.locations_of_coins,
                    level=self.level_index,
                    input_data=self.store_data.loc_of_e3,
                )
                self.store_data.add_data(
                    target_var=self.store_data.coin_ticks,
                    level=self.level_index,
                    input_data=self.current_tick,
                )
                self.coin_picked_up = True
                self.store_data.num_coins_picked_up += 1

    def count_key_presses(self, new_key):
        if new_key != self.store_data.current_key:
            self.store_data.add_data(
                target_var=self.store_data.tick_keys_binary,
                level=self.level_index,
                input_data=1,
            )
            self.total_keys_pressed += 1
            self.store_data.add_data(
                target_var=self.store_data.tick_keys_pressed,
                level=self.level_index,
                input_data=self.current_tick,
            )
            self.store_data.current_key = new_key

        else:
            self.store_data.add_data(
                target_var=self.store_data.tick_keys_binary,
                level=self.level_index,
                input_data=0,
            )

        return self.total_keys_pressed

    def draw_graph(self):
        for level in range(len(self.store_data.computed_data)):
            if self.store_data.computed_data[level] is not None:
                keys = [tick[0] for tick in self.store_data.computed_data[level]]
                values = [
                    tick_data[-1] for tick_data in self.store_data.computed_data[level]
                ]

                plt.figure()
                sns.scatterplot(x=keys, y=values)
                plt.xlabel("Tick")
                plt.ylabel("Number of keys pressed")
                plt.title(
                    f"Number of keys pressed in the last 1000-1500 ticks for level {level}"
                )

                current_directory = os.path.dirname(self.this_file)
                keys_graphs_directory = os.path.join(
                    current_directory, "Keys pressed graphs"
                )
                os.makedirs(keys_graphs_directory, exist_ok=True)

                plt.savefig(
                    os.path.join(
                        keys_graphs_directory, f"level_{level}_graph_keys_pressed.png"
                    )
                )

                plt.close()

    def picked_up_binary_mask(self):
        vector = np.ones(30)
        vector[: self.store_data.num_coins_picked_up] = 0
        self.store_data.add_data(
            target_var=self.store_data.tick_coin_picked_up,
            level=self.level_index,
            input_data=vector,
        )

    def calc_euc_dist(self):
        for level in range(len(self.store_data.player_locs)):
            if self.store_data.player_locs[level] is not None:
                ticks = self.store_data.all_ticks[level]
                player_positions = self.store_data.player_locs[level][:]

                coin_positions = self.store_data.locations_of_coins[level]

                player_positions_reshaped = player_positions[:, np.newaxis, :]
                masks = np.array(self.store_data.tick_coin_picked_up[level])

                if len(coin_positions) < 30:
                    self.logger.warning(f"Less than 30 coins in level {level}")
                    masks = masks[:, : len(coin_positions)]

                subtraction = player_positions_reshaped - coin_positions
                # mask will be n, 30, 1
                # multiply the n, 30, 2 mask
                masks_new_dim = masks[:, :, np.newaxis]

                multiplication = np.multiply(subtraction, masks_new_dim)

                distances = np.linalg.norm(multiplication, axis=2)
                self.calc_gaussian_dist(masks_new_dim, subtraction, level)
                sum_distances = distances.sum(axis=1)  # n, 1
                num_nonzeroes = np.count_nonzero(distances, axis=1)  # n, 1
                avg_distances = np.divide(
                    sum_distances,
                    num_nonzeroes,
                    out=np.zeros_like(sum_distances),
                    where=num_nonzeroes != 0,
                )  # n,1

                # combine with ticks
                combined = np.column_stack((ticks, avg_distances))
                directory_name = os.path.dirname(self.this_file)
                directory_name = os.path.join(directory_name, "npy files")
                os.makedirs(directory_name, exist_ok=True)

                self.store_data.player_avg_distance[level] = combined

    def calc_gaussian_dist(self, masks_new_dim, player_dists, level):
        def _get_z_scores(dists, mask):
            def _gaussian_dist(diff):
                return np.exp(
                    -1 / 2 * np.ndarray.dot(np.ndarray.dot(diff.T, INV_UNI_COV), diff)
                ) / np.sqrt((2 * np.pi) ** 2 * DET_UNI_COV)

            z_scores = np.zeros((dists.shape[0], dists.shape[1], 1))
            for i in range(dists.shape[0]):
                for j in range(dists.shape[1]):
                    if mask[i, j] > 0:
                        dist = _gaussian_dist(dists[i, j])
                        z_scores[i, j] = dist

            return z_scores

        if self.store_data.player_locs[level] is not None:
            # get and reshape all the positions
            coin_positions = self.store_data.locations_of_coins[level]
            e1_positions = self.store_data.e1_locs[level][:]
            e2_positions = self.store_data.e2_locs[level][:]
            e3_positions = self.store_data.e3_locs[level][:]

            e1_positions_reshaped = e1_positions[:, np.newaxis, :]
            e2_positions_reshaped = e2_positions[:, np.newaxis, :]
            e3_positions_reshaped = e3_positions[:, np.newaxis, :]

            # get all the distances and filter collected coins
            e1_dists = e1_positions_reshaped - coin_positions
            e2_dists = e2_positions_reshaped - coin_positions
            e3_dists = e3_positions_reshaped - coin_positions

            # should be n x 30 x 2
            player_z_scores = _get_z_scores(player_dists, masks_new_dim)
            e1_z_scores = _get_z_scores(e1_dists, masks_new_dim)
            e2_z_scores = _get_z_scores(e2_dists, masks_new_dim)
            e3_z_scores = _get_z_scores(e3_dists, masks_new_dim)

            concatenated_z_scores = np.stack(
                [player_z_scores, e1_z_scores, e2_z_scores, e3_z_scores], axis=0
            )

            summed_rows = np.sum(concatenated_z_scores, axis=0)
            assert summed_rows.shape == player_z_scores.shape

            player_probs = np.divide(
                player_z_scores,
                summed_rows,
                out=np.zeros_like(player_z_scores),
                where=summed_rows != 0,
            )
            e1_probs = np.divide(
                e1_z_scores,
                summed_rows,
                out=np.zeros_like(e1_z_scores),
                where=summed_rows != 0,
            )
            e2_probs = np.divide(
                e2_z_scores,
                summed_rows,
                out=np.zeros_like(e2_z_scores),
                where=summed_rows != 0,
            )
            e3_probs = np.divide(
                e3_z_scores,
                summed_rows,
                out=np.zeros_like(e3_z_scores),
                where=summed_rows != 0,
            )

            player_score = np.sum(player_probs, axis=1)

            self.store_data.player_level_score[level] = player_score

    def avg_dist_graphs(self):
        current_directory = os.path.dirname(self.this_file)
        dist_graphs_directory = os.path.join(
            current_directory, "Average distance to coins graphs"
        )
        os.makedirs(dist_graphs_directory, exist_ok=True)

        for level in range(len(self.store_data.player_avg_distance)):
            if self.store_data.player_avg_distance[level] is not None:
                groupings = self.store_data.group_levels()
                plt.figure(figsize=(25, 10))
                sns.scatterplot(
                    x=self.store_data.player_avg_distance[level][:, 0],
                    y=self.store_data.player_avg_distance[level][:, 1],
                )  # tick , average distance
                sns.scatterplot(
                    x=np.array(self.store_data.tick_keys_pressed[level]),
                    y=np.array(
                        -100 * np.ones(len(self.store_data.tick_keys_pressed[level]))
                    ),
                )

                for coin in self.store_data.coin_ticks[level]:
                    try:
                        if coin in self.store_data.player_coin_ticks[level]:
                            plt.axvline(
                                x=coin, color="g", linestyle="-", linewidth=0.75
                            )

                        else:
                            plt.axvline(
                                x=coin, color="r", linestyle="--", linewidth=0.75
                            )

                    except:
                        plt.axvline(x=coin, color="r", linestyle="--", linewidth=0.75)

                directory_name = os.path.dirname(self.this_file)
                directory_name = os.path.join(directory_name, "coin npy files")
                os.makedirs(directory_name, exist_ok=True)

                plt.title(f"Graph for Level {level}")
                plt.xlabel("Tick")
                plt.ylabel("Average Distance to Coins")

                level_directory = os.path.join(dist_graphs_directory, groupings[level])
                os.makedirs(level_directory, exist_ok=True)
                plt.savefig(
                    os.path.join(level_directory, f"level_{level}_avg_coin_dist.png")
                )
                plt.close()
