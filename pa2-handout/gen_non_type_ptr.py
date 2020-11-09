#!/usr/bin/python3
import random

if __name__ == "__main__":
    # random.seed()
    total_statements = 40
    total_variables = 10
    max_order = 6
    
    # numbers = [i + 1 for i in range(total_variables)]
    # order_range = [i for i in range(max_order + 1)]
    
    print('p {} {}'.format(total_variables, total_statements))
    for i in range(total_statements):
        l_order = int(random.random() * (max_order))
        l_val = 1 + int(random.random() * (total_variables))
        r_order = int(random.random() * (max_order)) - 1
        r_val = 1 + int(random.random() * (total_variables))
        print('s {} {} {} {}'.format(l_order, l_val, r_order, r_val))
