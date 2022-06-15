# author: Austin Pursley
# date: 2022-03-12
# french toast recipe analysis
# plots

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pprint

ft_recipes = pd.read_csv("french_toast_recipes_cleaned_final.csv", index_col=False, na_filter = False) 
###############################################################################
###############################################################################
# BAR CHARTS, VERTICAL
###############################################################################
###############################################################################

bread = ft_recipes.loc[ft_recipes["category"] == "bread"]
bread = bread.sort_values(by=['ingr'])
bread_vc = bread[["title", "category"]].value_counts()
bread_grp = bread.groupby(['title','category'])['ingr'].apply(' and '.join).reset_index()
bread_cnt = bread_grp["ingr"].value_counts().reset_index()
bsz = len(bread_cnt["ingr"])
# ft_multi_bread = ft_recipes[ft_recipes["title"].isin(list(multi_bread_titles))]

mlk = ft_recipes.loc[ft_recipes["category"] == "milkcream"]
mlk = mlk.sort_values(by=['ingr'])
mlk_vc = mlk[["title", "category"]].value_counts()
mlk_grp = mlk.groupby(['title','category'])['ingr'].apply(' and '.join).reset_index()
mlk_cnt = mlk_grp["ingr"].value_counts().reset_index()
msz = len(mlk_cnt["ingr"])

egg = ft_recipes.loc[ft_recipes["category"] == "eggs"]
egg = egg.sort_values(by=['ingr'])
egg_vc = egg[["title", "category"]].value_counts()
egg_grp = egg.groupby(['title','category'])['ingr'].apply(' and '.join).reset_index()
egg_cnt = egg_grp["ingr"].value_counts().reset_index()
esz = len(egg_cnt["ingr"])

fig, axs = plt.subplots(3, 1, gridspec_kw={'height_ratios': [bsz, msz, esz]},
                        figsize=(10,14), constrained_layout=True)

# adjust title position to not be slightly off center
mid = (fig.subplotpars.right + fig.subplotpars.left)/2
fig.suptitle("allrecipes.com French Toast Recipes \n Essential Ingredient Types", fontsize=18, x=mid)

# colors
colors = plt.cm.get_cmap('tab20b', 20).colors
c1 = colors[0]
c2 = colors[5]
c3 = colors[9]

N = 23
y_pos = np.linspace(1,N*3.0,N)
xmax=100
#############################################
# bread
#############################################
ax = axs[0]
ax.set_xlim([0,xmax])
ax.margins(0.015)
y = y_pos[0:len(bread_cnt["ingr"])]
p1 = ax.barh(y, bread_cnt["ingr"][::-1], tick_label=bread_cnt["index"][::-1], 
                 height=2.5,  color=c1)
# ticks
ax.set_xticks(ticks=[])
ax.tick_params(bottom=False, left=False)
# bar label
ax.bar_label(p1, label_type='edge', padding=8)
# remove border
for s in ax.spines:
    ax.spines[s].set_visible(False)

#############################################
# milk/cream
#############################################
ax = axs[1]
ax.set_xlim([0,xmax])
ax.margins(0.015)
y = y_pos[0:len(mlk_cnt["ingr"])]
p1 = ax.barh(y, mlk_cnt["ingr"][::-1], tick_label=mlk_cnt["index"][::-1], 
                 height=2.5,  color=c2)
# ticks
ax.set_xticks(ticks=[])
ax.tick_params(bottom=False, left=False)
# bar label
ax.bar_label(p1, label_type='edge', padding=8)
# remove border
for s in ax.spines:
    ax.spines[s].set_visible(False) 

#############################################
# egg
#############################################
ax = axs[2]
ax.set_xlim([0,xmax])
ax.margins(0.015)
y = y_pos[0:len(egg_cnt["ingr"])]
p1 = ax.barh(y, egg_cnt["ingr"][::-1], tick_label=egg_cnt["index"][::-1], 
                 height=2.5,  color=c3)
# ticks
ax.set_xticks(ticks=[])
ax.tick_params(bottom=False, left=False)
# bar label
ax.bar_label(p1, label_type='edge', padding=8)
# remove border 
for s in ax.spines:
    ax.spines[s].set_visible(False)
# plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
# plt.show()
# plt.margins(0, 0)
plt.savefig('2_analysis/french_toast_bar_plot2.png', dpi=300)