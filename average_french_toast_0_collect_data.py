# author: Austin Pursley
# date: 2022-01-15
# french toast recipe analysis
# part 0: extract french toast recipes from raw allrecipes.com data
# data coming from: https://github.com/onzie9/all_recipes_data

import regex as re
import pandas as pd

raw_recipe_data_dir = "all_recipes_data-master/DataFiles/"
raw_data_list = ["raw_data_1.txt", "raw_data_2.txt", "raw_data_3.txt",
                 "raw_data_4.txt"]

pattern = r"=======================================(?:\n|\r\n?)((.*)+)(?:\n|\r\n?)((.*)+)(?:\n|\r\n?)(\[(([^=]|\n)*)+\])"
recipereg = re.compile(pattern)
df = pd.DataFrame(columns=["Title", "Type", "Ingredients"])
for fn in raw_data_list:
    f_loc = raw_recipe_data_dir + fn
    f = open(raw_recipe_data_dir + fn)
    contents = f.read()
    m = re.findall(pattern, contents)
    df_temp = pd.DataFrame(columns=["Title", "Type", "Ingredients"])
    df_temp["Title"] = [x[0] for x in m]
    df_temp["Type"] = [x[2] for x in m]
    df_temp["Ingredients"] = [x[4] for x in m]
    df = df.append(df_temp)
    contents = re.sub(pattern, r"TITE: \1 \n TYPE: \3 \n INGREDIENT: \5", contents)
    
df.to_csv("all_recipes.csv", index=False)

# drop unnecessary columns
df = df.drop('Type', axis=1)
# make sure everything is lowercase
df["Title"] = df["Title"].str.lower()
df["Ingredients"] = df["Ingredients"].str.lower()
# drops rows that don't contain "french" and "toast" in the title of recipe
df = df[(df["Title"].str.contains("french")) & (df["Title"].str.contains("toast"))]
# drop duplicate rows
df = df.drop_duplicates()
# double check ingredient frequency / no duplicates
count_ingredients = df["Ingredients"].value_counts()
# write CSV
df["Ingredients"] = df["Ingredients"].str.strip('[]')
df.to_csv("french_toast_recipes.csv", index=False)