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

bread = ft_recipes.loc[ft_recipes["category"] == "bread"]
bread = bread.sort_values(by=['ingr'])
bread_vc = bread[["title", "category"]].value_counts()
bread_grp = bread.groupby(['title','category'])['ingr'].apply(' and '.join).reset_index()
bread_cnt = bread_grp["ingr"].value_counts().reset_index()
bsz = len(bread_cnt["ingr"])

###############################################################################
###############################################################################
# BAR CHARTS EXPERIMENTS
###############################################################################
###############################################################################
fig, axs = plt.subplots(2, 1, figsize=(10, 20),
                        constrained_layout=True)
# adjust title position to not be slightly off center
mid = (fig.subplotpars.right + fig.subplotpars.left)/2 - 0.06
fig.suptitle("Bar Chart Experimentation", fontsize=32, x=mid)

colors = plt.cm.get_cmap('tab20b', len(bread_cnt["ingr"])).colors
c1 = colors[0]
c2 = colors[5]
c3 = colors[9]

#############################################
# bar chart style 2
#############################################
axs[0].barh(bread_cnt["index"][::-1], bread_cnt["ingr"][::-1], color=c1)
axs[0].grid(color='#95a5a6', linestyle='-', linewidth=1.5, axis='x')
axs[0].set_axisbelow(True)
#############################################
# pew style bar chart
#############################################
y_pos = np.linspace(0,len(bread_cnt['ingr'])*2.0,len(bread_cnt['ingr']))  
p1 = axs[1].barh(y_pos, bread_cnt["ingr"][::-1], tick_label=bread_cnt["index"][::-1], 
                 height=1.0,  color=c2)
# ticks
axs[1].set_xticks(ticks=[])
axs[1].tick_params(bottom=False, left=False,labelsize=12)
# bar label
axs[1].bar_label(p1, label_type='edge', padding=2, fontsize=12)
# remove border
for s in axs[1].spines:
    axs[1].spines[s].set_visible(False)

plt.savefig('2_analysis/plot3_bread_types_bar_chart_style_compare.png', dpi=300)