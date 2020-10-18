from lineofsight.res.glob import *
import math

# radius'un önemi yok çünkü biz zaten gönderdiğimiz rayi ışın olarak kabul ediyoruz
radius = 1


class Ray:
    def __init__(self, m_pos, corner=None, angle=None):
        self.corner = corner
        self.m_pos = m_pos

        if angle:
            self.rdx = math.cos(angle) * radius
            self.rdy = math.sin(angle) * radius
            self.angle = angle
        elif corner:
            self.rdx = corner[0] - m_pos[0]
            self.rdy = corner[1] - m_pos[1]
            self.angle = math.atan2(self.rdy, self.rdx)
        else:
            raise ValueError

        self.start_pos = m_pos
        self.end_pos = (self.rdx + m_pos[0], self.rdy + m_pos[1])

    def create_neigbour_rays(self, offset=0.0001):
        ray1 = Ray(self.m_pos, angle=(self.angle - offset))
        ray3 = Ray(self.m_pos, angle=(self.angle + offset))

        # internette gördüğüm algoritmalar direkt olarak köşeye gönderilen ışınları da
        # hesaplıyor, fakat bunu yapmamız gerekmiyor çünkü zaten o köşenin kordinatlarına
        # sahibiz visibility poligonunu çizereken köşeleri de ekleyebiliriz

        return [ray1, self, ray3]
        # return [ray1, ray3]

    def __check_intersection(self, edge, *a, **kw):
        # The Coding Train Raycasting video:
        # https://www.youtube.com/watch?v=TOEi6T2mtHo&t=1777s

        # One Lone Coder Shadow Casting video:
        # https://www.youtube.com/watch?v=fc3nnG2CG8U&t=2238s

        # line - line intersection wikipedia:
        # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

        x1, y1 = edge.sx, edge.sy
        x2, y2 = edge.ex, edge.ey

        x3, y3 = self.start_pos
        x4, y4 = self.end_pos

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if den:
            # t edge için
            # u ışın için

            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

            # print(f"t: {t}, u:{u}, if {0 <= t <= 1 and 0 <= u}")
            if 0 <= t <= 1 and 0 <= u:
                return u

    def calc_intersection(self, edges, *a, **kw):
        intersections = []

        x3, y3 = self.start_pos
        x4, y4 = self.end_pos

        for edge in edges:
            # kesişim varsa listeye ekle
            if (rv := self.__check_intersection(edge, *a, **kw)):
                # hepsini kaydediyorum çünkü hangisinin en yakın olacağını bilemeyiz
                intersections.append(rv)

        # eğer kesişim varsa
        if len(intersections) > 0:
            #   ışık çarptıktan sonra ilerleyemediği için
            # ilk çarptığı yeri bulup sonrasını boş vereceğiz
            intersections.sort()
            self.end_pos = (x3 + intersections[0] * (x4 - x3),
                            y3 + intersections[0] * (y4 - y3))

    def draw(self, pygame, screen, color=colors.white):
        pygame.draw.line(screen, color, self.start_pos, self.end_pos)
