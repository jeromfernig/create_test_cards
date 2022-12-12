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

if __name__ == "__main__":
    data = run_scryfall_api(url)

    print(len(data))

#%%

def save_images(data, path='scryfall_images/'):

    if not os.path.isdir(path):
        os.mkdir(path)
    
    def store_image(image_uri, path, name='test', num='000', i='0'):
        if num+'_'+name+'.jpg' in os.listdir(path):
            print(f"{i} - {name} was cached")
            return

        res = requests.get(image_uri, stream=True)
        if res.status_code == 200:
            with open(path+num+'_'+name+'.jpg', 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print(f"{i} - successfully downloaded {name}")
        else:
            print(f"{i} - couldn't download {name}")
        time.sleep(0.1)

    uris = []

    for i, card in enumerate(data):
        try:
            u = card['image_uris']['large']
            n = card['name'].replace('/', '-')
            c = str(i).rjust(3, '0')
            store_image(u, path, name=n, num=c, i=i)
        except KeyError as ke:
            print(f"Card {card['name']} should have multiple faces")

            for finx, face in enumerate(card['card_faces']):
                u = face['image_uris']['large']
                n = face['name']
                c = str(i).rjust(3, '0') + list('ab')[finx]
                store_image(u, path, name=n, num=c, i=i)
    
    for image_uri in uris[:2]:
        return store_image(image_uri, path)

if __name__ == "__main__":
    save_images(data)

