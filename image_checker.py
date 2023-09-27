import os.path
from model import create_schools

schools = create_schools("ncaaf2.txt")

for school in schools:
    image_path = school.get_name()
    image_path = image_path.replace(" ", "_")
    image_path = "images/" + image_path + ".png"
    if not os.path.isfile(image_path):
        print(school.get_name())
