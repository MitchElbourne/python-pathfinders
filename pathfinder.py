import pygame
import random as rd

pygame.init()

clock = pygame.time.Clock()

SIZE = {"width": 500, "height": 500}
TABLE = {"columns": 100, "rows": 100}

screen = pygame.display.set_mode((SIZE["width"], SIZE["height"]))

class Graph:
    """Graph -> Constructs a dict graph"""
    def __init__(self, size, table):
        self.width = size['width']
        self.height = size['height']
        self.columns = table['columns']
        self.rows = table['rows']
        self.table = []
        self.updated = True

    def construct_table(self):
        """Construct the data table"""
        for row in range(self.rows):
            for column in range(self.columns):
                self.table.append({
                    "coords" : f"{row},{column}",
                    "width": self.width / self.columns,
                    "height": self.height / self.rows,
                    "start": False,
                    "end": False,
                    "visited": False,
                    "wall": False
                })
        self.set_start()
        self.set_end()

    def get_x(self, node):
        """Returns the x of the node in pixels"""
        return int(node["coords"].split(',')[0]) * node["width"]

    def get_y(self, node):
        """Returns the y of the node in pixels"""
        return int(node["coords"].split(',')[1]) * node["height"]

    def update_node(self, coords, type):
        """Takes in coordinates from mouse pos and updates the node"""
        for node in self.table:
            node_coords = (self.get_x(node), self.get_y(node))
            if(coords[0] > node_coords[0] and coords[0] < node_coords[0] + node["width"]):
                if(coords[1] > node_coords[1] and coords[1] < node_coords[1] + node["height"]):
                    if not node[type] and not node["start"] and not node["end"]:
                        node.update({type: True})
                    else:
                        node.update({type: False})
                    self.updated = True

    def generate_random_coords(self):
        """Generate coordinates based on rows and columns"""
        coords = f"{rd.randrange(0, self.rows)},{rd.randrange(0, self.columns)}"
        return coords

    def set_start(self):
        """Set the start position on the graph"""
        set_start = False
        start_coords = self.generate_random_coords()

        while set_start is False:
            for element in self.table:
                if element["coords"] == start_coords:
                    element["start"] = True
                    set_start = True

    def set_end(self):
        """Set the end position on the graph"""
        set_end = False

        while set_end is False:
            end_coords = self.generate_random_coords()

            for element in self.table:
                if element["coords"] == end_coords and element["start"] is not True:
                    element["end"] = True
                    set_end = True

    def draw(self, table):
        """Draw the table onto the window"""
        if self.updated:
            def colour(node):
                # start node
                if node["start"]:
                    return (50,205,50)
                # end node
                if node["end"]:
                    return (155,17,30)
                # visited node
                if node["visited"]:
                    return (200,255,255)
                if node["wall"]:
                    return (0,0,0)
                # default node
                return (128,128,128)

            for node in table:
                pygame.draw.rect(screen, colour(node), pygame.Rect(self.get_x(node), self.get_y(node), node["width"], node["height"]))

        self.updated = False

graph = Graph(SIZE, TABLE)
graph.construct_table()

RUN = True
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            graph.update_node(pygame.mouse.get_pos(), "wall")

    graph.draw(graph.table)

    pygame.display.update()
    clock.tick(60)
