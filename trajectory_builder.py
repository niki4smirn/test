def dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def circle_intersection(x1, y1, r1, x2, y2, r2):
    d = dist(x1, y1, x2, y2)
    if d > r1 + r2 or d < r1 - r2 or not d:
        return None
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = (r1 ** 2 - a ** 2) ** 0.5

    x3 = x1 + a * (x2 - x1) / d
    y3 = y1 + a * (y2 - y1) / d

    x4 = x3 + h * (y2 - y1) / d
    y4 = y3 - h * (x2 - x1) / d
    x5 = x3 - h * (y2 - y1) / d
    y5 = y3 + h * (x2 - x1) / d

    return x4, y4, x5, y5


def lines_intersection(line1, line2):
    (a1, b1, c1) = line1.get_coefficients()
    (a2, b2, c2) = line2.get_coefficients()
    if b2 * a1 - b1 * a2 == 0:
        return None
    x = (b1 * c2 - b2 * c1) / (b2 * a1 - b1 * a2)
    if b1 != 0:
        y = -(a1 * x + c1) / b1
    elif b2 != 0:
        y = -(a2 * x + c2) / b2
    else:
        return None
    return round(x), round(y)


def on_same_side(line, x1, y1, x2, y2):
    (a, b, c) = line.get_coefficients()
    return (a * x1 + b * y1 + c) * (a * x2 + b * y2 + c) > 0


def lines_from_point_to_circle(x1, y1, x2, y2, r):
    x3 = (x1 + x2) / 2
    y3 = (y1 + y2) / 2
    r2 = 0.5 * dist(x1, y1, x2, y2)
    inter = circle_intersection(x2, y2, r, x3, y3, r2)
    if inter is not None:
        return (Line(x1=x1, y1=y1, x2=inter[0], y2=inter[1]),
                Line(x1=x1, y1=y1, x2=inter[2], y2=inter[3]))
    else:
        return None


def move_to_circle(line1, x, y, r):
    if line1 is None:
        return None
    (a, b, c) = line1.get_coefficients()
    c1 = (r * r * (a * a + b * b)) ** 0.5
    c2 = -c1
    c1 -= (a * x) + (b * y)
    c2 -= (a * x) + (b * y)
    if abs(c1 - c) < abs(c2 - c):
        return Line(a=a, b=b, c=c1)
    else:
        return Line(a=a, b=b, c=c2)


def lines_from_circle_to_circle(x1, y1, r1, x2, y2, r2):
    (line1, line2) = lines_from_point_to_circle(x2, y2, x1, y1, r1 - r2)  # outside
    (line3, line4) = lines_from_point_to_circle(x2, y2, x1, y1, r1 + r2)  # inside
    line1 = move_to_circle(line1, x1, y1, r1)
    line2 = move_to_circle(line2, x1, y1, r1)
    line3 = move_to_circle(line3, x1, y1, r1)
    line4 = move_to_circle(line4, x1, y1, r1)
    temp1 = line1.get_coefficients()
    temp2 = line2.get_coefficients()
    if temp1 == temp2:
        line2.set_c(-temp1[2] - 2 * ((temp1[0] * x1) + (temp1[1] * y1)))
    return line1, line2, line3, line4


class Line:
    def __init__(self, **kwargs):
        y1 = kwargs.get("y1")
        y2 = kwargs.get("y2")
        x1 = kwargs.get("x1")
        x2 = kwargs.get("x2")

        a = kwargs.get("a")
        b = kwargs.get("b")
        c = kwargs.get("c")

        if x1 is not None and \
                x2 is not None and \
                y1 is not None and \
                y2 is not None:
            self.a = y2 - y1
            self.b = x1 - x2
            self.c = x2 * y1 - x1 * y2

        if a is not None and \
                b is not None and \
                c is not None:
            self.a = a
            self.b = b
            self.c = c

    def get_coefficients(self):
        return self.a, self.b, self.c

    def set_c(self, c):
        self.c = c

