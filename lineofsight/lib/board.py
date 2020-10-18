from lineofsight.lib.node import Node
from lineofsight.lib.edge import Edge
from lineofsight.lib.ray import Ray
from lineofsight.res.glob import *
import pygame


class Board:
    def __init__(self, screen, size, pixel_size, draw_grid=0, draw_edges=1):
        self.p_width, self.p_height = pixel_size
        self.width, self.height = size
        self.pixel_size = pixel_size
        self.draw_edges = draw_edges
        self.draw_grid = draw_grid
        self.screen = screen
        self.toggle = False

        self.py_num = self.height // self.p_height
        self.px_num = self.width // self.p_width
        self.empty_edges = [
            Edge((0, 0), (WIDTH, 0)),
            Edge((WIDTH, 0), (WIDTH, HEIGHT)),
            Edge((WIDTH, HEIGHT), (0, HEIGHT)),
            Edge((0, HEIGHT), (0, 0))
        ]

        self.__init_nodes()

    def __init_nodes(self):
        self.nodes = {}
        self.edges = []
        self.corners = []
        for x in range(self.px_num):
            for y in range(self.py_num):
                start_pos = (x * self.p_width, y * self.p_height)
                state = 0

                if (x in [1, self.px_num - 2] and 0 < y < self.py_num - 1) or (
                        y in [1, self.py_num - 2] and 0 < x < self.px_num - 1):
                    state = 1

                self.nodes[x, y] = Node(state, start_pos, self.pixel_size)

        self.__calc_edges()

    def __calc_edges(self):
        for key in self.nodes:
            # self.nodes[key].edge_ids = [-1] * 4

            for direction in directions:
                self.nodes[key].edge_ids[direction] = -1

        self.edges = []
        self.corners = []

        edge_counter = len(self.edges)
        for x in range(self.px_num):
            for y in range(self.py_num):
                current_node = self.nodes[x, y]
                """
                eğer üzerinde bulunduğumuz blok duvarsa:
                
                    solumuzda blok yoksa:
                        üstümüzde blok yoksa ya da üsttekinin solu yoksa:
                            sol için yarat
                        varsa:
                            üstümüzdekinin solunu uzat
                    
                    üstümüzde blok yoksa:
                        solumuzda blok yoksa ya da soldakinin üstü yoksa:
                            üst için yarat
                        varsa:
                            soldakinin üstünü uzat

                    sağımızda blok yoksa:
                        üstümüzde blok yoksa ya da üsttekinin sağı yoksa:
                            sağ için yarat
                        varsa:
                            üstümüzdekinin sağını uzat

                    altımızda blok yoksa:
                        solumuzda blok yoksa ya da soldakinin altı yoksa:
                            alt için yarat
                        varsa:
                            soldakinin altını uzat
                """

                if current_node.state != states.wall:
                    continue

                left = up = down = right = None
                if 0 < y:
                    up = self.nodes[x, y - 1]
                    up = up if up.state == states.wall else None
                if 0 < x:
                    left = self.nodes[x - 1, y]
                    left = left if left.state == states.wall else None
                if y < (self.py_num - 1):
                    down = self.nodes[x, y + 1]
                    down = down if down.state == states.wall else None
                if x < (self.px_num - 1):
                    right = self.nodes[x + 1, y]
                    right = right if right.state == states.wall else None

                if left is None:
                    if up is None or (up is not None
                                      and up.edge_ids[LEFT] == -1):
                        # sol için yarat
                        new_edge = Edge(current_node.topleft,
                                        current_node.bottomleft)
                        self.edges.append(new_edge)

                        current_node.edge_ids[LEFT] = edge_counter
                        edge_counter += 1

                    else:
                        # üstün solunu uzat
                        self.edges[up.edge_ids[LEFT]].ey += self.p_height
                        current_node.edge_ids[LEFT] = up.edge_ids[LEFT]

                if up is None:
                    if left is None or (left is not None
                                        and left.edge_ids[UP] == -1):
                        # üst için yarat
                        new_edge = Edge(current_node.topleft,
                                        current_node.topright)
                        self.edges.append(new_edge)

                        current_node.edge_ids[UP] = edge_counter
                        edge_counter += 1

                    else:
                        # solun üstünü uzat
                        self.edges[left.edge_ids[UP]].ex += self.p_width
                        current_node.edge_ids[UP] = left.edge_ids[UP]

                if right is None:
                    if up is None or (up is not None
                                      and up.edge_ids[RIGHT] == -1):
                        # sağ için yarat
                        new_edge = Edge(current_node.topright,
                                        current_node.bottomright)
                        self.edges.append(new_edge)

                        current_node.edge_ids[RIGHT] = edge_counter
                        edge_counter += 1

                    else:
                        # üstün sağını uzat
                        self.edges[up.edge_ids[RIGHT]].ey += self.p_height
                        current_node.edge_ids[RIGHT] = up.edge_ids[RIGHT]

                if down is None:
                    if left is None or (left is not None
                                        and left.edge_ids[DOWN] == -1):
                        # alt için yarat
                        new_edge = Edge(current_node.bottomleft,
                                        current_node.bottomright)
                        self.edges.append(new_edge)

                        current_node.edge_ids[DOWN] = edge_counter
                        edge_counter += 1

                    else:
                        # solun altını uzat
                        self.edges[left.edge_ids[DOWN]].ex += self.p_width
                        current_node.edge_ids[DOWN] = left.edge_ids[DOWN]

        # aynı köşeler kaldırılıyor (2 kat hızlanma)
        self.corners = []
        for edge in self.edges:
            self.corners.append((edge.sx, edge.sy))
            self.corners.append((edge.ex, edge.ey))
        self.corners = set(self.corners)

    def __calc_rays(self, m_pos, radius=500):
        # test için
        # self.edges = [Edge((500, 500), (600, 600))]
        # self.corners = [(500, 500), (600, 600)]

        rays = []
        for corner in self.corners:
            # corner ile mouse pozisyouna çizgi çekip açısını alıyoruz
            # daha sonra offseti ve hesapladığımız açıyı kullanarak köşe başına 3 tane ışık gönderiyoruz
            # gönderdiğimiz ışığın bir yere çarpıp çarpmadığını hesaplayacağım birazdan
            base_ray = Ray(m_pos, corner)

            for ray in base_ray.create_neigbour_rays():
                ray.calc_intersection(self.edges)
                rays.append(ray)

            # açıya göre sıralıyorum
            rays.sort(key=lambda ray: ray.angle)

        if len(rays) > 1:
            for i in range(len(rays) - 1):
                # sırayla tüm raylerin arası çiziliyor
                pygame.draw.polygon(
                    self.screen, colors.gray,
                    [m_pos, rays[i].end_pos, rays[i + 1].end_pos])

                if DRAW_RAYS:
                    rays[i].draw(pygame, self.screen, colors.white)

            # en son ilk ve son ray birleştiriliyor
            pygame.draw.polygon(self.screen, colors.gray,
                                [m_pos, rays[-1].end_pos, rays[0].end_pos])
            if DRAW_RAYS:
                rays[-1].draw(pygame, self.screen, colors.white)

        self.write(self.screen, f"Ray Count: {len(self.corners)*3}", (10, 10))

    @staticmethod
    def write(screen, msg, pos, font=16):
        font = pygame.font.Font('freesansbold.ttf', font)
        text = font.render(msg, True, colors.white)

        textRect = text.get_rect()
        textRect.topleft = pos

        screen.blit(text, textRect)

    def update(self, m_pos=None):
        self.__draw_nodes()

        if self.toggle and m_pos:
            self.__calc_rays(m_pos)
        if self.draw_grid:
            self.__draw_grid()
        if self.draw_edges:
            self.__draw_edges()

    def __draw_nodes(self):
        for x in range(self.px_num):
            for y in range(self.py_num):
                self.nodes[x, y].draw(self.screen)

    def __draw_grid(self, color=colors.white):
        for x in range(self.px_num + 1):
            for y in range(self.py_num + 1):
                # soldan sağa olan çizgiler
                pygame.draw.line(self.screen, color, (x * self.p_width, 0),
                                 (x * self.p_width, self.height))
                # yukarıdan aşağı doğru olan çizgiler
                pygame.draw.line(self.screen, color, (0, y * self.p_height),
                                 (self.width, y * self.p_height))

    def __draw_edges(self):
        for edge in self.edges:
            rad = int((self.p_width + self.p_height) / 2 * (2 / 15))
            pygame.draw.line(self.screen, colors.lime, edge.start_pos,
                             edge.end_pos, 2)

            pygame.draw.circle(self.screen, colors.turq, edge.start_pos, rad)
            pygame.draw.circle(self.screen, colors.turq, edge.end_pos, rad)

    def get_clicked_pos(self, mouse_pos):
        # x, y = ([i // self.p_width for i in mouse_pos])
        x, y = (mouse_pos[0] // self.p_width, mouse_pos[1] // self.p_height)

        x = (self.px_num - 1) if x > (self.px_num - 1) else x
        y = (self.py_num - 1) if y > (self.py_num - 1) else y

        return x, y

    def set_node_state(self, pos, state):
        self.nodes[pos].state = state
        self.__calc_edges()

    def toggle_switch(self):
        # print("toggle")
        self.toggle = bool(1 - self.toggle)

    def __repr__(self):
        final = ""
        for x in range(self.px_num):
            for y in range(self.py_num):
                final += f"[{repr(self.nodes[x, y])}]"
                final += ", " if y != self.py_num - 1 else ""
            final += "\n" if x != self.px_num - 1 else ""
        return final