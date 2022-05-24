# author: Austin Pursley
# date: 2022-03-04
# french toast recipe analysis
# anlaysis
# playing with plot styles, possibilities
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
# PLAYING WITH DIFFERENT PI CHART STYLE
###############################################################################
###############################################################################
fig, axs = plt.subplots(3, 1, figsize=(15, 15), subplot_kw=dict(aspect="equal"),
                        constrained_layout=True)
# adjust title position to not be slightly off center
mid = (fig.subplotpars.right + fig.subplotpars.left)/2 + 0.03 
fig.suptitle("French Toast Recipe Bread Types", fontsize=32, x=mid)
bread_pchart = bread_prc[0:9]
bread_other = bread_prc[9:24].sum()
# label_other = "other:\n" + labels[9:24].str.cat(sep='\n')
label_other = "other bread types"
bread_pchart[label_other] = bread_other
labels = pd.Series(bread_prc.index)
fig.text(0.7075,0.0065, (labels[9:24].str.cat(sep='\n')).replace(' bread',''), fontsize=9)

#############################################
# Pie Chart Style #1
#############################################    
pie_ax = axs[0]
# pie_ax.set_title("French Toast Recipe Bread Types (Style 1)", fontsize = 12)  
pie_chart_bread = bread_pchart.plot(kind="pie", ax=pie_ax, 
                                    # textprops={'fontsize': 9},
                                    labeldistance=1.075,
                                    # autopct='%.1f%%',
                                    # pctdistance=1.175,
                                    startangle=95, 
                                    cmap='tab20b', 
                                    ylabel='') 
# axs[2].legend(bbox_to_anchor=(1.05, 0.90))


#############################################
# Pie Chart Style #2
#############################################
pie_ax = axs[1]
# pie_ax.set_title("French Toast Recipe Bread Types (Style 2)", fontsize = 12)  
pie_chart_bread = bread_pchart.plot(kind="pie", ax=pie_ax, 
                                    # textprops={'fontsize': 9},
                                    labeldistance=None,
                                    # autopct='%.1f%%',
                                    # pctdistance=0.75,
                                    startangle=95, 
                                    cmap='tab20b', 
                                    ylabel='')
# method for having lines/arrows + box for labels
# source 1: https://stackoverflow.com/questions/55806320/how-to-add-box-and-label-to-pie-graph-exactly-as-shown-in-figure-below
# source 2: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html      
bread_pchart_str = bread_pchart.map(lambda x: '{0:.1f}'.format(x))
bread_pchart_labels = bread_pchart_str + "% " + bread_pchart.index  
wedges = pie_chart_bread.patches.copy() # had to dig into docs to find this...
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"), zorder=0, va="center")
for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    pie_ax.annotate(bread_pchart_labels[i], xy=(x, y), xytext=(1.1*np.sign(x), 1.2*y),
                horizontalalignment=horizontalalignment, **kw)

#############################################
# Pie Chart Style #3
#############################################    
pie_ax = axs[2]
# pie_ax.set_title("French Toast Recipe Bread Types (Style 3)", fontsize = 12)  
pie_chart_bread = bread_pchart.plot(kind="pie", ax=pie_ax, 
                                    # textprops={'fontsize': 9},
                                    labeldistance=None,
                                    autopct='%.1f%%',
                                    pctdistance=1.175,
                                    startangle=95, 
                                    cmap='tab20b', 
                                    ylabel='') 
pie_ax.legend(bbox_to_anchor=(1.03, 0.93))
plt.savefig('2_analysis/french_toast_pie_plot_exp.png', 
            bbox_inches='tight', dpi=300)