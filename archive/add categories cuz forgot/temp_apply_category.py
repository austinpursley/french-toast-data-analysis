import pandas as pd
import numpy as np

ingr_cln_t = pd.read_csv("french_toast_recipes_3_cleaned_draft.csv", index_col=False, na_filter = False)
# key we've put so much effort into making
ingr_m = pd.read_csv("4ingr_clean_key.csv", index_col=False, na_filter = False)

# ingr_m["Replacement"] = np.where(ingr_m["Replacement"] != "", ingr_m["Replacement"], ingr_m["Ingredient"])

old_ingr = list(ingr_m["Ingredient"])
for i in old_ingr:
    replacement = ingr_m.loc[ingr_m["Ingredient"] == i]["Replacement"].item()
    if not replacement:
        ingr_m.loc[ingr_m["Ingredient"] == i, ["Replacement"]] = i

ingr = list(ingr_m["Replacement"])
for i in ingr:
    
    category = ingr_m.loc[ingr_m["Replacement"] == i]["Category"].iloc[0]
    ingr_cln_t.loc[ingr_cln_t["ingr"] == i, ["category"]] = category
    
    subcategory = ingr_m.loc[ingr_m["Replacement"] == i]["Subcategory"].iloc[0]
    ingr_cln_t.loc[ingr_cln_t["ingr"] == i, ["subcategory"]] = subcategory
    
ingr_cln_t.to_csv("french_toast_recipes_4_cleaned_draft.csv", index=False) 