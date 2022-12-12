import os
from mtg_test_cards.main import tex

for file in os.listdir("output/"):
    print(file)
    
#%% 

image = Image.open(f"output/{file}")
image.show()

