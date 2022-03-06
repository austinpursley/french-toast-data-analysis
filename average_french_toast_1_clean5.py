# author: Austin Pursley
# date: 2022-03-05
# french toast recipe analysis
# cleaning data
# part 6: final quality checks

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ft_recipes = pd.read_csv("french_toast_recipes_cleaned_final.csv", index_col=False, na_filter = False)

# look at number and how often each title appears.
# # title appears = # ingredients 
# revealed some duplicates had to remove
qa_check_title = ft_recipes["title"].value_counts() 

# check each recipe only has only one bread, one eggs, and one milk/cream
# NOTE: some recipes call for both eggs and egg whites.
# NOTE: some recipes have mix of milks/creams
bread = ft_recipes.loc[ft_recipes["category"] == "bread"]
eggs = ft_recipes.loc[ft_recipes["category"] == "eggs"]
milkcream = ft_recipes.loc[ft_recipes["category"] == "milkcream"]
qa_check_bread = (bread["title"] + " " + bread["category"]).value_counts()
qa_check_eggs = (eggs["title"] + " " + eggs["category"]).value_counts()
qa_check_milkcream = (milkcream["title"] + " " + milkcream["category"]).value_counts()

# check ingr with commas, make sure caught all multiple / combined ingredients and seperated them