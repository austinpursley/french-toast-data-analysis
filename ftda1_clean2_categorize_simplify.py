# author: Austin Pursley
# date: 2022-01-16
# french toast recipe analysis
# cleaning data
# part 2: cleaning, categorize, simplifying ingredients (step 1)
# inital simplification of ingredient words, seperating units
import pandas as pd
import numpy as np

# as prep for this step, we've figured out units and words want to cut / replace
# - see "2units_key.csv" and "2words_cut_key.csv"
# and those files are updated throughout this step
# CSV to store and track/visualize cleaning process
ingr_clean = pd.read_csv("1_ingr_clean/0ingredients_clean_track.csv", index_col=False)


# apply units key
units_df = pd.read_csv("1_ingr_clean/2units_key.csv", index_col=False, na_filter = False)
units_df["ingr_units_replace"] = np.where(units_df["ingr_units_replace"] == "", units_df["ingr_units"], units_df["ingr_units_replace"])
units = list(units_df["ingr_units"])
# add units according to key for each ingredient
ingr_clean["ingr_units"] = ""
for u  in units:
    ingr_clean.loc[ingr_clean["ingr_full"].str.contains(r"\b"+u+r"\b", regex=True), ["ingr_units"]] = u
    u_replacement = units_df[units_df["ingr_units"] == u]["ingr_units_replace"].item()
    if u_replacement:
        ingr_clean["ingr_units"] = ingr_clean["ingr_units"].str.replace(r"\b"+u+r"\b", u_replacement, regex=True)
    ingr_clean["ingr_wrds"] = ingr_clean["ingr_wrds"].str.replace(r"\b"+u+r"\b", "", regex=True)
ingr_clean["ingr_units"] = ingr_clean["ingr_units"].str.replace(r" +", r" ", regex=True)
ingr_clean["ingr_units"] =  ingr_clean["ingr_units"].str.strip()
ingr_clean["ingr_wrds"] = ingr_clean["ingr_wrds"].str.replace(r" +", r" ", regex=True)
ingr_clean["ingr_wrds"] =  ingr_clean["ingr_wrds"].str.strip()


# numbers
nums_df = pd.read_csv("1_ingr_clean/2nums_key.csv", index_col=False, na_filter = False)
nums = list(nums_df["ingr_nums"])
ingr_clean["ingr_cnt"] = ""
ingr_clean["ingr_qnt"] = ""
for n in nums:
    cnt = nums_df.loc[nums_df["ingr_nums"] == n]["ingr_cnt_replace"].item()
    ingr_clean.loc[ingr_clean["ingr_nums"] == n, ["ingr_cnt"]] = cnt
    qnt = nums_df.loc[nums_df["ingr_nums"] == n]["ingr_qnt_replace"].item()
    ingr_clean.loc[ingr_clean["ingr_nums"] == n, ["ingr_qnt"]] = qnt
    num_total = nums_df.loc[nums_df["ingr_nums"] == n]["ingr_num_total"].item()
    ingr_clean.loc[ingr_clean["ingr_nums"] == n, ["ingr_num_total"]] = num_total
# applying some automation here. 
# however, still have to manually go through and edit as necessary

# test = ingr_cln_t["ingr_wrds_cln_nonu2"].value_counts()
# ingr_cln_t2 = pd.DataFrame(columns=["ingr_full", "quant", "units", "ingr"])
# ingr_cln_t2["ingr_full"] = ingr_cln_t["ingr_full"]
# ingr_cln_t2["ingr"] = ingr_cln_t["ingr_wrds_cln_nonu2"]

# simply inredients lists by cutting certain words
wrd_cut_df = pd.read_csv("1_ingr_clean/2words_cut_key.csv", index_col=False, na_filter = False)
ingr_clean["ingr_wrds_cln"] = ingr_clean["ingr_wrds"]
unique_cut_wrds = wrd_cut_df["Words Cuts"].value_counts()
cut = list(wrd_cut_df["Words Cuts"])
for w in cut:
    ingr_clean["ingr_wrds_cln"] = ingr_clean["ingr_wrds_cln"].str.replace(r"\b"+w+r"\b", "", regex=True)
ingr_clean["ingr_wrds_cln"] = ingr_clean["ingr_wrds_cln"].str.replace(r" +", r" ", regex=True)
ingr_clean["ingr_wrds_cln"] =  ingr_clean["ingr_wrds_cln"].str.strip()

ingr_clean.to_csv("1_ingr_clean/0ingredients_clean_track.csv", index=False)