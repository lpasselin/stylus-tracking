import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

radius = 25  # mm
tc = 25 / 3  # mm translation in x and y of corners from center of face


def rotation_around_y(d):
    r = np.deg2rad(d)
    return np.matrix([[np.cos(r), 0, -np.sin(r), 0], [0, 1, 0, 0], [np.sin(r), 0, np.cos(r), 0], [0, 0, 0, 1]])


def rotation_around_z(d):
    r = np.deg2rad(d)
    return np.matrix([[np.cos(r), np.sin(r), 0, 0], [-np.sin(r), np.cos(r), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def rotation_around_x(d):
    r = np.deg2rad(d)
    return np.matrix([[1, 0, 0, 0], [0, np.cos(r), -np.sin(r), 0], [0, np.sin(r), np.cos(r), 0], [0, 0, 0, 1]])


def translation(tx, ty, tz):
    return np.matrix([[1, 0, 0, tx],
                      [0, 1, 0, ty],
                      [0, 0, 1, tz],
                      [0, 0, 0, 1]])


def hom2cart(p):
    return p[:-1] / p[-1]


all_aruco_points = []

origin_points = np.matrix([ [-tc, -tc, 0, 1],
                            [-tc, tc, 0, 1],
                            [tc, tc, 0, 1],
                            [tc, -tc, 0, 1],

                            [0, 0, 0, 1],]).T

for i in [2, 1, 0, 4, 3]:
    aruco_corners = rotation_around_z(72*i) * rotation_around_y(116.565) * \
                    rotation_around_z(180) * translation(0, 0, radius) * origin_points
    all_aruco_points.append(hom2cart(aruco_corners))
for i in [0, 4, 3, 2, 1]:
    aruco_corners = rotation_around_z(72 * i) * rotation_around_y(116.565) * translation(0, 0, -radius) * rotation_around_y(180) * origin_points
    all_aruco_points.append(hom2cart(aruco_corners))

aruco_corners = translation(0, 0, radius) * origin_points
all_aruco_points.append(hom2cart(aruco_corners))
aruco_corners = translation(0, 0, -radius) * rotation_around_y(180) * origin_points
all_aruco_points.append(hom2cart(aruco_corners))


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

for c, ps in enumerate(all_aruco_points):
    ps = np.array(ps)
    # plot lines
    for i in [(0,1), (1, 2), (2, 3), (3, 0)]:
        ax.plot(ps[0, i], ps[1, i], ps[2, i], color='gray')
    # red dot top left
    ax.scatter(ps[0, 0], ps[1, 0], ps[2, 0], color='r')  # plot top left red
    ax.scatter(ps[0, 1], ps[1, 1], ps[2, 1], color='g')  # plot top right green

    # plot text
    ax.text(ps[0, -1], ps[1, -1], ps[2, -1], c, None)

# plot pencil hole
zero_point = np.array([[0, 0, 0, 1]]).T
pp = hom2cart(rotation_around_y(116.565/3) * translation(0, 0, -radius*2) * zero_point)
ax.plot([0, pp[0]], [0, pp[1]], [0, pp[2]], color='b')

plt.title('Red = aruco top left corner')
plt.tight_layout()
plt.show()

all_aruco_points = np.array(all_aruco_points)[:,:,0:4]
print(all_aruco_points)

# all_aruco_points = all_aruco_points.reshape((12*3, 4))
# np.savetxt('aruco_points.txt', all_aruco_points)
print(all_aruco_points)
