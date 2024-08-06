import os
import re
import argparse
import logging
from pat_data_processing.PAT_Data_Structure import PatDataStructure
import numpy as np
import pandas as pd
from tqdm import tqdm

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLOCKTYPES = [
    "coin: neutral -> positive (neutral)",
    "coin: neutral -> positive (post-manipulation)",
    "coin: neutral -> positive (post-block)",
    "coin: neutral -> negative (neutral)",
    "coin: neutral -> negative (post-manipulation)",
    "coin: neutral -> negative (post-block)",
    "speed: neutral -> negative (neutral)",
    "speed: neutral -> negative (post-manipulation)",
    "speed: neutral -> negative (post-block)",
    "speed: neutral -> positive (neutral)",
    "speed: neutral -> positive (post-manipulation)",
    "speed: neutral -> positive (post-block)",
    "End of game questions",
]
COINTYPES = [
    "player coins",
    "e1 coins",
    "e2 coins",
    "e3 coins",
]

SHORT_BLOCKTYPES = [
    "coin positive",
    "coin negative",
    "speed positive",
    "speed negative",
]

COINBLOCKS = [
    "coin: neutral -> positive (neutral)",
    "coin: neutral -> positive (post-manipulation)",
    "coin: neutral -> negative (neutral)",
    "coin: neutral -> negative (post-manipulation)",
    "speed: neutral -> positive (neutral)",
    "speed: neutral -> positive (post-manipulation)",
    "speed: neutral -> negative (neutral)",
    "speed: neutral -> negative (post-manipulation)",
]
QUESTIONTYPES = [
    "player coins",
    "e1 coins",
    "e2 coins",
    "e3 coins",
    "To what extent do you feel happy right now?",
    "Confident?",
    "Stressed?",
    "Excited?",
    "Frustrated?",
    "Proud?",
    "How much would you like to keep playing this game?",
    "How well are you playing this game right now?",
    "Which player do you think collected the most coins? (select one)",
    "Please rank the players from who got the MOST coins to who got the LEAST (You, P2, P3, P4)",
    "Overall, how fair was this game?",
    "How much did you enjoy playing this game?",
    "How likely are you to recommend this game to a friend?",
]
NEUTRALKEYS = [val for val in BLOCKTYPES if "(neutral)" in val]
STATSTYPES = [
    "gmm average",
    "gmm first third average",
    "gmm second third average",
    "gmm third third average",
    "gmm std",
    "gmm first third std",
    "gmm second third std",
    "gmm third third std",
    "gmm area under the curve",
]


def load_data(
    compiled_csv="../question_answers_round_3_with_coins.csv",
    questionaire_path="../data/CGHP Study - Questionnaires_July 22, 2024_08.16.csv",
    pat_data_path="../data/PAT",
):
    pat_coin_data = pd.read_csv(compiled_csv)
    questionaire_data = pd.read_csv(questionaire_path)
    game_data_root = pat_data_path

    questionaire_data = questionaire_data.loc[
        :, questionaire_data.columns.str.startswith("Q")
    ]
    question_descriptions = questionaire_data.iloc[0]
    questionaire_data = questionaire_data.drop(1)
    questionaire_data = questionaire_data[questionaire_data["Q53"].str.contains("PAT")]

    null_counts = pd.DataFrame(questionaire_data.isnull().sum().transpose())
    null_counts = null_counts.transpose()
    null_counts.to_csv("CGHP null_counts.csv")
    patInfoList = []
    for pat_id in (pbar := tqdm(questionaire_data["Q53"].unique())):
        # TODO: Check for inefficient memory usage here
        pbar.set_description(f"Loading {pat_id}")
        patInfoList.append(
            PatInfo(pat_id, questionaire_data, pat_coin_data, game_data_root)
        )

    return (
        patInfoList,
        null_counts,
        questionaire_data,
        pat_coin_data,
        question_descriptions,
    )


def configure_logging(logging_level, filename):
    numeric_level = getattr(logging, logging_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {logging_level}")
    filehandler = logging.FileHandler(
        os.path.join(PROJECT_ROOT, "logs", filename), mode="a"
    )
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[filehandler, logging.StreamHandler()],
    )


def replace_with_parentheses_value(s):
    # TODO: check if unused and delete
    match = re.search(r"\((.*?)\)", s)
    if match:
        value = match.group(1)
        s = s.replace(match.group(0), value)
        return s, value
    return s, None


def dict_append_or_create_list(dict, key, value):
    if key in dict:
        dict[key].append(value)
    else:
        dict[key] = [value]


class PatInfo:
    def __init__(self, pat_id, questionaire_data, pat_coin_data, pat_game_root):
        self.pat_id = pat_id

        self.questionaire_data = questionaire_data
        self.pat_coin_data = pat_coin_data
        self.questionaire_answers = None
        self.pat_data = None
        self.pat_game_root = pat_game_root
        self.pat_data_struct = None
        self.order = None
        self.pat_dict_data = {
            key: {k: [] for k in QUESTIONTYPES + STATSTYPES} for key in BLOCKTYPES
        }
        self.neutrals = []
        self.hasPAT = True
        self.filteredLevels = None
        self.logger = logging.getLogger("processing")
        self.get_pat_data()
        self.process_struct_data()
        self.aggregate_question_responses()
        self.get_order()

        self.neutrals = []
        self.get_neutrals()
        self.pat_data_struct
        self.logger.log(3, f"{self.pat_id}")
        self.logger.log(3, f"{self.pat_data.columns}")
        self.logger.log(3, f"{self.pat_data["Question"].unique()}")

    def extract_number(self, s):
        match = re.search(r"PAT_?(\d+)", s)
        if match:
            return int(match.group(1))
        else:
            return None

    def get_pat_data(self):
        self.questionaire_answers = self.questionaire_data[
            self.questionaire_data.Q53 == self.pat_id
        ]
        integer_id = int(self.extract_number(self.pat_id))
        self.pat_data = self.pat_coin_data[self.pat_coin_data.PAT_ID == integer_id]
        self.pat_data.reset_index(drop=True, inplace=True)
        self.pat_data_struct = PatDataStructure("./output")
        pat_data_path = os.path.join(
            self.pat_game_root, "PAT" + str(integer_id).zfill(3)
        )

        if os.path.isdir(pat_data_path):
            pat_data_path = os.path.join(
                pat_data_path, os.listdir(pat_data_path)[-1], "all_data"
            )

            self.logger.log(2, f"Loading data from {pat_data_path}")
            self.pat_data_struct.load_data(pat_data_path)
        else:
            self.hasPAT = False
            self.logger.warning(f"No PAT data found for {self.pat_id}")

    def process_struct_data(self):
        if self.pat_data_struct is not None:
            coin_idx = self.pat_data.loc[
                self.pat_data["Question"] == "player coins"
            ].index
            # coin_idx = self.pat_data[self.pat_data["Question"] == "player coins"].index
            level_stats = self.compute_gmm_features()
            if len(level_stats) == 0:
                self.logger.warning(f"No level stats found for {self.pat_id}")
            for idx, stats in zip(coin_idx, level_stats):
                row_object_copy = self.pat_data.loc[idx].copy()
                stack = np.vstack([row_object_copy.values] * 9)
                stack[:, 3] = STATSTYPES
                stack[:, 4] = stats
                self.pat_data = pd.concat(
                    [self.pat_data, pd.DataFrame(stack, columns=self.pat_data.columns)],
                    ignore_index=True,
                )

    def make_step(self, step_intervals, level_ticks):
        step_func = np.zeros(len(level_ticks))
        for interval in step_intervals:
            step_index = np.where(level_ticks == interval)[0][0]
            zeros = np.zeros(len(level_ticks[:step_index]))
            ones = np.ones(len(level_ticks[step_index:]))
            combined = np.concatenate((zeros, ones))
            step_func += combined

        return step_func

    def compute_real_score(self, level):
        levelCoins = self.pat_data_struct.player_coin_ticks[level]
        levelTicks = self.pat_data_struct.all_ticks[level]
        step_func = self.make_step(levelCoins, levelTicks)[:, np.newaxis]
        return (
            self.pat_data_struct.player_level_score[level][0] + step_func,
            levelTicks,
            levelCoins,
        )

    def compute_gmm_features(self):
        filtered_indices = [
            i
            for i, score in enumerate(self.pat_data_struct.player_level_score)
            if score is not None
        ]
        self.filteredLevels = filtered_indices
        # print(filtered_indices)
        # print(self.pat_data_struct.player_level_score)
        level_stats = []
        if len(filtered_indices) == 0:
            self.logger.warning(f"No filtered indices found for {self.pat_id}")
            self.logger.warning(f"{self.pat_data_struct.player_level_score}")
        for level in filtered_indices:
            score, levelTicks, levelCoins = self.compute_real_score(level)
            gmmStats = self.compute_gmm_stats(score, levelTicks)
            level_stats.append(gmmStats)

        return level_stats

    def weighted_avg_and_std(self, values, weights):
        """
        Return the weighted average and standard deviation.

        They weights are in effect first normalized so that they
        sum to 1 (and so they must not all be 0).

        values, weights -- NumPy ndarrays with the same shape.
        """
        average = np.average(values, weights=weights)
        # Fast and numerically precise:
        variance = np.std(values)
        return (average, variance)

    def compute_gmm_stats(self, score, levelTicks):
        interval = np.diff(levelTicks)
        vectorScore = score[:-1].ravel()
        weighted_average, weighted_std = self.weighted_avg_and_std(
            vectorScore, interval
        )
        one_third = int(len(score) / 3)
        first_third_avg, first_third_std = self.weighted_avg_and_std(
            vectorScore[:one_third], interval[:one_third]
        )
        second_third_avg, second_third_std = self.weighted_avg_and_std(
            vectorScore[one_third : 2 * one_third],
            interval[one_third : 2 * one_third],
        )
        third_third_avg, third_third_std = self.weighted_avg_and_std(
            vectorScore[2 * one_third :], interval[2 * one_third :]
        )

        area = np.trapz(score.ravel(), x=levelTicks)
        normalized_area = area
        return (
            weighted_average,
            first_third_avg,
            second_third_avg,
            third_third_avg,
            weighted_std,
            first_third_std,
            second_third_std,
            third_third_std,
            area,
        )

    def get_order(self):
        array = self.pat_data["Question Type"].unique()
        every_third_value = array[::3]
        # Remove values between parentheses
        every_third_value = [
            re.sub(r"\(.*?\)", "", value).strip() for value in every_third_value
        ]

        self.order = every_third_value

    def aggregate_question_responses(self):
        for Btype in BLOCKTYPES:
            for question in QUESTIONTYPES:
                val = self.pat_data[
                    (self.pat_data["Question Type"] == Btype)
                    & (self.pat_data["Question"] == question)
                ]
                if len(val) > 0:
                    self.pat_dict_data[Btype][question].append(val)
                else:
                    self.pat_dict_data[Btype][question].append(-1)
            for gmm_feature in STATSTYPES:
                val = self.pat_data[
                    (self.pat_data["Question Type"] == Btype)
                    & (self.pat_data["Question"] == gmm_feature)
                ]
                # print(val)
                if len(val) > 0:
                    self.pat_dict_data[Btype][gmm_feature].append(val)
                else:
                    self.pat_dict_data[Btype][gmm_feature].append(-1)

    def get_neutrals(self):
        for Btype in NEUTRALKEYS:
            for question in QUESTIONTYPES:
                if len(self.pat_dict_data[Btype][question]) > 0:
                    self.neutrals.append(self.pat_dict_data[Btype][question])
