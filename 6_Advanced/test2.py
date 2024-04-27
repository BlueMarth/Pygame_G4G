import math
import matplotlib

x = [2, 1, 0, -1, -2, -1, 0, 1]
y = [0, 1, 2, 1, 0, -1, -2, -1]
points = []

for i in range(len(x)):
    points.append([x[i],y[i]])

angles = []
for i in range(len(points)):
    x = points[i][0]
    y = points[i][1]
    angles.append([math.atan2(y,x)])

for i in range(len(angles)):
    print(points[i], angles[i])