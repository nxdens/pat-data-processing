import pandas as pd
import json
import os
import numpy as np
from typing import Union, Dict, Any
import yaml
import json
import logging
from pat_data_processing.Utils import PROJECT_ROOT
from tqdm import tqdm


def get_participant_answers(
    folder: os.PathLike,
    randomization: Dict[str, int],
    structures,
    id: int = 0,
) -> Union[list[any], list[str]]:
    """This function reads the json file contained in the folder for each participant and
    parses the keys related to questions

    Args:
        folder (os.PathLike): folder path containing named PATXXX
        id (int, optional): ID of the participant for dataframe initialization purposes

    Returns:
        Union[list[any], list[str]]: returns 2 lists with the first containing the
            question answers and the second containing the question and shown in game.
    """
    logger = logging.getLogger("processing")
    output = []

    data_dict = {}
    id = os.path.basename(os.path.dirname(folder))
    id = int(id.split("PAT")[-1])
    logger.debug(f"Processing {id}")

    with open(os.path.join(folder, "data.json")) as f:
        data_dict = json.load(f)

    struct_num = randomization[str(id)]
    struct = structures["structure" + str(struct_num)]

    actors = ["player", "e1", "e2", "e3"]

    block_sub_type = ["neutral", "post-manipulation", "post-block"]
    q_sub_type = ["Inter-trial", "Inter-trial", "post-block"]
    qTypes = []
    unraveled_blocktypes = []
    for block in struct[:-1]:
        for bloc, q in zip(block_sub_type, q_sub_type):
            if bloc == "neutral":
                num_rounds = 3
            elif bloc == "post-manipulation":
                num_rounds = 5
            elif bloc == "post-block":
                num_rounds = 1

            for _ in range(num_rounds):
                unraveled_blocktypes.append(
                    structures["blocks"][block]["description"] + f" ({bloc})"
                )
                qTypes.append(q)

    unraveled_blocktypes.append("End of game questions")
    qTypes.append("End of game")
    # question_keys = [x for x in data_dict.keys() if "questions" in x]
    question_keys = data_dict.keys()
    for q_key, block_type, q in zip(question_keys, unraveled_blocktypes, qTypes):
        question_dict = data_dict[q_key]

        # skip first key
        if "questions" in q_key:
            dict_keys_iter = iter(question_dict.keys())
            __level = next(dict_keys_iter)
            for sub_key in dict_keys_iter:
                row = [
                    id,
                    q,
                    block_type,
                ]
                row.append(sub_key)
                try:
                    row.append(question_dict[sub_key][0])
                except:
                    logger.warning(f"empty answer for {id} {q_key}")
                    row.append(None)
                output.append(row)
        else:
            level_round_key = next(iter(question_dict.keys()))
            level_data = question_dict[level_round_key]
            last_tick = list(level_data.keys())[-1]
            last_tick_data = level_data[last_tick]

            for actor in actors:
                coin_key = actor + " coins"
                coins = last_tick_data[coin_key]
                row = [
                    id,
                    q,
                    block_type,
                ]
                row.append(coin_key)
                row.append(coins)
                output.append(row)
    return output


def find_folders(start):
    # theres a bug somewhere but i just copied the folders so unused for now
    logger = logging.getLogger("processing")
    exclude = "PAT_round2/PAT001/10_32_39"
    folders = []
    roots = []
    for root, dirs, files in os.walk(start, topdown=False):
        for name in files:
            if name == "data.json":
                if root != exclude:
                    folders.append(root)
    logger.info(f"Compiling {folders}")
    return folders


def main(
    path: str = "PAT_round2/",
    output_path: str = "temp_PAT_variables.csv",
    dry_run: bool = False,
) -> pd.DataFrame:
    columns = np.array(["PAT_ID", "Block Type", "Question Type", "Question", "Score"])
    logger = logging.getLogger("Compiling")
    logger.debug(
        "Reading file at %s", os.path.join(os.path.dirname(__file__), "rand.yaml")
    )
    with open(os.path.join(os.path.dirname(__file__), "rand.yaml"), "r") as stream:
        data = yaml.safe_load(stream)

    with open(os.path.join(os.path.dirname(__file__), "structure.json"), "r") as f:
        structs = json.load(f)

    all_outputs = []

    # read answers from the list of folders below
    # TODO: find the file contained in the directory.
    #       Currently not sure how to determine which sub folder

    folders = sorted(find_folders(path))

    for id, f in (pbar := tqdm(enumerate(folders))):
        pbar.set_description(f"Compiling data from PAT0{f}")
        outputs = get_participant_answers(f, data, structs, id + 1)
        all_outputs += outputs

    # long = format_as_long(all_answers[0],questions=questions,randomization=data)
    # print(long)
    # convert to numpy for better dimension shaping
    all_outputs = np.array(all_outputs)
    # create dataframe and export to csv
    print(all_outputs.shape)
    df = pd.DataFrame(data=all_outputs, columns=columns)
    # df.sort_values(by=["PAT_ID","Block Type"], inplace=True)
    df.set_index("PAT_ID")
    if not dry_run:
        df.to_csv(output_path, index=False)
        logger.info(f"Data written to {output_path}")
    else:
        logger.info("Dry run mode enabled. Not writing to file.")
        logger.info(df.head())
        logger.info(df.shape)
        logger.info(df.columns)
        logger.info(df.describe())
    return df


if __name__ == "__main__":
    main()
