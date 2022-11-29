# -*- coding: utf-8 -*-
"""
Card class

Created on Sun Nov 27 12:53:34 2022

@author: Jerom Fernig
"""
from typing import Optional
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont

layout_paths = {
    'gold': "layout/gold.jpg"
    }

LOWEST_SIZE = 8

class ScalerCard(BaseModel):
        
    cardid: str
    copies: int
    name: str
    cost: str
    requirement: Optional[str]
    types: str
    subtypes: Optional[str]
    play: Optional[str]
    passive: Optional[str]
    expansion: str
    comment: Optional[str] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    
    def text_on_img(self, image, text="Hello", size=40):
        "Draws text on an Image"
        fnt = ImageFont.truetype('cour.ttf', size)
        # create image
        draw = ImageDraw.Draw(image)
        # draw text
        draw.text((8, 8), text, font=fnt, fill=(0,0,0))    
        return image
    
    def get_area(self, topleft, image=None):
        if image is None:
            image = self.image
        
        area = (topleft[0], 
                topleft[1],
                topleft[0] + image.size[0],
                topleft[1] + image.size[1])
        return area
    
    def get_size(self, text, pixels, size=40):
        #pixels = add_image.size[0]
        if len(text) > sizes_x[pixels][size] and size > LOWEST_SIZE:
            return self.get_size(text, pixels, size=size-4)
        else:
            return size

    
#%% Test

d = {"cardid": "01test",
    "copies": 1,
    "name": "test_name",
    "cost": "1money",
    # "requirement": str,
    "types": "building",
    # "subtypes": str,
    # "play": str,
    # "passive": str,
    "expansion": "test_exp",
    # "comment": str,
    }

sc = ScalerCard(**d)

print(sc)
