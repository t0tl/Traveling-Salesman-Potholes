from gps_class_test import GPSVis

vis = GPSVis(data_path='pothallref.json',
             map_path='map(1).png',  # Path to map downloaded from the OSM.
             #points=(60.7384, 17.0896, 60.6303, 17.2288)) # Two coordinates of the map (upper left, lower right) for map.png
             #points=(60.743034, 17.059659, 60.630945, 17.297264)) #map1
             points=(61.1, 16.6, 60.2, 17.4)) #map(1) 61.1


vis.create_image(color=(0, 0, 255), width=100)  # Set the color and the width of the GNSS tracks.
vis.plot_map(output='save')

print()