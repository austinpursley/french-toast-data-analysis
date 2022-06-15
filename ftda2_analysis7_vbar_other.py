# author: Austin Pursley
# date: 2022-05-23
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

#############################################
# other
#############################################
crit = ((ft_recipes["category"] != "eggs") & (ft_recipes["category"] != "bread") 
        & (ft_recipes["category"] != "milkcream"))
other = ft_recipes.loc[crit]


ocats = ["flavor", "sugar", "syrup", "fruit", "spread", "dairy", "nut", "cereal"]
ocats_cnt = []
hratios = []
for c, i in zip(ocats, range(len(ocats))):
    cat = other.loc[other["category"] == c]
    cat_cnt = cat["ingr"].value_counts().reset_index()
    ocats_cnt.append(cat_cnt)
    hratios.append(len(cat_cnt["ingr"]))


fig, axs = plt.subplots(len(ocats), 1, gridspec_kw={'height_ratios': hratios},
                        figsize=(9,20), constrained_layout=True)
mid = (fig.subplotpars.right + fig.subplotpars.left)/2
fig.suptitle("allrecipes.com French Toast Recipes \n 'Other' Ingredient Counts", fontsize=18, x=mid)
# colors
colors = plt.cm.get_cmap('tab20b', 40).colors

N = max([len(i) for i in ocats_cnt])
y_pos = np.linspace(1,N*3.0,N)
xmax=70

for occ, i in zip(ocats_cnt, range(len(ocats_cnt))):
    ax = axs[i]
    ax.set_xlim([0,xmax])
    ax.margins(0.015)
    y = y_pos[0:len(occ["ingr"])]
    x = occ["ingr"][::-1]
    p1 = ax.barh(y, x, 
               tick_label=occ["index"][::-1], height=2.5, color=colors[i+i*3])
    # ticks
    ax.set_xticks(ticks=[])
    ax.tick_params(bottom=False, left=False)
    # bar label
    ax.bar_label(p1, label_type='edge', padding=8)
    # remove border
    for s in ax.spines:
        ax.spines[s].set_visible(False)
        
plt.savefig('2_analysis/french_toast_bar_plot_other.png', dpi=300)