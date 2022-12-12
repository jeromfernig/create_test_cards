import pandas as pd
import os
import shutil

def remove_owned(path="scryfall_images/", csv_path="vintage_owned.csv"):

    owned = pd.read_csv(csv_path, header=None)
    owned.columns=['no','name','wie']
    
    files = os.listdir(path)
    
    to_remove = []
    
    for card in owned['name']:
        for f in files:
            if str(f)[4:-4].lower() == card:
                to_remove.append(f)
            
    
    for rem in to_remove:
        if os.path.exists(path+rem):
            os.remove(path+rem)
            print(f"Removed {rem}")
        else:
            print("The file does not exist")
            raise Exception()
    

def delete_fullart_daretti():

    if '097_Daretti, Ingenious Iconoclast.jpg' in os.listdir('scryfall_images/'):
        os.remove('scryfall_images/097_Daretti, Ingenious Iconoclast.jpg')
        print("Removed full art Daretti")


def move_dfcs_to_subfolder(path='proxies/'):
    dfcs = [f for f in os.listdir(path) if f[3] in ['a','b']]
    if not os.path.isdir(path+'dfcs/'):
        os.mkdir(path+'dfcs/')
    for dfc in dfcs:
        shutil.move(path+dfc, path+'dfcs/'+dfc)

if __name__ == "__main__":
    # remove_owned()
    # delete_fullart_daretti()
    move_dfcs_to_subfolder()
