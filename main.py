import numpy as np
import cv2

import trajectory_builder as tb


class Nail:
    def __init__(self, x, y, idx, param):
        self._x = x
        self._y = y

        self._idx = idx

        self._r = param["r"]
        self._head_r = param["head_r"]
        self._length = param["length"]
        self._depth = param["depth"]

        self._strings_number = 0

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_idx(self):
        return self._idx

    def get_strings_number(self):
        return self._strings_number

    def set_strings_number(self, strings_number):
        self._strings_number = strings_number

    def distance_to(self, nail):
        x = nail.get_x()
        y = nail.get_y()
        return ((self._x - x) ** 2 + (self._y - y) ** 2) ** 0.5


nails_list = []
nail_params = {
      "r": 0.06,
      "head_r": 0.175,
      "length": 2,
      "depth": 1
}

image = np.zeros((60, 60, 1), dtype="uint8")


ratio = 12
real_head_r = int(nail_params["head_r"] * ratio)

nails_list.append(Nail(20, 20, 0, nail_params))
nails_list.append(Nail(20, 30, 1, nail_params))
nails_list.append(Nail(30, 30, 2, nail_params))
cv2.circle(image, (20, 20), real_head_r, 255, -1)
cv2.circle(image, (20, 30), real_head_r, 255, -1)
cv2.circle(image, (30, 30), real_head_r, 255, -1)


strings_list = [((20, 20), (20, 30)),
                ((20, 30), (30, 30)),
                ((30, 30), (20, 20))]

for string in strings_list:
    (line1, line2, line3, line4) = \
        tb.lines_from_circle_to_circle(string[0][0], string[0][1], real_head_r,
                                       string[1][0], string[1][1], real_head_r)

cv2.imshow("1", image)
cv2.waitKey(0)



