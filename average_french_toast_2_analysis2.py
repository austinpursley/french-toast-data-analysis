# author: Austin Pursley
# date: 2022-03-04
# french toast recipe analysis
# plots

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pprint

ft_recipes = pd.read_csv("french_toast_recipes_cleaned_final.csv", index_col=False, na_filter = False) 


bread = ft_recipes.loc[ft_recipes["category"] == "bread"]
bread_cnt = bread["ingr"].value_counts()
bread_prc = bread["ingr"].value_counts(normalize=True)*100


eggs = ft_recipes.loc[ft_recipes["category"] == "eggs"]
eggs_cnt = eggs["ingr"].value_counts()
eggs_prc = eggs["ingr"].value_counts(normalize=True)*100

milkcream = ft_recipes.loc[ft_recipes["category"] == "milkcream"]
milkcream_cnt = milkcream["ingr"].value_counts()
milkcream_prc = milkcream["ingr"].value_counts(normalize=True)*100

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
bread_pchart = bread_prc[0:11].reset_index()
bread_pchart["legend"] = ""
bread_other = bread_prc[11:24].reset_index()
bread_other["legend"] = bread_other["index"].copy()
bread_other["index"]  = ""
bread_pchart = bread_pchart.append(bread_other)
bread_pchart = bread_pchart.rename(columns = {'index':'labels'})
bread_pchart = bread_pchart.set_index("labels")
# combing cmaps
c1 = plt.cm.get_cmap('tab20b', len(bread_pchart["legend"]))
c2 = plt.cm.get_cmap('Reds', len(bread_pchart["legend"]))
newcolors = c1(np.arange(1,12,1, dtype=int)) #note how use arange for discrete cmaps...
newcolors2 = c2(np.linspace(0.2, 0.8, 13)) #.. and linspace for continuous ones
newcolors = np.concatenate((newcolors, newcolors2))
grays = mcolors.ListedColormap(newcolors2)
newcmp = mcolors.ListedColormap(newcolors)

bread_pchart.plot(x="labels", y="ingr", kind="pie", ax=pie_ax, 
                                    labeldistance=1.1,
                                    startangle=20, 
                                    cmap=newcmp, 
                                    ylabel='', legend=False,
                                    wedgeprops={'linewidth': 0.5, 'linestyle': 'solid',
                                                'edgecolor' : 'black'}) 
pp = pprint.PrettyPrinter()
# pp.pprint(pie_ax.__dict__)
wedges = pie_ax.patches
# labels = [l.get_text() for l in pie_ax.texts]
labels = list(bread_pchart["legend"])
wedges = wedges[11:24]
labels = labels[11:24]
pie_ax.legend(labels = labels[::-1], handles = wedges[::-1], bbox_to_anchor=(1.0, 0.97))

#############################################
# Pie Chart Milk/Cream
############################################# 
pie_ax = axs[1]
mlk_pchart = milkcream_prc[0:6].reset_index()
mlk_pchart["legend"] = ""
mlk_other = milkcream_prc[6:13].reset_index()
mlk_other["legend"] = mlk_other["index"].copy()
mlk_other["index"] = ""
mlk_pchart = mlk_pchart.append(mlk_other)
mlk_pchart = mlk_pchart.rename(columns = {'index':'labels'})
mlk_pchart = mlk_pchart.set_index("labels")
pie_chart_mlk = mlk_pchart.plot(x="labels", y="ingr", kind="pie", ax=pie_ax, 
                                    labeldistance=1.075,
                                    startangle=20, 
                                    cmap='tab20b', 
                                    ylabel='', legend=False,
                                    wedgeprops={'linewidth': 0.5, 'linestyle': 'solid',
                                                'edgecolor' : 'black'}) 
wedges = pie_ax.patches
# labels = [l.get_text() for l in pie_ax.texts]
labels = list(mlk_pchart["legend"])
wedges = wedges[6:13]
labels = labels[6:13]
pie_ax.legend(labels = labels[::-1], handles = wedges[::-1], bbox_to_anchor=(1, 0.9))

#############################################
# Pie Chart Eggs
############################################# 
pie_ax = axs[2]
pie_chart_eggs = eggs_prc.plot(kind="pie", ax=pie_ax, 
                                    labeldistance=1.075,
                                    startangle=20, 
                                    cmap='tab20b', 
                                    ylabel='',
                                    wedgeprops={'linewidth': 0.5, 'linestyle': 'solid',
                                                'edgecolor' : 'black'}) 
# pie_ax.legend(bbox_to_anchor=(1.15, 0.60))

# plt.show()
plt.savefig('2_analysis/plot1_french_toast_recipes_essential_ingr_break_downs_pie_charts.png', dpi=300)

# Be cool to visualize essential ingredients for all recipes in one chart
# matrix. each row represents a recipe. 
# first column is bread, second column is eggs, third is milk/cream
# color coded to tell you which type it is.

# bar charts for three essential ingredients

# basic stats: number of recipes, etc.

# charts for other ingredients

# visualize all the types of ingredients

# reatios e.g. egg to bread to milkcream ratios

# "average" french toast recipe (if you dare)

# top ingredients mentioned, etc.