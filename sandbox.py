#%%
import pandas as pd
owned = pd.read_csv("vintage_owned.csv", header=None)
owned.columns=['no','name','wie']
#%%
import os
files = os.listdir("output/")

to_remove = []

for card in owned['name']:
    for f in files:
        if str(f)[:-4].lower() == card:
            to_remove.append(f)
        
# %%
for rem in to_remove:
    if os.path.exists("output/"+rem):
        os.remove("output/"+rem)
        print(f"Removed {rem}")
    else:
        print("The file does not exist")
# %%
