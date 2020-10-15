class Edge:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

        # self.sx, self.sy = start_pos
        # self.ex, self.ey = end_pos

    @property
    def start_pos(self):
        return self.sx, self.sy

    @property
    def end_pos(self):
        return self.ex, self.ey

    @start_pos.setter
    def start_pos(self, value):
        self.sx, self.sy = value

    @end_pos.setter
    def end_pos(self, value):
        self.ex, self.ey = value