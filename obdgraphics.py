class Point:

    def __init__(self, x, y):
        self.x = round(x)
        self.y = round(y)

    def __repr__(self):
        r = "Point(" + str(self.x) + ", " + str(self.y) + ")"
        return(r)


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

    def __repr__(self):
        r = "Line("
        r += self.start.__repr__()
        r += ", "
        r += self.end.__repr__()
        r += ")"
        return(r)


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

    def __repr__(self):
        r = "Curve("
        r += self.l0.start.__repr__()
        r += ", "
        r += self.l0.end.__repr__()
        r += ", "
        r += self.l1.end.__repr__()
        r += ")"
        return(r)


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


class Path:

    def __init__(self, pathstring):
        self.pathstring = pathstring
        self.linecurves = []
        last = None
        op = None
        coord = None
        points = []

        for token in pathstring.split(" "):
            if token == "-":
                points.append(last)
            elif token[0] in "1234567890":
                token = float(token)
                if coord:
                    last = Point(coord, token)
                    points.append(last)
                    coord = None
                else:
                    coord = token
            elif token in "LC":
                op = token
            if op == "L" and len(points) == 2:
                self.linecurves.append(Line(points[0], points[1]))
                points = []
            elif op == "C" and len(points) == 3:
                self.linecurves.append(Curve(points[0], points[1], points[2]))
                points = []

    def render(self, raster, samplenum):
        for lc in self.linecurves:
            i = 0
            while i < samplenum:
                raster.draw(lc.sample(i/samplenum))
                i += 1



example = Raster(425, 550)
p = Path("C 60 10 110 10 110 60 C - 110 110 60 110 C - 10 110 10 60 C - 10 10 60 10")
p.render(example, 100000)
example.save("example.pbm")
