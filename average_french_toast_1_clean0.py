# author: Austin Pursley
# date: 2022-01-15
# french toast recipe analysis
# cleaning data
# part 0: cutting recipes based on ingredients, variants

import pandas as pd

ft = pd.read_csv("french_toast_recipes.csv", index_col=False)

# removing variants
var = ["casserole", "sandwhich", "sandwich", "sandwhiches", "sandwiches", "stick", "sticks", 
             "fingers", "bites", "roll-ups", "banana-roll", "cookies", "wrapped-in-bacon",
             "toast-bake", "kabobs", "strata", "souffle", "soufle", "cobbler", "in-a-cup",
             "baked", "bake", "cups", "slow-cooker", "no-fry", "overnight", "slow-cooker"]
mask_var = ~(ft["Title"].str.contains(r'\b(?:{})\b'.format('|'.join(var))))
ft[~mask_var].to_csv("0_cut_ft_recipes/french_toast_recipes_cut_variants.csv",index=False)

# looking for recipes that don't have basic ingredients (bread, milk, eggs)
# bread
bread = ["bread", "toast", "baguette", "croissant", "hawaiian", 
                "challah", "brioche", "mexican bolillo rolls", "pannetone",
                "italian bread"]
mask_bread = ft["Ingredients"].str.contains(r'\b(?:{})\b'.format('|'.join(bread)))
ft[~mask_bread].to_csv("0_cut_ft_recipes/french_toast_recipes_cut_no_bread.csv",index=False)
#milk
milk = ["milk", "milks", "half-and-half", "half and half", "heavy whipping cream", 
                 "heavy cream", "egg nog", "eggnog", "whipping cream", "light cream", 
                 "mascarpone cheese", "irish cream liqueur"]
mask_milk = ft["Ingredients"].str.contains(r'\b(?:{})\b'.format('|'.join(milk)))
ft[~mask_milk].to_csv("0_cut_ft_recipes/french_toast_recipes_cut_no_milk.csv",index=False)
# eggs
eggs = ["egg", "eggs", "egg substitute", "egg beaters"]
mask_egg = ft["Ingredients"].str.contains(r'\b(?:{})\b'.format('|'.join(eggs)))
ft[~mask_egg].to_csv("0_cut_ft_recipes/french_toast_recipes_cut_no_egg.csv",index=False)

mask = mask_var & mask_bread & mask_milk & mask_egg

ft_non = ft[~mask] 
ft_clean = ft[mask]

ft_no_milk = ft[mask_var & mask_bread & mask_egg & ~mask_milk]

ft_non.to_csv("0_cut_ft_recipes/french_toast_recipes_cut_all.csv",index=False)
ft_clean.to_csv("french_toast_recipes_0_post_cut.csv",index=False)
ft_no_milk.to_csv("french_toast_recipes_0_post_cut_no_milk.csv",index=False)

# note: manually removed other elements as well. e.g. recipes where called out 
#       breads to be cubed.