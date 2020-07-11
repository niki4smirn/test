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


# nails_list = []
nail_params = {
      "r": 0.06,
      "head_r": 2,
      "length": 2,
      "depth": 1
}

image = np.zeros((500, 500, 1), dtype="uint8")


ratio = 12
real_head_r = int(nail_params["head_r"] * ratio)

# nails_list.append(Nail(100, 100, 0, nail_params))
# nails_list.append(Nail(100, 400, 1, nail_params))
# nails_list.append(Nail(400, 400, 2, nail_params))
cv2.circle(image, (100, 100), real_head_r, 255, -1)
cv2.circle(image, (400, 100), real_head_r, 255, -1)
cv2.circle(image, (400, 400), real_head_r, 255, -1)


strings_list = [((100, 100), (400, 400)),
                ((400, 400), (400, 100)),
                ((400, 100), (100, 100))]

prev_line = None
segment1 = strings_list[-1]
line1 = tb.lines_from_circle_to_circle(segment1[0][0], segment1[0][1],
                                       real_head_r,
                                       segment1[1][0], segment1[1][1],
                                       real_head_r)[0]

segment2 = strings_list[0]
line2 = tb.lines_from_circle_to_circle(segment2[0][0], segment2[0][1],
                                       real_head_r,
                                       segment2[1][0], segment2[1][1],
                                       real_head_r)[0]
prev_dot = tb.lines_intersection(line1, line2)
first_dot = prev_dot

i = 0

for string in strings_list:
    ((x1, y1), (x2, y2)) = string
    (line1, line2, line3, line4) = \
        tb.lines_from_circle_to_circle(x1, y1, real_head_r,
                                       x2, y2, real_head_r)

    if prev_line is None:
        prev_line = line1
    elif tb.on_same_side(prev_line, x1, y1, x2, y2):
        dot1 = tb.lines_intersection(prev_line, line1)
        dot2 = tb.lines_intersection(prev_line, line2)
        dist1 = tb.dist(prev_dot[0], prev_dot[1], dot1[0], dot1[1])
        dist2 = tb.dist(prev_dot[0], prev_dot[1], dot2[0], dot2[1])
        if dist1 > dist2:
            cv2.line(image, prev_dot, dot1, 128, 3)
            prev_dot = dot1
            prev_line = line1
        else:
            cv2.line(image, prev_dot, dot2, 128, 3)
            prev_dot = dot2
            prev_line = line2
    else:
        pass
    cv2.imshow(str(i), image)
    i += 1

cv2.line(image, prev_dot, first_dot, 128, 3)
cv2.imshow("final", image)
cv2.waitKey(0)
