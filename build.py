#!/usr/bin/python3
import argparse
import os
import shutil
from zipfile import ZipFile

def handleAutoComplete():
    if sys.platform == 'linux':
        complete_cmd = 'complete -F _longopt {}'.format(os.path.basename(__file__))
        bashrc_path = os.path.expanduser('~/.bashrc')
        with open(bashrc_path) as f:
            if not complete_cmd in f.read():
                os.system('echo "{}" >> {}'.format(complete_cmd, bashrc_path))
    else:
        pass

solution_files = {'pa1-handout': ['build.sh', 'main.py', 'run.sh']}

class BuildDirectory():
    def __init__(self, target_folder_name):
        self.target_basename = target_folder_name
        self.script_folder = os.path.abspath(os.path.dirname(__file__))
        self.build_root = os.path.join(self.script_folder, 'build')
        self.assignment_folder = os.path.join(self.script_folder, target_folder_name)
        self.output_zip_name = os.path.join(self.build_root, target_folder_name.replace('handout', 'solution') + '.zip')
        self.assignment_test_script = os.path.join(self.assignment_folder, 'test_main.py')
    

def runBuild(dirs):
    os.makedirs(dirs.build_root, exist_ok=True)
    with ZipFile(dirs.output_zip_name, 'w') as f:
        f.write(os.path.join(dirs.script_folder, 'team.txt'), 'team.txt')
        for filename in solution_files[dirs.target_basename]:
            f.write(os.path.join(dirs.assignment_folder, filename), filename)

def runTest(dirs):
    print("Run test cases...")
    exit_code = os.system("python3 {}".format(dirs.assignment_test_script))
    if(exit_code != 0):
        raise RuntimeError('unit test failed')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean', action='store_true', help='Clean build folder')
    parser.add_argument('target_folder', nargs=1, help="Name of the target homework folder")
    parser.add_argument('--test', action='store_true', help='Run test cases')
    args = parser.parse_args()

    target_folder = os.path.normpath(args.target_folder[0])

    dirs = BuildDirectory(target_folder) 

    if args.clean:
        shutil.rmtree(dirs.build_root, ignore_errors=True)
        quit()

    
    runBuild(dirs)
    if args.test:
        runTest(dirs)

    
