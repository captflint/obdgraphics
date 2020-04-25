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

i = 100
while i < 300:
    example.draw(Point(i, i))
    i += 1

example.save('example.pbm')
