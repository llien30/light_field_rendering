import math
import os

import cv2
import numpy as np
from scipy.interpolate import LinearNDInterpolator


def make_bulldozer_data():
    image_path = "./bulldozer"
    files = os.listdir(image_path)
    files.sort()
    light_field_4d = np.zeros((17, 17, 1152, 1536, 3), dtype=np.uint8)
    for u in range(17):
        for v in range(17):
            image = cv2.imread(f"{image_path}/{files[u * 17 + v]}")
            light_field_4d[u, v, :, :, :] = image
    return light_field_4d


def make_knight_data():
    image_path = "./knight"
    files = os.listdir(image_path)
    files.sort()
    light_field_4d = np.zeros((17, 17, 1024, 1024, 3), dtype=np.uint8)
    for u in range(17):
        for v in range(17):
            image = cv2.imread(f"{image_path}/{files[u * 17 + v]}")
            light_field_4d[u, v, :, :, :] = image
    return light_field_4d


def bulldozer_light_field_4d(s: float, t: float, u: float, v: float, data) -> set:

    S = [math.floor(s), math.ceil(s), math.floor(s) - 1]
    T = [math.floor(t), math.ceil(t), math.ceil(t) + 1]
    U = [math.floor(u), math.ceil(u), math.floor(u) - 1]
    V = [math.floor(v), math.ceil(v), math.ceil(v) + 1]
    coords = []
    blue = []
    green = []
    red = []
    for s_coord in S:
        for t_coord in T:
            for u_coord in U:
                for v_coord in V:
                    coords.append((s_coord, t_coord, u_coord, v_coord))
                    if (
                        0 <= s_coord < 17
                        and 0 <= t_coord < 17
                        and 0 <= u_coord < 1152
                        and 0 <= v_coord < 1536
                    ):
                        blue.append(data[s_coord][t_coord][u_coord][v_coord][0])
                        green.append(data[s_coord][t_coord][u_coord][v_coord][1])
                        red.append(data[s_coord][t_coord][u_coord][v_coord][2])
                    else:
                        blue.append(0)
                        green.append(0)
                        red.append(0)
    blue_light_field = LinearNDInterpolator(coords, blue, 0)
    green_light_field = LinearNDInterpolator(coords, green, 0)
    red_light_field = LinearNDInterpolator(coords, red, 0)

    b = blue_light_field(s, t, u, v)
    g = green_light_field(s, t, u, v)
    r = red_light_field(s, t, u, v)

    return b, g, r


def knight_light_field_4d(s: float, t: float, u: float, v: float, data) -> set:

    S = [math.floor(s), math.ceil(s), math.floor(s) - 1]
    T = [math.floor(t), math.ceil(t), math.ceil(t) + 1]
    U = [math.floor(u), math.ceil(u), math.floor(u) - 1]
    V = [math.floor(v), math.ceil(v), math.ceil(v) + 1]
    coords = []
    blue = []
    green = []
    red = []
    for s_coord in S:
        for t_coord in T:
            for u_coord in U:
                for v_coord in V:
                    coords.append((s_coord, t_coord, u_coord, v_coord))
                    if (
                        0 <= s_coord < 17
                        and 0 <= t_coord < 17
                        and 0 <= u_coord < 1024
                        and 0 <= v_coord < 1024
                    ):
                        blue.append(data[s_coord][t_coord][u_coord][v_coord][0])
                        green.append(data[s_coord][t_coord][u_coord][v_coord][1])
                        red.append(data[s_coord][t_coord][u_coord][v_coord][2])
                    else:
                        blue.append(0)
                        green.append(0)
                        red.append(0)
    blue_light_field = LinearNDInterpolator(coords, blue, 0)
    green_light_field = LinearNDInterpolator(coords, green, 0)
    red_light_field = LinearNDInterpolator(coords, red, 0)

    b = blue_light_field(s, t, u, v)
    g = green_light_field(s, t, u, v)
    r = red_light_field(s, t, u, v)

    return b, g, r


def bulldozer_light_field_renderer(
    x: float, y: float, z: float, theta: float, data, save_path
) -> None:
    image = np.zeros((100, 100, 3))
    r = z / (1 - z)
    max_h = x + (1 - z) * math.tan(theta)
    min_h = x - (1 - z) * math.tan(theta)
    max_w = y + (1 - z) * math.tan(theta)
    min_w = y - (1 - z) * math.tan(theta)
    for h in range(100):
        for w in range(100):
            u = min_h + (max_h - min_h) * h / 100
            v = min_w + (max_w - min_w) * w / 100
            s = x + (x - u) * r
            t = y + (v - y) * r

            s *= 17
            t *= 17
            u *= 1152
            v *= 1536
            blue, green, red = bulldozer_light_field_4d(s, t, u, v, data)
            image[h, w, :] = [int(blue), int(green), int(red)]
    cv2.imwrite(save_path, image)

    return


def knight_light_field_renderer(
    x: float, y: float, z: float, theta: float, data, save_path
) -> None:
    image = np.zeros((100, 100, 3))
    r = z / (1 - z)
    max_h = x + (1 - z) * math.tan(theta)
    min_h = x - (1 - z) * math.tan(theta)
    max_w = y + (1 - z) * math.tan(theta)
    min_w = y - (1 - z) * math.tan(theta)
    for h in range(100):
        for w in range(100):
            u = min_h + (max_h - min_h) * h / 100
            v = min_w + (max_w - min_w) * w / 100
            s = x + (x - u) * r
            t = y + (v - y) * r

            s *= 17
            t *= 17
            u *= 1024
            v *= 1024
            blue, green, red = knight_light_field_4d(s, t, u, v, data)
            image[h, w, :] = [int(blue), int(green), int(red)]
    cv2.imwrite(save_path, image)

    return


def bulldozer_light_field_renderer_rotate(omega, z, theta, data, save_path) -> None:
    image = np.zeros((100, 100, 3))
    r = z / (1 - z)

    x = 0.5 + 0.1 * math.sin(omega)
    y = 0.5 + 0.1 * math.cos(omega)
    phi_x = math.atan(0.1 * math.sin(omega) / (1 - z))
    phi_y = math.atan(0.1 * math.cos(omega) / (1 - z))
    max_h = x + (1 - z) * math.tan(theta + phi_x)
    min_h = x - (1 - z) * math.tan(theta - phi_x)
    max_w = y + (1 - z) * math.tan(theta + phi_y)
    min_w = y - (1 - z) * math.tan(theta - phi_y)
    for h in range(100):
        for w in range(100):
            u = min_h + (max_h - min_h) * h / 100
            v = min_w + (max_w - min_w) * w / 100
            s = x + (x - u) * r
            t = y + (v - y) * r

            s *= 17
            t *= 17
            u *= 1152
            v *= 1536
            blue, green, red = bulldozer_light_field_4d(s, t, u, v, data)
            image[h, w, :] = [int(blue), int(green), int(red)]
    cv2.imwrite(save_path, image)
    print("image saved!")

    return


# rectified_data = make_rectified_data()
# print("Finished Load Data!")
# b_light_field, g_light_field, r_light_field = light_field_4d(rectified_data)
# print("Finished Making Light Field!")
# for x in range(3, 8):
#     for y in range(3, 8):
#         light_field_renderer(
#             x * 0.1,
#             y * 0.1,
#             0.05,
#             0.5,
#             rectified_data,
#             "./rectified_rendered/{:.2f}_{:.2f}_0.8.png".format(x * 0.1, y * 0.1),
#         )
#         print("image saved!")

# for phi in range(35, 45):
#     light_field_renderer(
#         0.5,
#         0.5,
#         0.05,
#         phi * 0.01,
#         rectified_data,
#         "./rectified_rendered/0.5_0.5_{:.2f}.png".format(phi * 0.1),
#     )
#     print("image saved!")

# for z in range(-5, 6):
#     light_field_renderer(
#         0.5,
#         0.5,
#         z * 0.1,
#         0.5,
#         rectified_data,
#         f"./video_image/{z+5}.png",
#     )
#     print("image saved!")
