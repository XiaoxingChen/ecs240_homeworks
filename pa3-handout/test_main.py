import os
import sys
if __name__ == "__main__":
    script_folder = os.path.abspath(os.path.dirname(__file__))
    exit_code = 0
    print()
    exit_code += os.system('python3 {}'.format(os.path.join(script_folder,'faintvar', 'test_main.py')))
    exit_code += os.system('python3 {}'.format(os.path.join(script_folder,'reachingdef', 'test_main.py')))
    if exit_code != 0:
        quit(1)