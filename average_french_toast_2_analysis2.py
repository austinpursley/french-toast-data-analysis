# author: Austin Pursley
# date: 2022-03-04
# french toast recipe analysis
# pie plots

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pprint

ft_recipes = pd.read_csv("french_toast_recipes_cleaned_final.csv", index_col=False, na_filter = False) 

###############################################################################
###############################################################################
# PI CHART DIFFERENT INGREDIENTS
###############################################################################
###############################################################################
fig, axs = plt.subplots(3, 1, figsize=(15, 15), subplot_kw=dict(aspect="equal"),
                        constrained_layout=True)
# adjust title position to not be slightly off center
mid = (fig.subplotpars.right + fig.subplotpars.left)/2 + 0.03 
fig.suptitle("French Toast Recipes, Essential Ingredient Types", fontsize=32, x=mid)
#############################################
# Pie Chart Bread
#############################################
pie_ax = axs[0]
bread = ft_recipes.loc[ft_recipes["category"] == "bread"]
bread = bread.sort_values(by=['ingr'])
bread_vc = bread[["title", "category"]].value_counts()
bread_grp = bread.groupby(['title','category'])['ingr'].apply(' and '.join).reset_index()
bread_cnt = bread_grp["ingr"].value_counts().reset_index()
bread_prc = bread_grp["ingr"].value_counts(normalize=True)*100
m = 12
e = 24
# set up labels and legend labels
bread_prc = bread_prc.reset_index()
bread_prc_str = bread_prc["ingr"].map(lambda x: '{0:.1f}'.format(x)) 
bread_prc["labels"] = bread_prc_str + "% " + bread_prc["index"] 
bread_prc["legend"] = bread_prc.loc[:, "labels"]
bread_maj = bread_prc[0:m]
bread_maj["legend"] = ""
bread_other = bread_prc[m:e]
bread_other["labels"]  = ""
bread_pchart = bread_maj.append(bread_other)
bread_pchart = bread_pchart.set_index("index")
# colors
c1 = plt.cm.get_cmap('tab20b', len(bread_maj["legend"]))
# c2 = plt.cm.get_cmap('Reds_r', len(bread_pchart["legend"]))
c3 = plt.cm.get_cmap('tab20', len(bread_other["legend"]))
colors = c1.colors
# colors2 = c2(np.linspace(0.2, 0.8, 13)) #.. and linspace for continuous ones
colors3 = c3.colors
newcolors = np.concatenate((colors[0:m], colors3[0:(e-m)]))
newcmp = mcolors.ListedColormap(newcolors)
# pie chart
pie_ax.pie(bread_pchart["ingr"], labels=bread_pchart["labels"], 
            labeldistance=1.1, startangle=20, 
            colors=newcolors,
            wedgeprops={'linewidth': 0.5, 'linestyle': 'solid',
                         'edgecolor' : 'black'})
# legend
wedges = pie_ax.patches
labels = list(bread_pchart["legend"])
wedges = wedges[m:e]
labels = labels[m:e] 
pie_ax.legend(labels = labels[::-1], handles = wedges[::-1], bbox_to_anchor=(1.0, 0.85))

#############################################
# Pie Chart Milk/Cream
############################################# 
pie_ax = axs[1]
mlk = ft_recipes.loc[ft_recipes["category"] == "milkcream"]
mlk = mlk.sort_values(by=['ingr'])
mlk_vc = mlk[["title", "category"]].value_counts()
mlk_grp = mlk.groupby(['title','category'])['ingr'].apply(' and '.join).reset_index()
mlk_cnt = mlk_grp["ingr"].value_counts().reset_index()
mlk_prc = mlk_grp["ingr"].value_counts(normalize=True)*100
m = 8
e = 13
# set up labels and legend labels
mlk_prc = mlk_prc.reset_index()
mlk_prc_str = mlk_prc["ingr"].map(lambda x: '{0:.1f}'.format(x)) 
mlk_prc["labels"] = mlk_prc_str + "% " + mlk_prc["index"] 
mlk_prc["legend"] = mlk_prc.loc[:, "labels"]
mlk_maj = mlk_prc[0:m]
mlk_maj["legend"] = ""
mlk_other = mlk_prc[m:e]
mlk_other["labels"]  = ""
mlk_pchart = mlk_maj.append(mlk_other)
mlk_pchart = mlk_pchart.set_index("index")
# colors
c1 = plt.cm.get_cmap('tab20b', len(mlk_prc["legend"]))
colors = c1.colors
# pie chart
pie_ax.pie(mlk_pchart["ingr"], labels=mlk_pchart["labels"], 
            labeldistance=1.1, startangle=20, 
            colors=colors,
            wedgeprops={'linewidth': 0.5, 'linestyle': 'solid',
                         'edgecolor' : 'black'})
# legend
wedges = pie_ax.patches
labels = list(mlk_pchart["legend"])
wedges = wedges[m:e]
labels = labels[m:e]
pie_ax.legend(labels = labels[::-1], handles = wedges[::-1], bbox_to_anchor=(1, 0.8))

#############################################
# Pie Chart Eggs
############################################# 
pie_ax = axs[2]
eggs = ft_recipes.loc[ft_recipes["category"] == "eggs"]
eggs = eggs.sort_values(by=['ingr'])
eggs_vc = eggs[["title", "category"]].value_counts()
eggs_grp = eggs.groupby(['title','category'])['ingr'].apply(' and '.join).reset_index()
eggs_cnt = eggs_grp["ingr"].value_counts().reset_index()
eggs_prc = eggs_grp["ingr"].value_counts(normalize=True)*100
# set up labels and legend labels
eggs_prc = eggs_prc.reset_index()
eggs_prc_str = eggs_prc["ingr"].map(lambda x: '{0:.1f}'.format(x)) 
eggs_prc["labels"] = eggs_prc_str + "% " + eggs_prc["index"] 
eggs_prc["legend"] = eggs_prc.loc[:, "labels"]
# colors
colors = c1(np.arange(0,15,3, dtype=int))
# pie chart
pie_ax.pie(eggs_prc["ingr"], labels=eggs_prc["labels"], 
            labeldistance=1.1, startangle=20, 
            colors=colors,
            wedgeprops={'linewidth': 0.5, 'linestyle': 'solid',
                         'edgecolor' : 'black'})

plt.savefig('2_analysis/plot1_french_toast_recipes_essential_ingr_break_downs_pie_charts.png', dpi=300)