# author: Austin Pursley
# date: 2022-03-05
# french toast recipe analysis
# cleaning data
# part 6: final quality checks

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
ft_recipes_og = pd.read_csv("french_toast_recipes.csv", index_col=False, na_filter = False)
ft_recipes = pd.read_csv("french_toast_recipes_cleaned_final.csv", index_col=False, na_filter = False)

# look at number and how often each title appears.
# # title appears = # ingredients 
# revealed some duplicates had to remove
qc_check_title = ft_recipes["title"].value_counts() 
# other value counts
qc_check_category = ft_recipes["category"].value_counts() 
qc_check_catsub = ft_recipes["subcategory"].value_counts() 
qc_check_cat_and_sub = ft_recipes[["category", "subcategory"]].value_counts() 

# check each recipe only has only one bread, one eggs, and one milk/cream
# NOTE: some recipes call for both eggs and egg whites.
# NOTE: some recipes have mix of milks/creams
bread = ft_recipes.loc[ft_recipes["category"] == "bread"]
eggs = ft_recipes.loc[ft_recipes["category"] == "eggs"]
milkcream = ft_recipes.loc[ft_recipes["category"] == "milkcream"]
qc_check_bread = (bread["title"] + " " + bread["category"]).value_counts()
qc_check_eggs = (eggs["title"] + " " + eggs["category"]).value_counts()
qc_check_milkcream = (milkcream["title"] + " " + milkcream["category"]).value_counts()

# other
qc_check_flavor = ft_recipes.loc[ft_recipes["category"] == "flavor", ["ingr"]].value_counts()
qc_check_sugar = ft_recipes.loc[ft_recipes["category"] == "sugar", ["ingr"]].value_counts()
qc_check_fat = ft_recipes.loc[ft_recipes["category"] == "fat", ["ingr"]].value_counts()
qc_check_fruit = ft_recipes.loc[ft_recipes["category"] == "fruit", ["ingr"]].value_counts()
qc_check_dairy = ft_recipes.loc[ft_recipes["category"] == "dairy", ["ingr"]].value_counts()
qc_check_syrup = ft_recipes.loc[ft_recipes["category"] == "syrup", ["ingr"]].value_counts()

# check which have a fat (indicative fried / sautted)
# egg_grp = egg.groupby(['title','category'])['ingr'].apply(' and '.join).reset_index()
ingr_group = ft_recipes.groupby(["title"])['category'].apply(','.join).reset_index()
fat_mask = (ingr_group["category"].str.contains("fat"))
ft_fat_titles = ingr_group[fat_mask].value_counts()
ft_no_fat_titles = ingr_group[~fat_mask].value_counts().reset_index()["title"]

# checks for duplicates
dup_og_titles = ft_recipes_og[ft_recipes_og.duplicated(["Title"])]

dup_title_ing_quant_units = ft_recipes[ft_recipes.duplicated(["title", "ingr","quant","units"])]
# instance of frozen butter and butter in apple-pie-french-toast
# instance of room temp butter and butter in bacon-crusted
# instance of 1 cup of blueberry for seperate ingredient steps (total 2 cups) blue-berry-french-toast
# blueberry-stuffed-french-toast, same as above but also with sugar in two steps
# cinsammon-raisin-stuffed-french-toast, cinnamon in two steps
# fabulous frosted french toast, sugar in two steps
# few more left... will assume that all duplicates are intentional, 
# cases where ingredients used in another step

dup_title_ing = ft_recipes[ft_recipes.duplicated(["title", "ingr"])]

# "or" check
mask_ors_all = (ft_recipes["ingr_full"].str.contains(r"\bor\b"))
ft_ors_all = ft_recipes[mask_ors_all]
mask_or_bread = (ft_recipes["ingr_full"].str.contains(r"\bor\b")) & (ft_recipes["category"] =="bread")
ft_ors_bread = ft_recipes[mask_or_bread]
mask_or_mlk = (ft_recipes["ingr_full"].str.contains(r"\bor\b")) & (ft_recipes["category"] =="milkcream")
ft_ors_mlk = ft_recipes[mask_or_mlk]
mask_or_eggs = (ft_recipes["ingr_full"].str.contains(r"\bor\b")) & (ft_recipes["category"] =="eggs")
ft_ors_eggs = ft_recipes[mask_or_eggs]
or_other = mask_ors_all & ~(mask_or_bread | mask_or_mlk | mask_or_eggs)
ft_ors_other = ft_recipes[or_other]

# "and" check
mask_and_all = (ft_recipes["ingr_full"].str.contains(r"\band\b"))
ft_and_all = ft_recipes[mask_and_all]

# mods / operations
# (if wanted, could add this info to current "cut" column)
mod = ["cut", "cubed", "sliced", "crushed", "crumbled", "trimmed", "whipped", "diced", "mashed", "softened",
       "beaten", "melted", "divided", "warmed", "heated", "divided", "chopped", "toasted", 
       "drained", "peeled", "rinsed", "defrosted", "slivered", "unwrapped", "torn", "removed", "thawed",
       "cored"]
mask_mod = ft_recipes["ingr_full"].str.contains(r'\b(?:{})\b'.format('|'.join(mod)))
ft_mod = ft_recipes[mask_mod]
# checks related to commas 
mask_comma = (ft_recipes["ingr_full"].str.contains(","))
mask_to_taste = (ft_recipes["ingr_full"].str.contains("to taste")) | (ft_recipes["ingr_full"].str.contains("as needed")) 
comma_but_no_or = mask_comma & ~mask_ors_all
ft_comma_but_no_or = ft_recipes[comma_but_no_or]
comma_no_mod = mask_comma & ~mask_mod
ft_comma_no_process = ft_recipes[comma_no_mod]
ft_comma_no_process_no_to_taste = ft_recipes[comma_no_mod & ~mask_to_taste]
mask_confection = (ft_recipes["ingr_full"].str.contains("confection"))
ft_confection = ft_recipes[mask_confection]

# check reciped that call for cubing bread are removed
mask_bread_cubed = (ft_recipes["ingr_full"].str.contains(r"cubed|cubes")) & (ft_recipes["category"] =="bread")
ft_bread_cubed = ft_recipes[mask_bread_cubed]

# check baked recipes are removed
mask_baked = (ft_recipes["title"].str.contains(r"baled|bake"))
ft_baked = ft_recipes[mask_baked]

# checks with recipe instructions (had to scrape that data myself, see clean6)
instr_check = pd.read_csv("recipe_data_scraped/ft_recipes_scrape_ingr_instr-master.csv", index_col=False, na_filter = False)
titles_scraped = set(instr_check["title"].unique())
instr_check = instr_check.set_index("title")
titles = set(ft_recipes["title"].unique())

cut = list(titles_scraped - titles)

instr_check = instr_check.drop(cut)

instr_check["contains baked"] = instr_check["instructions"].str.lower().str.contains(r"bake|baked|oven|degrees", regex=True)
instr_check["contains overnight"] = instr_check["instructions"].str.lower().str.contains(r"overnight|fridge", regex=True)
instr_check["no skillet"] = ~(instr_check["instructions"].str.lower().str.contains(r"pan|skillet|griddle|waffle iron", regex=True))
instr_check.to_csv("instr_check.csv")