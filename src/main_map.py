from gps_class_test import GPSVis
from PIL import Image

vis = GPSVis(data_path='pothallref.json',
             map_path='map(10).png',  # Path to map downloaded from the OSM.
             points=(61, 16.7, 60.5, 17.4))


vis.create_image(color=(0, 0, 255), width=100)  # Set the color and the width of the GNSS tracks.
vis.plot_map(output='save')

print()

imfg = Image.open("resultMap.png")
imbg = Image.open("resultCoords.png")
imbg_width, imbg_height = imbg.size
imfg_resized = imfg.resize((imbg_width, imbg_height), Image.LANCZOS)
imbg.paste(imfg_resized, None, imfg_resized)
imbg.save("final.png")