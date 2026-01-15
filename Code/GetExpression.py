#Gets the unicode IDs for the letters and the letters with bars over them
from .Constant import letters, bar_letters

class GetExpression:
    def __init__(self, loop, grid):
        #gets the grid size and loops
        self.grid = grid
        self.loop = loop
        self.cols = self.grid.cols
        self.rows = self.grid.rows

        #sets the var requirements to null
        self.a_req = None
        self.b_req = None
        self.c_req = None
        self.d_req = None

        self.expression_requirements = self.get_requirements()
        self.expression = self.get_expression()
    
    #gets the requirements of the code.
    def get_requirements(self):
        if self.rows == 4 and self.cols == 4:
            #4x4
            x_pos = list({row[0] for row in self.loop})
            y_pos = list({col[1] for col in self.loop})
            self.get_x_req(x_pos)
            self.get_y_req(y_pos)
            
        elif self.rows == 2:
            if self.cols == 2:
                #2x2
                if all(row[0] == self.loop[0][0] for row in self.loop):
                    self.a_req = self.loop[0][0]
                
                if all(row[1] == self.loop[0][1] for row in self.loop):
                    self.b_req = self.loop[0][1]

            elif self.cols == 4:
                #2x4
                x_pos = list({row[0] for row in self.loop})
                
                self.get_x_req(x_pos)

                if all(row[1] == self.loop[0][1] for row in self.loop):
                    self.c_req = self.loop[0][1]
        
        return [self.a_req, self.b_req, self.c_req, self.d_req]
    

    #Gets the x coordinate requirements
    def get_x_req(self, x_pos):
        if 0 in x_pos and 1 in x_pos and 2 in x_pos and 3 in x_pos:
            pass
        else:
            if 0 in x_pos and 1 in x_pos:
                self.a_req = 0
            
            elif 1 in x_pos and 2 in x_pos:
                self.b_req = 1
            
            elif 2 in x_pos and 3 in x_pos:
                self.a_req = 1
            
            elif 3 in x_pos and 0 in x_pos:
                self.b_req = 0

            elif 0 in x_pos:
                self.a_req = 0
                self.b_req = 0

            elif 1 in x_pos:
                self.a_req = 0
                self.b_req = 1

            elif 2 in x_pos:
                self.a_req = 1
                self.b_req = 1
                
            elif 3 in x_pos:
                self.a_req = 1
                self.b_req = 0

    #Gets the Y position requirements.
    def get_y_req(self, y_pos):
        if 0 in y_pos and 1 in y_pos and 2 in y_pos and 3 in y_pos:
            pass
        else:
            if 0 in y_pos and 1 in y_pos:
                self.c_req = 0
            
            elif 1 in y_pos and 2 in y_pos:
                self.d_req = 1
            
            elif 2 in y_pos and 3 in y_pos:
                self.c_req = 1
            
            elif 3 in y_pos and 0 in y_pos:
                self.d_req = 0

            elif 0 in y_pos:
                self.c_req = 0
                self.d_req = 0

            elif 1 in y_pos:
                self.c_req = 0
                self.d_req = 1

            elif 2 in y_pos:
                self.c_req = 1
                self.d_req = 1

            elif 3 in y_pos:
                self.c_req = 1
                self.d_req = 0
    
    def get_expression(self):
        #If there are no requirements for the boolean exp to be true the program returns True
        if all(exp == None for exp in self.expression_requirements):
            return 1
        
        expression = []
        #Creates the boolean logic for the term
        for i in range(len(self.expression_requirements)):
            if self.expression_requirements[i] != None:
                if self.expression_requirements[i]:
                    expression.append(letters[i])
                else:
                    expression.append(bar_letters[i])
        
        #returns all boolean requirements for exp to be true
        if len(expression) == 1:
            return str(expression[0])
        else:
            return ''.join(expression)
      