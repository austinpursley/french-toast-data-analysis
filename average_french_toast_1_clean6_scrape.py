import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import glob
import os

ft_recipes = pd.read_csv("french_toast_recipes_cleaned_final.csv", index_col=False, na_filter = False)
scrapped_csv = pd.read_csv("recipe_data_scraped/ft_recipes_ingr_instr-master.csv", index_col=False, na_filter = False)
titles = set(ft_recipes["title"].unique())
scraped_current = set(scrapped_csv["title"].unique())
# check on which json files we still need
json_fs = glob.glob("recipe_data_scraped/*.json")
txt_fs = glob.glob("recipe_data_scraped/*.txt")
# scraped_current = json_fs + txt_fs
# scraped_current= set([os.path.splitext(os.path.basename(d))[0] for d in scraped_current])
added = list(sorted(scraped_current - titles))
missing = list(sorted(titles - scraped_current))

ft_scraped_data = pd.DataFrame(columns=["ingredients", "instructions"])
ft_scraped_data.index.name = "title"

for title in missing:
    print(title)
    url = requests.get('https://www.allrecipes.com/recipe/' + title + '/')
    soup = BeautifulSoup(url.content, 'html.parser')
    script_f = soup.find('script', string=re.compile("recipeIngredient"))
    if script_f:
        script = script_f.string
        data =  json.loads(script)[1]
        json_object = json.dumps(data, indent = 4)
        with open("recipe_data_scraped/" + title + ".json", "w") as outfile:
            outfile.write(json_object)
        # ft_scraped_data["ingredients"] = 
        ft_scraped_data.at[title, 'ingredients'] = '\n'.join(data["recipeIngredient"])
        instructions = data['recipeInstructions']
        ft_scraped_data.at[title, 'instructions'] = '\n'.join([s["text"] for s in instructions])
    else:
        with open('recipe_data_scraped/' +  os.path.basename(title) + ".txt", "w") as f:
            f.write(url.text)
        ingr = [i.contents[0] for i in soup.find_all(itemprop="recipeIngredient") if i.contents]
        instr = [i.contents[0] for i in soup.find_all(class_ = r"recipe-directions__list--item") if i.contents]
        ft_scraped_data.at[title, 'ingredients'] = '\n'.join(ingr)
        ft_scraped_data.at[title, 'instructions'] = '\n'.join(instr)
        # continue

ft_scraped_data.to_csv("recipe_data_scraped/ft_recipes_ingr_instr-4.csv")