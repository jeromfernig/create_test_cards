# Card object
# - finds its own data via the scryfall API
# - finds its own image via the scryfall API

#%%
import requests
import json
import os
from PIL import Image
import time

#%%
class Card():

    def __init__(self, name: str, set: str = None, col_num: str = None):
        self.name = name
        self.set = set.lower() if set else None
        self.col_num = col_num
        self.data = self.get_card_data()
        try:
           self.images = self.get_card_images()
        except Exception as e:
            print("Error getting card images:", e)
            self.images = None

    def get_card_data(self):
        api_url = "https://api.scryfall.com/cards/named?fuzzy="

        url = api_url + self.name
        
        if self.set:
            url += "&set=" + self.set
        
        print("getting card data from", url)
        response = requests.get(url)
        time.sleep(0.1)
        data = json.loads(response.text)

        if self.col_num is None:
            return data
        
        # if col_num is not None, we need to find the right card in the response
        self.find_card_in_printings

        return self.find_card_in_printings(data['prints_search_uri'])
    
    def find_card_in_printings(self, prints_search_uri):
        printings = requests.get(prints_search_uri).json()
        time.sleep(0.1)
        print("searching among {} printings".format(printings['total_cards']))
        cards = printings['data']

        # filter on set
        if self.set:
            cards = [card for card in cards if card['set'] == self.set]

        for c in cards:
            print(c['collector_number'])

        # filter on collector number
        cards = [card for card in cards if card['collector_number'] == self.col_num]
        assert len(cards) == 1, "Error: found {} cards with collector number {}".format(len(cards), self.col_num)
        return cards[0]

    def get_card_images(self):
        images = []

        if "card_faces" in self.data:
            print("debug - card has multiple faces")
            for face in self.data['card_faces']:
                print("debug - looking at face", face['name'])
                img = self.cached_image(face['name']) # try to load from cache
                if img is None:
                    # download
                    print("downloading image", face['image_uris']['large'])
                    img = Image.open(requests.get(face['image_uris']['large'], stream=True).raw)
                    time.sleep(0.1)
                self.save_img(img, face['name'])
                images.append(img)
        
        else:
            # there's only one card face
            img = self.cached_image(self.data['name']) # try to load from cache
            if img is None:
                # download
                print("downloading image", self.data['image_uris']['large'])
                img = Image.open(requests.get(self.data['image_uris']['large'], stream=True).raw)
                time.sleep(0.1)
            self.save_img(img, self.data['name'])
            images.append(img)

        return images
    
    def cached_image(self, name):
        if self.set:
            name = name + "$" + self.set
        if self.col_num:
            name = name + "$" + self.col_num

        files = os.listdir("images")
        cache = [f.split(".")[0].lower() for f in files]

        if name.lower() in cache:
            idx = cache.index(name.lower())
            print("loading from cache: ", files[idx])
            return Image.open("images/" + files[idx])
        return None
        
    def save_img(self, img, filename):
        if self.set:
            filename += "$" + self.set
        if self.col_num:
            filename += "$" + self.col_num
        print("saving image under name:", filename)
        img.save("images/" + filename + ".png")


#%%

recall = Card("ancestral recall")

# %%
hm = Card("huntmaster of the fells")
# %%
vic = Card("viconia, disciple of arcana") 

# %%
br = Card("balaged recovery", set="znr")

# %%
ring = Card("the one ring", col_num="0")
# %%
