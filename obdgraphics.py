class Point:

    def __init__(self, x, y):
        self.x = round(x)
        self.y = round(y)


class Line:

    def __init__(self, start, end):
        if isinstance(start, Point):
            self.start = start
        else:
            raise TypeError
        if isinstance(end, Point):
            self.end = end
        else:
            raise TypeError

    def sample(self, t):
        if t < 0:
            raise ValueError
        if t > 1:
            raise ValueError
        x = self.start.x
        y = self.start.y
        x += t * (self.end.x - self.start.x)
        y += t * (self.end.y - self.start.y)
        return(Point(x, y))


class Curve:

    def __init__(self, p0, p1, p2):
        self.l0 = Line(p0, p1)
        self.l1 = Line(p1, p2)

    def sample(self, t):
        if t < 0:
            raise ValueError
        if t > 1:
            raise ValueError
        q0 = self.l0.sample(t)
        q1 = self.l1.sample(t)
        qline = Line(q0, q1)
        return(qline.sample(t))


class Raster():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bytesperrow = width // 8
        if width % 8:
            self.bytesperrow += 1
        self.data = bytearray(self.bytesperrow * height)

    def draw(self, p):
        if isinstance(p, Point) == False:
            raise TypeError
        if p.x >= self.width:
            return()
        if p.y >= self.height:
            return()
        biti = p.x % 8
        bytei = p.y * self.bytesperrow + p.x // 8
        mask = 128 >> biti
        self.data[bytei] = self.data[bytei] | mask

    def save(self, name):
        f = open(name, "wb")
        header = "P4 " + str(self.width) + " " +str(self.height) + " "
        header = bytes(header, "ascii")
        f.write(header)
        f.write(self.data)
        f.close()



example = Raster(425, 550)

c = Curve(Point(10,10), Point(410, 310), Point(110, 110))

i = 0
m = 100000
while i <= m:
    example.draw(c.sample(i/m))
    i += 1

example.save("example.pbm")
