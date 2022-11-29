import json
import requests
import pandas as pd
import time
import os
import shutil

url = "https://api.scryfall.com/cards/search?q=cube=vintage"

cards = []

def run_scryfall_api(url):

    apiresult = requests.get(url).json()
    data = apiresult['data']

    while 'next_page' in apiresult:
        print("getting next page")
        time.sleep(0.1)
        apiresult = requests.get(apiresult['next_page']).json()
        data += apiresult['data']
        print(len(data))

    return data

data = run_scryfall_api(url)

print(len(data))

#%%

def save_images(data, path='output/'):

    if not os.path.isdir(path):
        os.mkdir(path)
    
    def store_image(image_uri, path, name='test', num=0):
        if name+'.jpg' in os.listdir(path):
            return

        res = requests.get(image_uri, stream=True)
        if res.status_code == 200:
            with open(path+name+'.jpg', 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print(f"successfully donloaded {name}")
        else:
            print(f"couldn't download {name}")
        time.sleep(0.1)

    uris = []

    for i, card in enumerate(data):
        try:
            u = card['image_uris']['large']
            n = card['name'].replace('/', '-')
            c = str(i).rjust(3, '0')
            store_image(u, path, name=n, num=c)
        except KeyError as ke:
            if str(ke) == 'image_uris':
                for finx, face in enumerate(card['card_faces']):
                    u = face['image_uris']['large']
                    n = face['name']
                    c = str(i).rjust(3, '0') + list('ab')[finx]
                    store_image(u, path, name=n, num=c)
    
    for image_uri in uris[:2]:
        return store_image(image_uri, path)

            
res = save_images(data)
# %%
