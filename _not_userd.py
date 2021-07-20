import os
from itertools import product

import numpy as np
from scipy.interpolate import LinearNDInterpolator


def light_field_4d(data):
    image_path = "./rectified"
    files = os.listdir(image_path)
    files.sort()

    S = [i - 0 for i in range(2)]
    T = [i - 0 for i in range(2)]
    U = [i - 576 for i in range(1152)]
    V = [i - 768 for i in range(1536)]

    coords = []
    color_r = []
    color_b = []
    color_g = []
    for s in S:
        for t in T:
            for u in U:
                for v in V:
                    coords.append((s, t, u, v))
                    bgr = data[s + 0][t + 0][u + 576][v + 768]
                    color_b.append(bgr[0])
                    color_g.append(bgr[1])
                    color_r.append(bgr[2])

    b_light_field = LinearNDInterpolator(coords, color_b)
    print("Finished making blue light field")
    g_light_field = LinearNDInterpolator(coords, color_g)
    print("Finished making green light field")
    r_light_field = LinearNDInterpolator(coords, color_r)
    print("Finished making red light field")
    return b_light_field, g_light_field, r_light_field


def interpolator(coords, data, point):
    dims = len(point)
    indices = []
    sub_coords = []
    for j in range(dims):
        idx = np.digitize([point[j]], coords[j])[0]
        indices += [[idx - 1, idx]]
        sub_coords += [coords[j][indices[-1]]]
    indices = np.array([j for j in product(*indices)])
    sub_coords = np.array([j for j in product(*sub_coords)])
    sub_data = data[list(np.swapaxes(indices, 0, 1))]
    li = LinearNDInterpolator(sub_coords, sub_data)
    return li([point])[0]
