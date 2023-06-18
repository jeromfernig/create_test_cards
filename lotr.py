#%%
import requests
import time
from PIL import Image
import math

card_size = (750, 1050)

def get_lotr_cards():
    cards_in_set = 261
    url = "https://api.scryfall.com/cards/search?q=set=ltr&unique=prints&order=set"
       
    apiresult = requests.get(url).json()
    time.sleep(0.1)
    data = apiresult['data']

    while 'next_page' in apiresult:
        print("getting next page")
        apiresult = requests.get(apiresult['next_page']).json()
        time.sleep(0.1)
        data += apiresult['data']
        print(len(data))

    main_set = [card for card in data if int(card['collector_number']) <= cards_in_set]

    land_nums = list(range(272, 282))

    lands = [card for card in data if int(card['collector_number']) in land_nums]

    return main_set + lands

def get_img(uri):
    try:
        print("getting image", uri)
        # load image from bytes object
        img = Image.open(requests.get(uri, stream=True).raw)
        time.sleep(0.1)
        return img
    except:
        print("Error getting image")
        return None
    
def fix_corner(im):
    crop_pix = 20

    # Get the background color
    bg_color = im.getpixel((300, 5))
    bg_width, bg_height = im.size
    background = Image.new('RGB', (bg_width, bg_height), bg_color)

    new_width, new_height = im.size

    # crop original image
    im = im.crop((crop_pix, crop_pix, new_width-crop_pix, new_height-crop_pix))

    # paste original image onto background
    background.paste(im, (crop_pix, crop_pix))

    return background

data = get_lotr_cards()

# # pick 8 cards for now
# data = data[:8]

# change basic lands rarity to land
for card in data: 
    if card['name'] in ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']:
        card['rarity'] = 'land'	

# extract images
n_rarity = {'common': 2, 'uncommon': 2, 'rare': 1, 'mythic': 1, 'land': 12}
images = []

for card in data:
    img = get_img(card['image_uris']['large'])
    for _ in range(n_rarity[card['rarity']]):
        images.append(img)

# # pick 8 images for now
# images = images[:8]

v_margin, h_margin = 250, 180
v_card, h_card = card_size

# resize images
images = [img.resize((v_card, h_card)) for img in images]

# fix corners
images = [fix_corner(img) for img in images]

### Create pdfs

pdf_list = []
n_pages = int(math.ceil(len(images)/8))

pdf_coordinates = [
    (v_margin, h_margin),
    (v_margin + v_card, h_margin),
    (v_margin + 2*v_card, h_margin),
    (v_margin + 3*v_card, h_margin),
    (v_margin, h_margin + h_card),
    (v_margin + v_card, h_margin + h_card),
    (v_margin + 2*v_card, h_margin + h_card),
    (v_margin + 3*v_card, h_margin + h_card),
]

for i in range(n_pages):
    # new A4 page in landscape mode
    pdf = Image.new('RGB', (3507, 2480), (255, 255, 255))
    

    # paste the images into the image
    for img, coord in zip(images, pdf_coordinates):
        pdf.paste(img, coord)

    # rotate the pdf
    pdf = pdf.rotate(90, expand=True)

    pdf_list.append(pdf)

    # remove first 8 items from images
    images = images[8:]

# save the pdf
pdf_list[0].save('lotr_test.pdf', resolution=300, save_all=True, append_images=pdf_list[1:])

# %%
