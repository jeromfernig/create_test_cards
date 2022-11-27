# -*- coding: utf-8 -*-

import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

### USER INPUT
setname = "cluedo" #name of the folder
shortname = "CLUE" #like DOM for dominaria
longname = "MtG meets Cluedo!" #official name of the set
release_date = "2021-05-26" #YYYY-MM-DD
csvpath = "data/csv/CLUEDO set - card list.csv"

df = pd.read_csv(csvpath)

#%%

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

for i in range(df.shape[0]):

    card = df.iloc[i,:]
    xmlcard = ET.SubElement(cards, "card")

    # name
    name = str(card['Code']) + "_" + str(card['Name'])
    ET.SubElement(xmlcard, "name").text = name

    # set
    ET.SubElement(xmlcard, "set").text = shortname

    # color
    ET.SubElement(xmlcard, "color").text = str(card['Color'])

    # mana cost
    if str(card['Mana cost']) != 'nan':
        ET.SubElement(xmlcard, "manacost").text = str(card['Mana cost'])

    # type
    ET.SubElement(xmlcard, "type").text = str(card['Type']) + " - " + str(card['Subtypes'])

    # power / toughness
    if str(card['P/T']) != 'nan':
        ET.SubElement(xmlcard, "pt").text = str(card['P/T'])

    # loyalty
    if str(card['Loyalty']) != 'nan':
        ET.SubElement(xmlcard, "loyalty").text = str(card['Loyalty'])    

    # tablerow
    typetext = str(card['Type']).lower()
    if 'creature' in typetext:
        ET.SubElement(xmlcard, "tablerow").text = "2" # creatures
    elif 'land' in typetext:
        ET.SubElement(xmlcard, "tablerow").text = "0" # lands
    elif 'instant' in typetext or 'sorcery' in typetext:
        ET.SubElement(xmlcard, "tablerow").text = "3" # nonpermanents
    else:
        ET.SubElement(xmlcard, "tablerow").text = "1" # nonland, noncreature permanents

    # abilities
    ET.SubElement(xmlcard, "text").text = str(card['Abilities'])

    # token
    if "token" in typetext or "emblem" in typetext:
        ET.SubElement(xmlcard, "token").text = "1"


tree = ET.ElementTree(root)

tree.write("test.xml", xml_declaration=True, encoding="UTF-8")




# #%%
# xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
# with open("test.xml", "w") as f:
#     f.write(xmlstr)
# #%%



#     0 → lands
#     1 → non-creature, non-land permanents (like Planeswalkers, Enchantments, and Artifacts)
#     2 → creatures (this includes all cards that have the "creature" type like "Enchantment Creature")
#     3 → non-permanent cards (like Instants and Sorceries)









# <?xml version="1.0" encoding="UTF-8"?>
# <cockatrice_carddatabase version="3">
# 	<sets>
# 		<set>
# 			<name>CLUE</name>
# 			<longname>MtG meets Cluedo</longname>
# 			<settype>Custom</settype>
# 			<releasedate>2021-05-26</releasedate>
# 		</set>
# 	</sets>
# 	<cards>
# 		<card>
# 			<name>Hawk</name>
# 			<set picURL="C:/Users/User/Dropbox/Repos/mtg_test_cards/output/cluedo/CW01_Hawk.jpg">CLUE</set>
# 			<color>W</color>
# 			<manacost>W</manacost>
# 			<cmc>1</cmc>
# 			<type>Creature - Bird</type>
# 			<pt>1/1</pt>
# 			<tablerow>2</tablerow>
# 			<text></text>
# 		</card>
# 	</cards>
# </cockatrice_carddatabase>