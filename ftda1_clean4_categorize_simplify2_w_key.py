# author: Austin Pursley
# date: 2022-01-17
# french toast recipe analysis
# cleaning data
# part 5: cleaning, categorize, simplifying ingredients (step 5)
# applying keys to complete clean-up

import pandas as pd
import numpy as np

ingr_cln_t = pd.read_csv("1_ingr_clean/0ingredients_clean_track.csv", index_col=False, na_filter = False)
# key we've put so much effort into making
ingr_m = pd.read_csv("1_ingr_clean/4ingr_clean_key.csv", index_col=False, na_filter = False)
vc_m = ingr_m.value_counts()

# ingr_m["Replacement"] = np.where(ingr_m["Replacement"] != "", ingr_m["Replacement"], ingr_m["Ingredient"])

old_ingr = list(ingr_m["Ingredient"])
for i in old_ingr:
    replacement = ingr_m.loc[ingr_m["Ingredient"] == i]["Replacement"].item()
    if replacement:
        ingr_cln_t.loc[ingr_cln_t["ingr_wrds_cln"] == i, ["ingr_wrds_cln2"]] = replacement
    else:
        ingr_m.loc[ingr_m["Ingredient"] == i, ["Replacement"]] = i
        ingr_cln_t.loc[ingr_cln_t["ingr_wrds_cln"] == i, ["ingr_wrds_cln2"]] = i
    
new_ingr = list(ingr_m["Replacement"])
for i in new_ingr:
    category = ingr_m.loc[ingr_m["Replacement"] == i]["Category"].iloc[0]
    ingr_cln_t.loc[ingr_cln_t["ingr_wrds_cln2"] == i, ["category"]] = category
    
    subcategory = ingr_m.loc[ingr_m["Replacement"] == i]["Subcategory"].iloc[0]
    ingr_cln_t.loc[ingr_cln_t["ingr_wrds_cln2"] == i, ["subcategory"]] = subcategory

test = ingr_cln_t["ingr_wrds_cln2"].value_counts()
ingr_cln_t2 = pd.DataFrame(columns=["title", "ingr_full", "quant", "units", "ingr", "category", "subcategory"])
ingr_cln_t2["title"] = ingr_cln_t["title"]
ingr_cln_t2["ingr_full"] = ingr_cln_t["ingr_full"]
ingr_cln_t2["quant"] = ingr_cln_t["ingr_num_total"]
ingr_cln_t2["units"] = ingr_cln_t["ingr_units"]
ingr_cln_t2["ingr"] = ingr_cln_t["ingr_wrds_cln2"]
ingr_cln_t2["category"] = ingr_cln_t["category"]
ingr_cln_t2["subcategory"] = ingr_cln_t["subcategory"]
ingr_cln_t2.to_csv("french_toast_recipes_1_cleaned_draft.csv", index=False) 
