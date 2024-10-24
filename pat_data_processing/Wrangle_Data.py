import numpy as np
import re
from pat_data_processing.Utils import (
    load_data,
    PROJECT_ROOT,
    dict_append_or_create_list,
    BLOCKTYPES,
    COINTYPES,
    SHORT_BLOCKTYPES,
)
import logging
import datetime
import pandas as pd
import os


class DataWrangler:
    def __init__(self, data_path: os.PathLike = None, dry_run: bool = False) -> None:
        self.data_path = data_path
        self.dry_run = dry_run
        self.logger = logging.getLogger("processing")

        self.PAT_df = None  # set by wrangle data
        self.PAT_diffed_df = None  # set by wrangle_diffs

        self.compiled_csv = os.path.join(self.data_path, "temp_PAT_variables.csv")
        self.questionaire_path = os.path.join(
            self.data_path, "CGHP Study - Questionnaires_July 22, 2024_08.15.csv"
        )
        self.pat_data_path = os.path.join(self.data_path, "PAT")

        if not os.path.exists(self.compiled_csv):
            self.logger.error(f"Compiled data not found at {self.compiled_csv}")
            raise FileNotFoundError(f"Compiled data not found at {self.compiled_csv}")

        if not os.path.exists(self.questionaire_path):
            self.logger.error(
                f"Questionaire data not found at {self.questionaire_path}"
            )
            raise FileNotFoundError(
                f"Questionaire data not found at {self.questionaire_path}"
            )

        if not os.path.exists(self.pat_data_path):
            self.logger.error(f"PAT data not found at {self.pat_data_path}")
            raise FileNotFoundError(f"PAT data not found at {self.pat_data_path}")

        if not os.path.exists(
            os.path.join(PROJECT_ROOT, "data", "questionaire_scores.csv")
        ):
            self.logger.error(
                f"Questionaire scores not found at {os.path.join(PROJECT_ROOT, 'data', 'questionaire_scores.csv')}"
            )
            raise FileNotFoundError(
                f"Questionaire scores not found at {os.path.join(PROJECT_ROOT, 'data', 'questionaire_scores.csv')}"
            )

        self.logger.info("Loading data")
        (
            self.data_list,
            __,
            __,
            __,
            __,
        ) = load_data(
            compiled_csv=self.compiled_csv,
            questionaire_path=self.questionaire_path,
            pat_data_path=self.pat_data_path,
        )

    def run_wrangling(self):
        self.wrangle_data()
        self.wrangle_diffs()
        self.add_acc()
        self.save_all()

    def wrangle_data(self):
        df_val_dict = {}
        self.logger.info("Wrangling data")
        for i in range(len(self.data_list)):
            if self.data_list[i].hasPAT:

                dict_append_or_create_list(
                    df_val_dict, "pat_id", self.data_list[i].pat_id
                )
                for key in self.data_list[i].pat_dict_data.keys():
                    for key2 in self.data_list[i].pat_dict_data[key].keys():
                        dat = self.data_list[i].pat_dict_data[key][key2]
                        newkey = key + " " + key2

                        if type(dat[0]) is not int:
                            vals = dat[0]["Score"].values
                            if len(vals) >= 1:
                                if (
                                    type(vals[0]) is np.float64
                                    or type(vals[0]) is float
                                    or vals[0].isnumeric()
                                ):
                                    vals = vals.astype(float)
                                    vals = np.mean(vals)
                                else:
                                    vals = vals[0]
                                dict_append_or_create_list(df_val_dict, newkey, vals)
                for key in self.data_list[i].questionaire_answers:
                    dict_append_or_create_list(
                        df_val_dict,
                        key,
                        list(self.data_list[i].questionaire_answers[key].items())[0][1],
                    )

        self.logger.log(0, df_val_dict.keys())
        for k in df_val_dict.keys():
            self.logger.log(0, f"{k} {len(df_val_dict[k])}")

        df = pd.DataFrame(df_val_dict, columns=df_val_dict.keys())
        questionaire_scores = pd.read_csv(
            os.path.join(PROJECT_ROOT, "data", "questionaire_scores.csv")
        )
        df = pd.merge(df, questionaire_scores, on="Q53", how="inner")
        df["pat_id"] = df["pat_id"].apply(lambda x: re.sub(r"\D", "", x))
        self.logger.log(10, df["pat_id"])
        self.PAT_df = df

    def wrangle_diffs(self):
        cols = self.PAT_df.columns
        self.logger.info("Wrangling diffs")
        difs = {}
        # rename columns to remove neutral -> and ":"
        # calculate sensitivity
        # remove "End of game questions"
        for c in cols:
            if "(neutral)" in c:
                # find the corresponding positive or negative (maybe with offset?)
                # and calculate the difference
                split = c.split(" ")
                joined_Var = str.join(" ", split[5:])
                new_col = str.join(
                    " ", [split[0].replace(":", ""), split[3], joined_Var]
                )
                replaced = c.replace("(neutral)", "(post-manipulation)")
                dif = self.PAT_df[c].values - self.PAT_df[replaced].values
                difs[new_col + " change"] = dif
            elif "post-block" in c:
                # rename
                split = c.split(" ")
                joined_Var = str.join(" ", split[5:])
                new_col = str.join(
                    " ", [split[0].replace(":", ""), split[3], joined_Var]
                )

                difs[new_col + " change"] = self.PAT_df[c].values
            else:
                difs[c] = self.PAT_df[c].values

        diffedDF = pd.DataFrame(difs)
        diffedDF = diffedDF[["Q53"] + [col for col in diffedDF.columns if col != "Q53"]]

        dif_cols = diffedDF.columns
        for c in dif_cols:
            if "positive" in c and diffedDF[c].dtype == "float64":
                neg = c.replace("positive", "negative")
                dif_col_name = c.replace("positive", "diff")
                ratio_col_name = c.replace("positive", "ratio")
                diffedDF[dif_col_name] = diffedDF[c] - diffedDF[neg]
                diffedDF[ratio_col_name] = diffedDF[c] / diffedDF[neg]

        self.PAT_diffed_df = diffedDF

    def add_acc(self):

        counts = []
        # each row use code below to get get counts and check max of every 4? values
        for block in BLOCKTYPES:
            split_block = block.split(" ")
            # Find columns that contain all elements of split_block
            matching_columns = [
                col
                for col in self.PAT_df.columns
                if col.startswith(split_block[0])
                and all([elem in col for elem in split_block[1:]])
            ]
            for match in matching_columns:
                if any([elem in match for elem in COINTYPES]):
                    counts.append(self.PAT_df[match].values)
                    self.logger.log(10, block)
                    self.logger.log(10, match)
        
        counts = np.array(counts).T
        self.logger.log(10, counts.shape)
        totals = []
        for i in range(4):
            neutral = counts[:, i::8]
            postmanip = counts[:, i + 4::8]
            total = neutral + postmanip*2
            self.logger.log(10, f"total shape: {total.shape}")
            totals.append(total)

        totals = np.array(totals)  # shape is (4 actors, n_participants, 4 blocktypes)
        self.logger.log(10, f"totals shape: {totals.shape}")
        maxes = totals.argmax(axis=0)
        maxes = maxes == 0
        maxes = maxes.astype(int)
        maxes[:, [2, 3]] = maxes[
            :, [3, 2]
        ]  # swap to make sure the order is correct for short blocktypes
        player_bool_cols = [
            " ".join([block, "player most boolean"]) for block in SHORT_BLOCKTYPES
        ]
        
        overall_max = totals.sum(axis=2).T
        self.logger.log(10, f"overall max sums: {overall_max}")
        overall_max = overall_max.argmax(axis=1) == 0
        overall_max = overall_max.reshape(-1, 1)
        
        # should be (n_participants, 1)
        self.logger.log(10, f"overall max shape: {overall_max.shape}")
        self.logger.log(10, overall_max)
        player_bool_cols.append("Overall player most boolean")
        maxes = np.hstack([maxes, overall_max])
           
        self.logger.log(10, f"maxes shape: {maxes.shape}")
        self.logger.log(10, f"boolean cols: {player_bool_cols}")
        self.logger.log(10, maxes)
        
        max_df = pd.DataFrame(maxes, columns=player_bool_cols)

        self.PAT_acc_df = pd.concat([self.PAT_diffed_df, max_df], axis=1)

        question = (
            "Which player do you think collected the most coins? (select one) change"
        )
        for bool, block in zip(player_bool_cols, SHORT_BLOCKTYPES):
            block_question = " ".join([block, question])
            if_you = self.PAT_diffed_df[block_question] == "You"
            correct = self.PAT_acc_df[bool] == if_you
            block_correct = block_question.replace("change", "correct")
            self.PAT_acc_df[block_correct] = correct
        
        overall_question = "End of game questions Please rank the players from who got the MOST coins to who got the LEAST (You, P2, P3, P4)"
        most_responses = self.PAT_diffed_df[overall_question]
        
        def most_responses_correct_apply(response):
            if pd.isna(response) or response is None:
                return None
            self.logger.log(10, response)
            lower_most_response = response.lower()
            if_you = re.match(r"^(you|me)", lower_most_response) is not None
            self.logger.log(10, if_you)
            return if_you
        
        most_responses.map(most_responses_correct_apply)
        correct = self.PAT_acc_df["Overall player most boolean"] == if_you
        overall_correct = overall_question + " correct"
        self.PAT_acc_df[overall_correct] = correct
    
    def save_all(self):
        if not self.dry_run:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            self.PAT_df.to_csv(
                os.path.join(PROJECT_ROOT, "data", f"pat_compiled_sheet_{date}.csv"),
                index=False,
            )
            self.PAT_diffed_df.to_csv(
                os.path.join(
                    PROJECT_ROOT, "data", f"pat_compiled_sheet_diffed_{date}.csv"
                ),
                index=False,
            )
            self.PAT_acc_df.to_csv(
                os.path.join(
                    PROJECT_ROOT, "data", f"pat_diffes_with_accuracy_{date}.csv"
                ),
                index=False,
            )


if __name__ == "__main__":  # pragma: no cover
    wrangler = DataWrangler()
