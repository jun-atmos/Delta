import os
import glob

img_dir = 'rain_img/'
csv_dir = 'weather_csv/'
[os.remove(file) for file in glob.glob(os.path.join(csv_dir, '*'))]
[os.remove(file) for file in glob.glob(os.path.join(img_dir, '*'))]