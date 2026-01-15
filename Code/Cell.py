#Cell class. It retains a boolean identity for each cell in the main map.
class Cell:
    def __init__(self):
        #sets itself to False at init
        self.num = 0
    
    def clicked(self):
        #when it is clicked it inverts its boolean identity
        self.num = not self.num
    
    def get_num(self):
        #returns the number back into the main GUI.
        return self.num