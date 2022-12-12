from PIL import Image
import os

# Parameters
crop_pix = 25
margin_pix = 36
mpc_width, mpc_height = 822, 1122
logo_size = (120, 120)
logo_loc = (90, 500)

def proxify_image(path_to_image=None, image=None, logo=True):

    if path_to_image is None and image is None:
        raise ValueError("Must provide either path_to_image or image")
    elif path_to_image is not None and image is not None:
        raise ValueError("Must provide either path_to_image or image, not both")
    
    if path_to_image is not None:
        im = Image.open(path_to_image)
    else:
        im = image

    # Resize image
    new_width = mpc_width - 2 * margin_pix
    new_height = mpc_height - 2 * margin_pix
    im = im.resize((new_width, new_height), Image.ANTIALIAS)

    # Get the background color
    bg_color = im.getpixel((300, 5))
    bg_width = 822
    bg_height = 1122
    background = Image.new('RGB', (bg_width, bg_height), bg_color)

    # crop original image
    im = im.crop((crop_pix, crop_pix, new_width-crop_pix, new_height-crop_pix))

    # paste original image onto background
    background.paste(im, (margin_pix+crop_pix, margin_pix+crop_pix))

    if logo:
        # open Stift logo
        logo = Image.open('layout/stift_united_cartoon.png')
        logo = logo.resize(logo_size, Image.ANTIALIAS)

        # paste logo onto background
        background.paste(logo, logo_loc, mask=logo)

    background.show()

    return background

def proxify_directory(directory="scryfall_images/", output_folder="proxies/", logo=True):
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    files = os.listdir(directory)
    for f in files:
        if f in os.listdir(output_folder):
            print(f"Skipping {f} because it already exists in {output_folder}")
            continue

        proxy = proxify_image(directory+f, logo=logo)
        proxy.save(output_folder+f)
        print(f"Saved {f} to {output_folder}")	

if __name__ == "__main__":
    proxify_directory(directory="fela_and_moya/", output_folder="proxies/fela_and_moya/", logo=False)
