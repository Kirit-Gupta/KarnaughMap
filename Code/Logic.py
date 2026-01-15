#Displays example format of the array_of_vals input for future reference and reusbaility

array_of_vals_example_format  = [[1, 0],[0, 1]]  #  1 0
                                                 #  0 1

#Creates the class MapLogic which simplifiys a K map by identifying the simplest loops.
class MapLogic:
    #initialises the function
    def __init__(self):
        self.array_of_vals = None
        self.loops = []  #format = [x, y]

    #gets all possible loops and then simplifies them
    def get_loops(self, array_of_vals):
        self.loops = []
        self.array_of_vals = array_of_vals
        
        self.loop_single()
        self.loops2()
        self.square_loops()
        self.loops4()
        self.loop16()
        self.rect_loops()
        self.loop_all()
        self.flip_pos()
        self.remove_looped_duplicates()
        #simplification step runs twice to double check all loops have been removed.
        self.simplify_loops()
        self.simplify_loops()
        #removes redundant loops
        self.remove_looped_duplicates()
        #returns the simplest loops back to the main program
        return self.loops
    
    #finds all loops made up of one singular term
    def loop_single(self):
        for i in range(len(self.array_of_vals)):
            for j in range(len(self.array_of_vals[i])):
                if self.array_of_vals[i][j]:
                    self.loops.append([[j, i]])

    #Finds all loops made up of 2 terms including loops that wrap around.
    def loops2(self):
        for i in range (len(self.array_of_vals)):
            for j in range (len(self.array_of_vals[i])):
                if self.array_of_vals[i][j]:
                    if j != len(self.array_of_vals[i])-1:
                        if self.array_of_vals[i][j+1]:
                            self.loops.append([[j, i], [j+1, i]])
                    else:
                        next_j = 0
                        if self.array_of_vals[i][next_j]:
                            self.loops.append([[j, i],[next_j, i]])
                    
                    if i != len(self.array_of_vals)-1:
                        if self.array_of_vals[i+1][j]:
                            self.loops.append([[j, i], [j, i+1]])
                    else:
                        next_i = 0
                        if self.array_of_vals[next_i][j]:
                            self.loops.append([[j, i], [j, next_i]])

    #checks all vertical 1x4 loops
    def loops4vertical(self, i):
        for ls in self.array_of_vals:
            if not ls[i]:
                return False
        return True
    
    #checks all horizontal 4x1 loops
    def loops4horizontal(self, i):
        print(self.array_of_vals[i])
        if not all(self.array_of_vals[i]):
            return False
        return True

    #creates all 1x4 or 4x1 loops
    def loops4(self):
        for i in range(len(self.array_of_vals[0])):
            if self.loops4vertical(i):
                array_of_line = []
                for j in range(len(self.array_of_vals)):
                    array_of_line.append([i,j])
                self.loops.append(array_of_line)
            
        for i in range(len(self.array_of_vals)):
            if self.loops4horizontal(i):
                array_of_line = []
                for j in range(len(self.array_of_vals[0])):
                    array_of_line.append([j, i])
                self.loops.append(array_of_line)
    
    #creates a loop of all values if true
    def loop16(self):
        if self.all_pos():
            temp_ls = []
            for i in range(len(self.array_of_vals)):
                for j in range (len(self.array_of_vals[i])):
                    temp_ls.append([j, i])
            self.loops.append(temp_ls)
    
    #creates a loop of 2x2 
    def square_loops(self):
        for i in range(len(self.array_of_vals)):
            for j in range(len(self.array_of_vals[i])):
                next_i = (i + 1) % len(self.array_of_vals)
                next_j = (j + 1) % len(self.array_of_vals[0])

                if (self.array_of_vals[i][j] and
                    self.array_of_vals[i][next_j] and self.array_of_vals[next_i][j] and self.array_of_vals[next_i][next_j]):

                    self.loops.append([[j, i], [next_j, i], [next_j, next_i], [j, next_i]])
    
    #creates a loop of 2x4
    def rect_loops(self):
        rows = len(self.array_of_vals)
        cols = len(self.array_of_vals[0])

        for i in range(rows):
            next_i = (i + 1) % rows
            if self.loops4horizontal(i) and self.loops4horizontal(next_i):
                temp_ls = []
                for j in range(cols):
                    temp_ls.append([j, i])
                    temp_ls.append([j, next_i])
                self.loops.append(temp_ls)

        for i in range(cols):
            next_j = (i + 1) % cols
            if self.loops4vertical(i) and self.loops4vertical(next_j):
                temp_ls = []
                for j in range(rows):
                    temp_ls.append([i, j])
                    temp_ls.append([next_j, j])
                self.loops.append(temp_ls)

    #checks if all positions are the same
    def all_pos(self):
        for i in self.array_of_vals:
            if not all(i):
                return False
        return True
    
    #checks if all values are the same
    def all_true(self):
        for ls in self.array_of_vals:
            if not all(ls):
                return False
        return True
    
    #loops all values
    def loop_all(self):
        if self.all_true():
            temp_ls = []
            for i in range(len(self.array_of_vals)):
                for j in range(len(self.array_of_vals[i])):
                    temp_ls.append([j, i])
            self.loops.append(temp_ls)
                
    #flips the value of x and y due to erros in logic in code above
    def flip_pos(self):
        rows = len(self.array_of_vals)
        cols = len(self.array_of_vals[0])
        for i in range(len(self.loops)):
            for j in range(len(self.loops[i])):
                if self.loops[i][j][0] == -1:
                    self.loops[i][j][0] = rows - 1
                if self.loops[i][j][1] == -1:
                    self.loops[i][j][1] = cols - 1

    #removes any loops that have been duplicated due to ordering.
    def remove_looped_duplicates(self):
        for ls in self.loops:
            ls.sort()
        temp_ls = []
        
        for i in range(len(self.loops)):
            if self.loops[i] not in temp_ls:
                temp_ls.append(self.loops[i])
        
        self.loops = temp_ls
            
    #creates simplified loops and removes loop redundencies
    def simplify_loops(self):
        
        result = []
        sets = [set(tuple(x) for x in loop) for loop in self.loops]

        for i, loop_set in enumerate(sets):
            contained = False
            for j, other_set in enumerate(sets):
                if i != j and loop_set.issubset(other_set):
                    contained = True
                    break
            if not contained:
                result.append(list(loop_set))
        
        self.loops = result
        
        self.remove_redundant_loops()

        ls = []
        for loop in self.loops:
            lp = []
            for item in loop:
                if item != 0:
                    lp.append(list(item))
            ls.append(lp)
        self.loops = ls

    #removes redundant loops
    def remove_redundant_loops(self):
        ls = []
        self.loops.sort(key=len, reverse=False)
        for i in range(len(self.loops)):
            ls.append([])
            for j in range(len(self.loops[i])):
                ls[i].append(0)
                for k in range(len(self.loops)):
                    if i != k:
                        if self.loops[i][j] in self.loops[k]:
                            ls[i][j] = 1
            
            if all(ls[i]):
                self.loops[i] = [0]
                    
#test case
k = MapLogic()
k.get_loops([[1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]])