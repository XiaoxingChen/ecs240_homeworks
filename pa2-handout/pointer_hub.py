class PointerHub():
    """
    For Monte Carlo test
    """
    def __init__(self, all_vars):
        self.point_to = {var: None for var in all_vars}

    def update(self, statement):
        """
        return: 
            2-tuple, if statement updated
            None, if nullptr
        """
        l_order, l_var, r_order, r_var = statement
        for i in range(l_order):
            l_var = self.point_to[l_var]
            if l_var is None:
                return None

        for i in range(r_order + 1):
            r_var = self.point_to[r_var]
            if r_var is None:
                return None

        self.point_to[l_var] = r_var
        return (l_var, r_var)