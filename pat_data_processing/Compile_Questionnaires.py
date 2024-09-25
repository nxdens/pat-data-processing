import pandas as pd
import pat_data_processing.Utils as Utils
import os
import logging


def compile_EDS(df: pd.DataFrame, drop_cols=True):
    eds_data = df[["Q53"] + Utils.EDS_COLS].drop(index=[0, 1])
    eds_data = eds_data.dropna()
    eds_data[Utils.EDS_COLS] = eds_data[Utils.EDS_COLS].astype(int)

    eds_data["EDS_total"] = eds_data.iloc[:, 1:-2].sum(
        axis=1
    )  # currently includes Q11 which might not be correct
    eds_chron = [0, 0.5, 3, 36, 104, 260]  # might be 360
    vals = eds_data.iloc[:, 1:-2]
    eds_data["EDS_ChroTotal"] = vals.map(lambda x: eds_chron[int(x)]).sum(axis=1)

    if drop_cols:
        eds_data.drop(columns=Utils.EDS_COLS, inplace=True)

    return eds_data


def compile_SWBS(df: pd.DataFrame, subscales=True, drop_cols=True):
    swbs_data = df[["Q53"] + Utils.SWBS_COLS].drop(index=[0, 1])
    swbs_data = swbs_data.dropna()
    swbs_data[Utils.SWBS_COLS] = swbs_data[Utils.SWBS_COLS].astype(int)

    Social_Integration = ["Q90_2", "Q90_6", "Q90_11"]
    Social_Acceptance = ["Q90_3", "Q90_10", "Q90_14"]
    Social_Contribution = ["Q90_4", "Q90_7", "Q90_15"]
    Social_Actualization = ["Q90_5", "Q90_9", "Q90_13"]
    Social_Coherence = ["Q90_1", "Q90_8", "Q90_12"]
    swbs_data["WellBeingSum"] = swbs_data.iloc[:, 1:].sum(axis=1)
    if subscales:
        swbs_data["WB_Integ"] = swbs_data[Social_Integration].sum(axis=1)
        swbs_data["WB_Acce"] = swbs_data[Social_Acceptance].sum(axis=1)
        swbs_data["WB_Contri"] = swbs_data[Social_Contribution].sum(axis=1)
        swbs_data["WB_Actua"] = swbs_data[Social_Actualization].sum(axis=1)
        swbs_data["WB_Coher"] = swbs_data[Social_Coherence].sum(axis=1)

    if drop_cols:
        swbs_data.drop(columns=Utils.SWBS_COLS, inplace=True)

    return swbs_data


def compile_RiC(df: pd.DataFrame, subscales=True, drop_cols=True):
    ric_data = df[["Q53"] + Utils.RIC_COLS].drop(index=[0, 1])
    ric_data = ric_data.dropna()
    ric_data[Utils.RIC_COLS] = ric_data[Utils.RIC_COLS].astype(int)

    ric_data["RiC_NumFriend_Q1"] = ric_data.iloc[:, 1]
    ric_data["RiC_NumFriend_Q1"] = ric_data.iloc[:, 2]
    frequency = ["Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]
    same_freq = ["Q3", "Q5", "Q7"]
    diff_freq = ["Q4", "Q6", "Q8"]

    quality = ["Q3a", "Q4a", "Q5a", "Q6a", "Q7a", "Q8a"]
    same_qual = ["Q3a", "Q5a", "Q7a"]
    diff_qual = ["Q4a", "Q6a", "Q8a"]

    ric_data["RiC_Frequency"] = ric_data[frequency].mean(axis=1)
    ric_data["RiC_Quality"] = ric_data[quality].mean(axis=1)
    ric_data["RiC_AveSameRace_freq"] = ric_data[same_freq].mean(axis=1)
    ric_data["RiC_AveDiffRace_freq"] = ric_data[diff_freq].mean(axis=1)
    ric_data["RiC_AveSameRace_quali"] = ric_data[same_qual].mean(axis=1)
    ric_data["RiC_AveDiffRace_quali"] = ric_data[diff_qual].mean(axis=1)

    if subscales:
        ric_data["RiC_SameLeisure_Freq_Q3"] = ric_data["Q3"]
        ric_data["RiC_DiffLeisure_Freq_Q4"] = ric_data["Q4"]
        ric_data["RiC_SameWork_Freq_Q5"] = ric_data["Q5"]
        ric_data["RiC_DiffWork_Freq_Q6"] = ric_data["Q6"]
        ric_data["RiC_SameOnline_Freq_Q7"] = ric_data["Q7"]
        ric_data["RiC_DiffOnline_FreqQ8"] = ric_data["Q8"]

        ric_data["RiC_SameLeisure_Quali_Q3a"] = ric_data["Q3a"]
        ric_data["RiC_DiffLeisure_Quali_Q4a"] = ric_data["Q4a"]
        ric_data["RiC_SameWork_Quali_Q5a"] = ric_data["Q5a"]
        ric_data["RiC_DiffWork_Quali_Q6a"] = ric_data["Q6a"]
        ric_data["RiC_SameOnline_Quali_Q7a"] = ric_data["Q7a"]
        ric_data["RiC_DiffOnline_Quali_Q8a"] = ric_data["Q8a"]

    if drop_cols:
        ric_data.drop(columns=Utils.RIC_COLS, inplace=True)

    return ric_data


def compile_CSE(df: pd.DataFrame, subscales=True, drop_cols=True):
    cse_data = df[["Q53"] + Utils.CSE_COLS].drop(index=[0, 1])
    cse_data = cse_data.dropna()
    cse_data[Utils.CSE_COLS] = cse_data[Utils.CSE_COLS].astype(int)

    cse_data["CSEsum"] = cse_data.iloc[:, 1:].sum(axis=1)
    membership = [Utils.CSE_COLS[i - 1] for i in [1, 5, 9, 13]]
    private_collective = [Utils.CSE_COLS[i - 1] for i in [2, 6, 10, 14]]
    public_collective = [Utils.CSE_COLS[i - 1] for i in [3, 7, 11, 15]]
    importance = [Utils.CSE_COLS[i - 1] for i in [4, 8, 12, 16]]
    if subscales:
        cse_data["CSEmember"] = cse_data[membership].sum(axis=1)
        cse_data["CSEprivate"] = cse_data[private_collective].sum(axis=1)
        cse_data["CSEpublic"] = cse_data[public_collective].sum(axis=1)
        cse_data["CSEidentity"] = cse_data[importance].sum(axis=1)

    if drop_cols:
        cse_data.drop(columns=Utils.CSE_COLS, inplace=True)
    return cse_data


def compile_SWLS(df: pd.DataFrame, drop_cols=True):
    swls_data = df[["Q53"] + Utils.SWLS_COLS].drop(index=[0, 1])
    swls_data = swls_data.dropna()
    swls_data[Utils.SWLS_COLS] = swls_data[Utils.SWLS_COLS].astype(int)

    swls_data["SWLSSum"] = swls_data.iloc[:, 1:].sum(axis=1)

    if drop_cols:
        swls_data.drop(columns=Utils.SWLS_COLS, inplace=True)

    return swls_data


def compile_MSPSS(df: pd.DataFrame, subscales=True, drop_cols=True):
    mspss_data = df[["Q53"] + Utils.MSPSS_COLS].drop(index=[0, 1])
    mspss_data = mspss_data.dropna()
    mspss_data[Utils.MSPSS_COLS] = mspss_data[Utils.MSPSS_COLS].astype(int)

    mspss_data["MSPSS_total"] = mspss_data.iloc[:, 1:].mean(axis=1)
    significant_other = ["Q92_1", "Q92_2", "Q92_5", "Q92_10"]
    family = ["Q92_3", "Q92_4", "Q92_8", "Q92_11"]
    friends = ["Q92_6", "Q92_7", "Q92_9", "Q92_12"]
    if subscales:
        mspss_data["MSPSS_SigOther"] = mspss_data[significant_other].mean(axis=1)
        mspss_data["MSPSS_Family"] = mspss_data[family].mean(axis=1)
        mspss_data["MSPSS_Friend"] = mspss_data[friends].mean(axis=1)

    if drop_cols:
        mspss_data.drop(columns=Utils.MSPSS_COLS, inplace=True)
    return mspss_data


def compile_Chronic_Strains(df: pd.DataFrame, drop_cols=True):
    chronic_strain_data = df[["Q53"] + Utils.CHRONIC_STRAINS_COLS].drop(index=[0, 1])
    chronic_strain_data = chronic_strain_data.dropna()
    chronic_strain_data[Utils.CHRONIC_STRAINS_COLS] = chronic_strain_data[
        Utils.CHRONIC_STRAINS_COLS
    ].astype(int)

    chronic_strain_data["ChroStrain_total"] = chronic_strain_data.iloc[:, 1:].sum(
        axis=1
    )
    if drop_cols:
        chronic_strain_data.drop(columns=Utils.CHRONIC_STRAINS_COLS, inplace=True)
    return chronic_strain_data


def main(data_path):
    csv_path = os.path.join(
        data_path, "CGHP Study - Questionnaires_July 22, 2024_08.16.csv"
    )
    logger = logging.getLogger("Compiling")
    df = pd.read_csv(csv_path)
    eds_df = compile_EDS(df)
    swbs_df = compile_SWBS(df)
    ric_df = compile_RiC(df)
    cse_df = compile_CSE(df)
    swls_df = compile_SWLS(df)
    mspss_df = compile_MSPSS(df)
    strain_df = compile_Chronic_Strains(df)
    df_list = [eds_df, swbs_df, ric_df, cse_df, swls_df, mspss_df, strain_df]
    merged = eds_df
    for df in df_list[1:]:
        merged = pd.merge(merged, df, on="Q53", how="outer")

    logger.info(f"Compiled data from {csv_path}")
    savepath = os.path.join(Utils.PROJECT_ROOT, f"data/questionaire_scores.csv")
    merged.to_csv(savepath, index=False)


if __name__ == "__main__":
    test_path = (
        f"{Utils.PROJECT_ROOT}/data/CGHP Study - Questionnaires_July 22, 2024_08.16.csv"
    )
    main(test_path)
