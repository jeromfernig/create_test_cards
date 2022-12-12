from scryfall_api import run_scryfall_api, save_images
from remove_owned import remove_owned, delete_fullart_daretti, move_dfcs_to_subfolder
from prepare_as_proxy import proxify_directory

# Get card data from Scryfall API for vintage cube
data = run_scryfall_api("https://api.scryfall.com/cards/search?q=cube=vintage")

# Download images from Scryfall API
save_images(data)

# Filter cards that we already own
remove_owned()
delete_fullart_daretti()

# Proxify each image
proxify_directory()

# Move double-faced cards to subfolder
move_dfcs_to_subfolder()

proxify_directory(directory='personal_cards/', output_folder='proxies/personal_proxies/')
proxify_directory(directory='custom_cards/', output_folder='proxies/custom_proxies/', logo=False)


