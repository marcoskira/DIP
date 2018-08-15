class Pixel:
    r = 0
    g = 0
    b = 0
    
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label


class Blob:

    pixels_list = []
    pixels_qty = 0

    def __init__(self, label):
        self.label = label