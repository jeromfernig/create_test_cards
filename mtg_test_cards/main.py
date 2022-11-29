# -*- coding: utf-8 -*-

# Imports

import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from google_images_search import GoogleImagesSearch
import xml.etree.ElementTree as ET

### USER INPUT
# setname = "cluedo" #name of the folder
# shortname = "CLUE" #like DOM for dominaria
# longname = "MtG meets Cluedo!" #official name of the set
# release_date = "2021-05-26" #YYYY-MM-DD
# csvpath = "data/csv/CLUEDO set - card list.csv"

setname = "Alchemy" #name of the folder
shortname = "ALC" #like DOM for dominaria
longname = "Alchemy: Boes en Jerom's custom set" #official name of the set
release_date = "2022-04-03" #YYYY-MM-DD
csvpath = "data/csv/custom set Boes&Jerom - Testomgeving.csv"

df = pd.read_csv(csvpath)

# Required columns: ['Version', 'Color', 'Code', 'Type',
#                    'Name', 'Mana cost', 'Subtypes', 'P/T',
#                    'Loyalty', 'Abilities', 'Art']

if setname not in os.listdir("output"):
    os.mkdir("output/{}".format(setname))
    os.mkdir("output/{}/xml".format(setname))
    os.mkdir("output/{}/images".format(setname))

#%% Functions

def text_on_img(image, text="Hello", size=40):
    "Draws text on an Image"
    fnt = ImageFont.truetype('cour.ttf', size)
    # create image
    draw = ImageDraw.Draw(image)
    # draw text
    draw.text((8, 8), text, font=fnt, fill=(0,0,0))    
    return image

def get_area(topleft, image):
    area = (topleft[0], 
            topleft[1],
            topleft[0] + image.size[0],
            topleft[1] + image.size[1])
    return area

color_path = {
    'W':'data/layout/white.jpg',
    'U':'data/layout/blue.jpg',
    'B':'data/layout/black.jpg',
    'R':'data/layout/red.jpg',
    'G':'data/layout/green.jpg',
    'M':'data/layout/gold.jpg',
    'C':'data/layout/colorless.jpg',
    'A':'data/layout/colorless.jpg',
    'nan':'data/layout/colorless.jpg'
    }

# #%% Set font sizes
LOWEST_SIZE = 8

sizes_x = {
    144:{40:5,
         36:6,
         32:7,
         28:8,
         24:9,
         20:10,
         16:13, 
         12:18,
         8:25
        },
    456:{40:18,
         36:20,
         32:23,
         28:25,
         24:31,
         20:36,
         16:44,
         12:63,
         8:88
        },
    612:{40:24,
         36:27,
         32:31,
         28:35,
         24:42,
         20:49,
         16:60,
         12:85,
         8:119
        }
    }

sizes_y = {
    40:8,
    36:9,
    32:10,
    28:12,
    24:14,
    20:16,
    16:18,
    12:24,
    8:30
    }

# #%% Functions cont. 

def get_size(text, pixels, size=40):
    #pixels = add_image.size[0]
    if len(text) > sizes_x[pixels][size] and size > LOWEST_SIZE:
        return get_size(text, pixels, size=size-4)
    else:
        return size
    
def format_abilities(text, size=40):
    newtext = str(text)
    # set max chars that fit on a single line
    max_chars_x = sizes_x[612][size]
    # replace some shorthands
    newtext = newtext.replace("~", "CARDNAME")
    newtext = newtext.replace("ETBs", "enters the battlefield")
    # split abilities into separate abilities
    newtext = newtext.split(". ")
    # for each ability, split into words (del=" ")
    words = []
    for ability in newtext:
        words.append(ability.split(" "))
        
    # based on the max chars of a line of text:
        # fit words on separate lines of text
            
    # for each word, first check whether len of that word would overflow the
    # current line. If yes, add \n and set n_chars to 0. Then, add the word to
    # the text plus a whitespace and add the chars to n_chars.
    # After each ability, add \n and set n_chars to 0
    result = ""
    lines = 0
    for ability in words:
        n_chars = 0
        for word in ability:
            assert type(word) == type("")
            if len(word) + n_chars > max_chars_x:
                result += "\n"
                lines += 1
                n_chars = 0
            result += word + " "
            n_chars += len(word) + 1
        result += "\n"
        lines += 1
            
    # check if the amount of lines exceed the vertical size
    # if yes:
        # recur function with size = size - 1
    # if no:
        # return formatted text and size
    
    if lines > sizes_y[size] and size > LOWEST_SIZE:
        return format_abilities(text, size=size-4)
    else:
        return result, size

def paste_text_img(image, path, topleft=(0,0), text="test", size=None):
    add_img = Image.open(path)
    
    if not size: size = get_size(text, add_img.size[0], size=40)
    add_img = text_on_img(add_img, text=text, size=size)
    
    area = get_area(topleft, add_img)
    image.paste(add_img, area)
    
    return image

def paste_img(image, path, topleft=(0,0)):
    add_img = Image.open(path)
    
    area = get_area(topleft, add_img)
    image.paste(add_img, area)
    
    return image

def run_google_api(name):
    print("Googling an image for card:", name)
    api_key = "AIzaSyBBXt4Ofj3SgTxZvUd5lW-S23bAPcU1vzg"
    project_cx =  "55b04e7a7bbf27a92"
    
    gis = GoogleImagesSearch(api_key, project_cx)
    
    _search_params = {
        'q':name,
        'num':1, 
        'filetype':'jpg'
        }
    
    print("debug los")
    
    gis.search(search_params=_search_params, 
               path_to_dir='data/temp/{}'.format(name), 
               width=450, height=288)
    
    print("debug los")
    
    # load the image that we just put there and save it as {name}.jpg
    filename = os.listdir("data/temp/{}".format(name))[0]
    print("debug, filename:", filename)
    
    if filename == ".jpg":
        image = Image.open("data/layout/art.jpg")
        image = text_on_img(image, text="Image Error", size=40)
        filename = "{}.jpg".format(name)
        print("debug, new filename:", filename)
        image.save("data/temp/{}.jpg".format(filename))
    
    loadpath = "data/temp/{}/{}".format(name, filename)
    savepath = "data/art/{}.jpg".format(name)
    
    img = Image.open(loadpath)
    img.save(savepath)
    
    # remove temp tiles
    #for file in os.listdir("data/temp/{}".format(name)):
    #    os.remove("data/temp/{}/{}".format(name, file))
    
    # remove temp folder
    #os.rmdir("data/temp/{}".format(name)) 

def get_art(name):
    # check if there is a file with name name. If not, run google image api
    print("debug, name in get_art:", name)
    
    try: 
        if "{}.jpg".format(name) not in os.listdir("data/art"):
            run_google_api(name)
    except:
        image = Image.open("data/layout/art.jpg")
        image = text_on_img(image, text="Image Error", size=40)
        image.save("data/art/{}.jpg".format(name))
    
    return "data/art/{}.jpg".format(name)

#%% Prepare XML

root = ET.Element("cockatrice_carddatabase", version="3")

sets = ET.SubElement(root, "sets")
mtgset = ET.SubElement(sets, "set")

# Set variables
ET.SubElement(mtgset, "name").text = shortname
ET.SubElement(mtgset, "longname").text = longname
ET.SubElement(mtgset, "settype").text = "Custom"
ET.SubElement(mtgset, "releasedate").text = release_date

# Card variables
cards = ET.SubElement(root, "cards")


#%% Run loop - for each card: save into XMl and save as image

for i in range(df.shape[0]):

    card = df.iloc[i,:]
    
    if str(card['Name']) == 'nan':
        continue
    
    ### XML SETUP
    
    # initialize xmlcard
    xmlcard = ET.SubElement(cards, "card")

    # set
    ET.SubElement(xmlcard, "set").text = shortname

    # tablerow
    typetextlower = str(card['Type']).lower()
    if 'creature' in typetextlower:
        ET.SubElement(xmlcard, "tablerow").text = "2" # creatures
    elif 'land' in typetextlower:
        ET.SubElement(xmlcard, "tablerow").text = "0" # lands
    elif 'instant' in typetextlower or 'sorcery' in typetextlower:
        ET.SubElement(xmlcard, "tablerow").text = "3" # nonpermanents
    else:
        ET.SubElement(xmlcard, "tablerow").text = "1" # nonland, noncreature permanents
        
    # token or emblem
    if "token" in typetextlower or "emblem" in typetextlower:
        ET.SubElement(xmlcard, "token").text = "1"

    ### COLOR

    image = Image.open(color_path[str(card['Color'])])

    ET.SubElement(xmlcard, "color").text = str(card['Color'])
    
    ### CODE_VERSION
    
    if str(card['Version']) == 'nan':
        codetext = str(card['Code'])
    else:
        codetext = str(card['Code']) + "_" + str(card['Version'])
            
    image = paste_text_img(image,
                           "data/layout/code_version.jpg",
                           topleft=(52, 872),
                           text=codetext)
    
    ### POWER_TOUGHNESS
    
    if str(card['P/T']) != 'nan':
        ptltext = str(card['P/T'])
        image = paste_text_img(image,
                               "data/layout/power_toughness.jpg",
                               topleft=(520, 872),
                               text=ptltext)
        
        ET.SubElement(xmlcard, "pt").text = str(card['P/T'])
        
    elif str(card['Loyalty']) != 'nan':
        ptltext = str(card['Loyalty'])
        
        image = paste_text_img(image,
                               "data/layout/power_toughness.jpg",
                               topleft=(520, 872),
                               text=ptltext)
        
        ET.SubElement(xmlcard, "loyalty").text = str(card['Loyalty'])
    
    else:
        ptltext = ""
        
        image = paste_text_img(image,
                               "data/layout/power_toughness.jpg",
                               topleft=(520, 872),
                               text=ptltext)
    
    ### NAME
    
    nametext = str(card['Name'])
    
    image = paste_text_img(image,
                           "data/layout/name.jpg",
                           topleft=(52, 56),
                           text=nametext)
    
    name = codetext + "_" + nametext
    ET.SubElement(xmlcard, "name").text = name
    
    ### MANA_COST
    
    if str(card['Mana cost']) == 'nan':
        mctext = ""
    else: 
        mctext = str(card['Mana cost'])
    
    image = paste_text_img(image, 
                           "data/layout/mana_cost.jpg",
                           topleft=(520, 56), 
                           text=mctext)

    if mctext != "":
        ET.SubElement(xmlcard, "manacost").text = str(card['Mana cost'])
    
    ### TYPE
    
    if str(card['Subtypes']) == 'nan':
        typetext = str(card['Type'])
    else: 
        typetext = str(card['Type']) + " - " + str(card['Subtypes'])
    
    image = paste_text_img(image, 
                           "data/layout/type.jpg", 
                           topleft=(52, 436),
                           text=typetext)

    ET.SubElement(xmlcard, "type").text = typetext
    
    ### ABILITIES
    
    abilitiestext, abilitiessize = format_abilities(card['Abilities'])
    
    image = paste_text_img(image,
                           "data/layout/abilities.jpg",
                           topleft=(52, 516),
                           text=abilitiestext, 
                           size=abilitiessize)

    ET.SubElement(xmlcard, "text").text = str(card['Abilities'])

    ### ART
    
    if str(card['Art']) == 'nan':
        image = paste_img(image,
                          "data/layout/art.jpg",
                          topleft=(132, 136))
    elif str(card['Art']) == 'google':
        art_path = get_art(str(card['Name']))
        image = paste_img(image, 
                          art_path,
                          topleft=(132, 136))
    else:
        arttext, artsize = format_abilities(str(card['Art']))
        image = paste_text_img(image,
                               "data/layout/art.jpg",
                               topleft=(132, 136),
                               text=arttext,
                               size=artsize)
    
    ### TEST CARD
    
    image = paste_img(image, 
                      "data/layout/test_card.jpg",
                      topleft=(52, 136))
    
    image = paste_img(image,
                      "data/layout/test_card.jpg",
                      topleft=(595, 136))

    #### SAVE
    
    filename = str(codetext) + "_" + str(nametext) + ".jpg"
    
    image.save("output/{}/images/{}".format(setname, filename))
    
tree = ET.ElementTree(root)

xmlfilename = "output/{}/xml/{}.xml".format(setname, setname)
tree.write(xmlfilename, xml_declaration=True, encoding="UTF-8")

#%%

# #%%
# text = '111\n222\n333\n444\n555\n666\n777\n888\n999\n000\n' * 4
# #text = '1234567890123456789012345678901234567890' * 4
# #text = '       10|       20|       30|       40|       50|       60|       70|       80|       90|      100|12345678901234567890'

# img = Image.open("data/layout/abilities.jpg")
# img = text_on_img(img, text=text, size=40)
# img



# #%%

# shorttext = "Flying. Whenever ~ ETBs, you may attach target equipment you control to it."
# longtext = "Flying. Whenever ~ ETBs, you may attach target equipment you control to it. This creature has trample as long as some condition is true bla bla bla. Also it should have first strike. Maybe even double strike. Bla bla bla bla"
# superlong = longtext * 10

# print(format_abilities(shorttext)[0])
# print(format_abilities(longtext)[0])
# print(format_abilities(superlong))


