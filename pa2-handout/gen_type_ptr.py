#!/usr/bin/python3
import random

if __name__ == "__main__":
    # random.seed()
    total_statements = 100
    variables_per_type = 10
    total_types = 10
    max_order = 8

    TYPE_OFFSET = 1000
    
    print('p {} {}'.format(variables_per_type * total_types, total_statements))

    for i in range(total_types):
        for j in range(variables_per_type):
            print('t {} {}'.format(i * TYPE_OFFSET + 1 + j, i))

    for i in range(total_statements):
        l_type = int(random.random() * (total_types))
        r_type = int(random.random() * (total_types))
        t_type = int(random.random() * min(l_type + 1, r_type + 2))

        l_val = l_type * TYPE_OFFSET + 1 + int(random.random() * (variables_per_type))
        r_val = r_type * TYPE_OFFSET + 1 + int(random.random() * (variables_per_type))

        l_order = l_type - t_type
        r_order = r_type - t_type
        
        print('s {} {} {} {}'.format(l_order, l_val, r_order, r_val))
