from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Line

import random
from .Constant import LOOP_COLOR
from .GetExpression import GetExpression

class Loop(Widget):
    def __init__(self, coords, grid, padding=5, **kwargs):
        super().__init__(**kwargs)
        self.coords = coords
        self.grid = grid
        self.color = random.choice(LOOP_COLOR)
        self.padding = padding
        self.radius = 100
        self.expression = self.get_expression()
        print(self.expression)

        self.grid.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_once(self.redraw)
    

    def redraw(self, *args):
        self.canvas.clear()

        with self.canvas:
            Color(*self.color)

            cols = self.grid.cols
            rows = self.grid.rows
            cell_width = self.grid.width / cols
            cell_height = self.grid.height / rows

            min_col = min(c for c, r in self.coords)
            max_col = max(c for c, r in self.coords)
            min_row = min(r for c, r in self.coords)
            max_row = max(r for c, r in self.coords)
            min_y = self.grid.y + (rows - max_row - 1) * cell_height - self.padding
            max_y = self.grid.y + (rows - min_row) * cell_height + self.padding
            min_x = self.grid.x + min_col * cell_width - self.padding
            max_x = self.grid.x + (max_col + 1) * cell_width + self.padding

            self.radius = min(cell_width, cell_height) * 0.5

            circle_x1 = min_x + cell_width - (cell_width * 0.3)
            circle_x2 = max_x - cell_width + (cell_width * 0.3)
            loop_height = max_y - min_y

            circle_y1 = min_y + cell_height - (cell_height * 0.3)
            circle_y2 = max_y - cell_height + (cell_height * 0.3)
            loop_width = max_x - min_x
            
            if (min_col + 1 in (c for c, r in self.coords)) or (min_col == max_col):
                if (min_row + 1 in (r for c, r in self.coords)) or (min_row == max_row):
                    #loop normally
                    Line(
                        rounded_rectangle=(min_x, min_y, max_x - min_x, max_y - min_y, self.radius),
                        width=2
                    )

                else:
                    #loop vertically
                    Line(ellipse = (min_x, circle_y1 - self.radius, loop_width, self.radius * 2, -90, 90), width = 2)
                    Line(points=[min_x, circle_y1, min_x, circle_y1 - cell_height], width = 2)
                    Line(points=[max_x, circle_y1, max_x, circle_y1 - cell_height], width = 2)

                    Line(ellipse = (min_x, circle_y2 - self.radius, loop_width, self.radius * 2, 90, 270), width = 2)
                    Line(points=[min_x, circle_y2, min_x, circle_y2 + cell_height], width = 2)
                    Line(points=[max_x, circle_y2, max_x, circle_y2 + cell_height], width = 2)


            if  not( (min_col + 1 in (c for c, r in self.coords)) or (min_col == max_col)):
                if (min_row + 1 in (r for c, r in self.coords)) or (min_row == max_row):
                    #loop horizontally
                    Line(ellipse=(circle_x1 - self.radius, min_y, self.radius * 2,loop_height, 0, 180), width=2)
                    Line(points=[circle_x1, min_y, circle_x1 - (cell_width*1.0), min_y], width=2)
                    Line(points=[circle_x1, max_y, circle_x1 - (cell_width*1.0), max_y], width=2)
                    
                    Line(ellipse=(circle_x2 - self.radius, min_y, self.radius * 2,loop_height, 180, 360), width=2)
                    Line(points=[circle_x2, max_y, circle_x2 + cell_width, max_y], width=2)
                    Line(points=[circle_x2, min_y, circle_x2 + cell_width, min_y], width=2)
                
                else:
                    #loop 4 corners
                    print('hello')
                    Line(circle=(circle_x1, circle_y1, self.radius, 0, 90), width=2)
                    Line(points=[circle_x1 + self.radius, circle_y1, circle_x1 + self.radius, circle_y1 - cell_height], width = 2)
                    Line(points=[circle_x1, circle_y1 + self.radius, circle_x1 - cell_width, circle_y1 + self.radius], width = 2)
                    
                    Line(circle=(circle_x2, circle_y2 , self.radius, 180, 270), width=2)
                    Line(points=[circle_x2 - self.radius, circle_y2 + cell_height, circle_x2 - self.radius, circle_y2], width = 2)
                    Line(points=[circle_x2, circle_y2 - self.radius, circle_x2 + cell_width, circle_y2 - self.radius], width = 2)

                    Line(circle=(circle_x1, circle_y2 , self.radius, 90, 180), width=2)
                    Line(points=[circle_x1 + self.radius, circle_y2 + cell_height, circle_x1 + self.radius, circle_y2], width = 2)
                    Line(points=[circle_x1, circle_y2 - self.radius, circle_x1 - cell_width, circle_y2 - self.radius], width = 2)

                    Line(circle=(circle_x2, circle_y1 , self.radius, 270, 360), width=2)
                    Line(points=[circle_x2 - self.radius, circle_y1 - cell_height, circle_x2 - self.radius, circle_y1], width = 2)
                    Line(points=[circle_x2, circle_y1 + self.radius, circle_x2 + cell_width, circle_y1 + self.radius], width = 2)

    def get_expression(self):
        expression_resolver = GetExpression(self.coords, self.grid)
        return expression_resolver.expression
