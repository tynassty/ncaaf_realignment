import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from model import create_schools

x = []
y = []
z = []
name = []

schools = create_schools("ncaaf2.txt", rivals_file="knowrivalry.txt")
for school in schools:
    y.append(school.latitude)
    x.append(school.longitude)
    z.append(school.get_detail("sagarin"))
    name.append(school.name)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x, y, z, c='b', marker='o')  # You can customize the color and marker style

ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Sagarin rating')

ax.set_ylim(10, 60)
ax.set_xlim(-160, -60)

plt.show()
