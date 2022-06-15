# author: Austin Pursley
# date: 2022-01-15
# french toast recipe analysis
# cleaning data
# part 1: break down ingredients into unique words, numbers, units
# prep for next step, manually going through unique values etc to write keys
import pandas as pd

df = pd.read_csv("french_toast_recipes_0_post_cut.csv", index_col=False)
# df = pd.read_csv("french_toast_recipes_0_post_cut_no_milk.csv", index_col=False)
df = df.apply(lambda x: x.str.split('\n').explode())

df["Ingredients Numbers"] = df["Ingredients"].str.replace(r'[^0-9\\\s\n\/.]','', regex=True)
df["Ingredients Numbers"] = df["Ingredients Numbers"].str.replace(r" +", r" ", regex=True)
# ingredient lists with only words (remove numbers, other characters)
df["Ingredients Words"] = df["Ingredients"].str.replace(r'[\(\)-]',' ', regex=True)
df["Ingredients Words"] = df["Ingredients Words"].str.replace(r'[^a-zA-Z\s\n]','', regex=True)
df["Ingredients Words"] = df["Ingredients Words"].str.replace(r" +", r" ", regex=True)

# define dataframe to for clean + simplified ingredients
ingr_cln = pd.DataFrame(columns=["title", "ingr_full", "ingr_nums", "ingr_cnt", "ingr_qnt", "ingr_units","ingr_num_total", "ingr_wrds"])
# ingredients_full = []
# [[ingredients_full.append(i) for i in i_list] for i_list in df["Ingredients"].str.split('\n')]
# ingredients_nums = []
# [[ingredients_nums.append(i) for i in i_list] for i_list in df["Ingredients Numbers"].str.split('\n')]
# ingredients_words = []
# [[ingredients_words.append(i) for i in i_list] for i_list in df["Ingredients Words"].str.split('\n')]
# writing best guesses for now
ingr_cln["title"] = df["Title"]
ingr_cln["ingr_full"] = df["Ingredients"]
ingr_cln["ingr_full"] = ingr_cln["ingr_full"].str.strip()
ingr_cln["ingr_wrds"] = df["Ingredients Words"] # for now, col still contains units
ingr_cln["ingr_wrds"] = ingr_cln["ingr_wrds"].str.strip()
ingr_cln["ingr_nums"] = df["Ingredients Numbers"]
ingr_cln["ingr_nums"] = ingr_cln["ingr_nums"].str.strip()
ingr_cln["ingr_units"] = ingr_cln["ingr_wrds"].str.split(' ').str[0]
ingr_cln["ingr_units"] = ingr_cln["ingr_units"].str.strip()
ingr_cln.to_csv("1_ingr_clean/0ingredients_clean_track.csv", index=False)
# ingr_cln["ingr_full"] = ingredients_full
# ingr_cln["ingr_full"] = ingr_cln["ingr_full"].str.strip()
# ingr_cln["ingr_wrds"] = ingredients_words # for now, col still contains units
# ingr_cln["ingr_wrds"] = ingr_cln["ingr_wrds"].str.strip()
# ingr_cln["ingr_nums"] = ingredients_nums
# ingr_cln["ingr_nums"] = ingr_cln["ingr_nums"].str.strip()
# ingr_cln["ingr_units"] = ingr_cln["ingr_wrds"].str.split(' ').str[0]
# ingr_cln["ingr_units"] = ingr_cln["ingr_units"].str.strip()
ingr_cln.to_csv("1_ingr_clean/0ingredients_clean_track.csv", index=False)

# want keys to find and/or replace words, numbers, units within ingredients
# in this step, we'll write "drafts" with guesses to start out with
# then manually manually edit and save final versions of the keys

# writing draft for a units key
units_key_dft = pd.DataFrame(columns=["ingr_units", "Replacement", "Original Example"])
units_key_dft["ingr_units"] = (ingr_cln["ingr_units"]).unique()
units_key_dft["ingr_units_replace"]  = ""
units_key_dft["Original Example"]  = ""
for n in units_key_dft["ingr_units"]:
    test = units_key_dft.loc[units_key_dft["ingr_units"] == n, "Original Example"] 
    units_key_dft.loc[units_key_dft["ingr_units"] == n, "Original Example"] = ingr_cln.loc[ingr_cln["ingr_units"] == n, ["ingr_full"]].iloc[0].item()
units_key_dft.to_csv("1_ingr_clean/1units_key_draft.csv", index=False)

# writing draft for a numbers key
num_key_dft = pd.DataFrame(columns=["ingr_nums", "ingr_nums_replace", "ingr_cnt_replace", "ingr_qnt_replace", "Original Example"])
num_key_dft["ingr_nums"] = ingr_cln.sort_values(by='ingr_nums')['ingr_nums'].unique()
num_key_dft["ingr_nums_replace"]  = ""
num_key_dft["Replacement-ingr_cnt"]  = ""
num_key_dft["Replacement-ingr_qnt"]  = ""
num_key_dft["Original Example"]  = ""
for n in num_key_dft["ingr_nums"]:
    test = num_key_dft.loc[num_key_dft["ingr_nums"] == n, "Original Example"] 
    num_key_dft.loc[num_key_dft["ingr_nums"] == n, "Original Example"] = ingr_cln.loc[ingr_cln["ingr_nums"] == n, ["ingr_full"]].iloc[0].item()
num_key_dft["ingr_nums_replace"] = num_key_dft["ingr_nums"]
num_key_dft["ingr_nums_replace"] = num_key_dft["ingr_nums_replace"].str.replace(r"\s?\\2122\s?", " ", regex=True)
num_key_dft["ingr_nums_replace"] = num_key_dft["ingr_nums_replace"].str.replace(r"\s?\\2019\s?", " ", regex=True)
num_key_dft["ingr_nums_replace"] = num_key_dft["ingr_nums_replace"].str.replace(r"\s?\.\s?", " ", regex=True)    
num_key_dft["ingr_nums_replace"] = num_key_dft["ingr_nums_replace"].str.replace(r"\s?\\\s?", " ", regex=True) 
num_key_dft["ingr_nums_replace"] = num_key_dft["ingr_nums_replace"].str.replace(r" +", r" ", regex=True)
num_key_dft["ingr_nums_replace"] = num_key_dft["ingr_nums_replace"].str.replace(r"^ $", r"", regex=True)
num_key_dft["ingr_cnt_replace"] = num_key_dft["ingr_nums_replace"].str.split(" ").str[0]
num_key_dft["ingr_qnt_replace"] = num_key_dft["ingr_nums_replace"].str.split(" ").str[1]
num_key_dft.to_csv("1_ingr_clean/1nums_key_draft.csv", index=False)

# write CSV files for unique words
# go through these to pick out words to cut out, etc.
fn = "1_ingr_clean/1ingredients_only_words_unique.csv"
pd.DataFrame(ingr_cln.sort_values(by='ingr_wrds')['ingr_wrds'].unique(), columns=["ingr_wrds"]).to_csv(fn, index=False)
unique_words = ingr_cln["ingr_wrds"].unique()
unique_words.sort()
df_uw = pd.DataFrame(unique_words, columns=["unq_wrds"])
df_uw.to_csv("1_ingr_clean/1ingredients_only_words_seperated_unique.csv", index=False)
