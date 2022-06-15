# author: Austin Pursley
# date: 2022-01-17
# french toast recipe analysis
# cleaning data
# part 3: cleaning, categorize, simplifying ingredients (step 2)
# working out key for clean-up, classifciation
# see: "ingr_clean_key.csv" for result of effort

import pandas as pd

ingr_cln = pd.read_csv("1_ingr_clean/0ingredients_clean_track.csv", index_col=False, na_filter = False)
# below csv updated throughout process of this step
# e.g. run, look at data, find new version of bread, add to CSV, run again
# just represents a first step in classificaiton. see key for final classes
ingr_cls = pd.read_csv("1_ingr_clean/3ingr_class_init.csv", index_col=False, na_filter = False)

# going through ingredient lists to simplify + classify them further
# Spyder Variable Explorer gettin lots of use here
ingr_cln_unq = pd.DataFrame(ingr_cln["ingr_wrds"].unique(), columns=["ingr_wrds"])
ingr_cln_unq["ingr_wrds"] =  ingr_cln_unq["ingr_wrds"].str.strip()
ingr_cln_unq = pd.DataFrame(ingr_cln_unq["ingr_wrds"].unique(), columns=["ingr_wrds"])
bread = list(ingr_cls["bread"].unique()); bread.remove('')
mask_bread = ingr_cln_unq["ingr_wrds"] .str.contains(r'\b(?:{})\b'.format('|'.join(bread)))
ingr_bread = ingr_cln_unq[mask_bread]["ingr_wrds"] .unique()

milk = list(ingr_cls["milkcream"].unique()); milk.remove('')
mask_milk = ingr_cln_unq["ingr_wrds"] .str.contains(r'\b(?:{})\b'.format('|'.join(milk)))
ingr_milk = ingr_cln_unq[mask_milk]["ingr_wrds"] .unique()

eggs = list(ingr_cls["eggs"].unique()); eggs.remove('')
mask_eggs = ingr_cln_unq["ingr_wrds"] .str.contains(r'\b(?:{})\b'.format('|'.join(eggs)))
ingr_eggs = ingr_cln_unq[mask_eggs]["ingr_wrds"] .unique()

fruits = list(ingr_cls["fruit"].unique())
mask_fruits = ingr_cln_unq["ingr_wrds"] .str.contains(r'\b(?:{})\b'.format('|'.join(fruits)))
ingr_fruits = ingr_cln_unq[mask_fruits]["ingr_wrds"] .unique()

nut = list(ingr_cls["nuts"].unique()); nut.remove('')
sweets = list(ingr_cls["sweet"].unique()); sweets.remove('')
fats = list(ingr_cls["fat"].unique()); fats.remove('')
flav = list(ingr_cls["flavor"].unique()); flav.remove('')
comb = nut + sweets + fats + flav
mask_adds1 = ingr_cln_unq["ingr_wrds"] .str.contains(r'\b(?:{})\b'.format('|'.join(comb)))
ingr_adds1 = ingr_cln_unq[mask_adds1]["ingr_wrds"] .unique()

dairy = list(ingr_cls["dairy"].unique()); dairy.remove('')
mask_dairy = ingr_cln_unq["ingr_wrds"] .str.contains(r'\b(?:{})\b'.format('|'.join(dairy)))
ingr_dairy = ingr_cln_unq[mask_dairy]["ingr_wrds"] .unique()

ingr_other = ingr_cln_unq[~(mask_bread | mask_milk | mask_eggs | mask_fruits | mask_adds1 | mask_dairy)]["ingr_wrds"] .unique()