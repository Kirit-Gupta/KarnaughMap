class Parse:
    VARIABLES = {'A', 'B', 'C', 'D'}

    def __init__(self, expression):
        self.expression = expression
        self.boolean_comb_table = None
        self.func = self.parse_expression(expression)
    
    def _get_var_count(self):
        #unique_vars = set()
        #for char in self.expression:
        #    if char.isalpha() and char.isupper():
        #        unique_vars.add(char)
        unique_vars = 4
        return (unique_vars)
    
    def set_map_size(self):
        return self._get_var_count()

    def get_boolean_combs(self):
        expression = ['00', '01', '11', '10']
        two_expression = ['0', '1']
        bool_ls = []
        if self.set_map_size() == 4:
            for ex1 in expression:
                for ex2 in expression:
                    bool_ls.append(ex2+ex1)
        elif self.set_map_size() == 3:
            for ex1 in two_expression:
                for ex2 in expression:
                    bool_ls.append(ex2 + ex1)
        elif self.set_map_size() == 2:
            for ex1 in two_expression:
                for ex2 in two_expression:
                    bool_ls.append(ex2 + ex1)
        
        boolean_ls = []
        for item in bool_ls:
            ls = []
            for exp in item:
                ls.append(bool(int(exp)))
            boolean_ls.append(tuple(ls))
        
        return boolean_ls


    def parse_expression(self, expr):
        terms = []
        depth = 0
        start = 0

        for i, char in enumerate(expr):
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            elif char == '+' and depth == 0:
                terms.append(expr[start:i])
                start = i + 1
        terms.append(expr[start:])

        term_funcs = [self.parse_term(t) for t in terms]
    
        return lambda a, b, c, d, tf=term_funcs: any(f(a, b, c, d) for f in tf)    
    
    def parse_term(self, term):
        factors = []
        i = 0
        while i < len(term):
            ch = term[i]
            if ch == '(':
                start = i + 1
                depth = 1
                while depth > 0:
                    i += 1
                    if term[i] == '(':
                        depth += 1
                    elif term[i] == ')':
                        depth -= 1
                inner = term[start:i]
                inner_f = self.parse_expression(inner)
                if i + 1 < len(term) and term[i+1] == "'":
                    factors.append(lambda a, b, c, d, f=inner_f: not f(a, b, c, d))
                    i += 1
                else:
                    factors.append(inner_f)

            elif ch in self.VARIABLES:
                if i + 1 < len(term) and term[i + 1] == "'":
                    factors.append(lambda a, b, c, d, v=ch: not {'A': a, 'B': b, 'C': c or False, 'D': d}[v])
                    i += 1
                else:
                    factors.append(lambda a, b, c, d, v=ch: {'A': a, 'B': b, 'C': c or False, 'D': d}[v])
            i += 1

        return lambda a, b, c, d, fs=factors: all(f(a, b, c, d) for f in fs)
    
    def return_logical_list(self):
        bool_ls = self.get_boolean_combs()

        for i in range(len(bool_ls)):
            bool_ls[i] = self.evaluate(*bool_ls[i])
        return bool_ls
        

    def evaluate(self, a = None, b = None, c = None, d = None):
        return self.func(a, b, c, d)
    
    
    

P = Parse("(A+A')'")
print(P.return_logical_list())