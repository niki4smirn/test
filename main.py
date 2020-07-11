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
      "head_r": 2,
      "length": 2,
      "depth": 1
}

image = np.zeros((500, 500, 1), dtype="uint8")


ratio = 12
real_head_r = int(nail_params["head_r"] * ratio)

nails_list.append(Nail(20, 20, 0, nail_params))
nails_list.append(Nail(20, 450, 1, nail_params))
nails_list.append(Nail(450, 450, 2, nail_params))
cv2.circle(image, (20, 20), real_head_r, 255, -1)
cv2.circle(image, (20, 450), real_head_r, 255, -1)
cv2.circle(image, (450, 450), real_head_r, 255, -1)


strings_list = [((20, 20), (20, 450)),
                ((20, 450), (450, 450)),
                ((450, 450), (20, 20))]

prev_line = None
prev_dot = (20, 20)

for string in strings_list:
    ((x1, y1), (x2, y2)) = string
    (line1, line2, line3, line4) = \
        tb.lines_from_circle_to_circle(x1, y1, real_head_r,
                                       x2, y2, real_head_r)

    if prev_line is None:
        prev_line = line1
        cv2.line(image, (x1, y1), (x2, y2), 128, 3)
    elif tb.on_same_side(prev_line, x1, y1, x2, y2):
        dot1 = tb.lines_intersection(prev_line, line1)
        dot2 = tb.lines_intersection(prev_line, line2)
        dist1 = tb.dist(prev_dot[0], prev_dot[1], dot1[0], dot1[1])
        dist2 = tb.dist(prev_dot[0], prev_dot[1], dot2[0], dot2[1])
        if dist1 > dist2:
            cv2.line(image, dot1, (x2, y2), 128, 3)
            prev_line = line1
        else:
            cv2.line(image, dot2, (x2, y2), 128, 3)
            prev_line = line2
    else:
        pass

cv2.circle(image, (20, 20), real_head_r, 255, -1)
cv2.circle(image, (20, 450), real_head_r, 255, -1)
cv2.circle(image, (450, 450), real_head_r, 255, -1)

cv2.imshow("1", image)
cv2.waitKey(0)



