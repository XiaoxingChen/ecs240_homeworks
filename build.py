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

solution_files = {
    'pa1-handout': ['build.sh', 'main.py', 'run.sh'],
    'pa2-handout': [ 
        os.path.join('andersen', 'build.sh'), 
        os.path.join('andersen', 'main.py'), 
        os.path.join('andersen', 'run.sh'),
        os.path.join('typed', 'build.sh'), 
        os.path.join('typed', 'main.py'), 
        os.path.join('typed', 'run.sh')]}

class BuildDirectory():
    def __init__(self, target_folder_name):
        self.target_basename = target_folder_name
        self.script_folder = os.path.abspath(os.path.dirname(__file__))
        self.build_root = os.path.join(self.script_folder, 'build')
        self.assignment_folder = os.path.join(self.script_folder, target_folder_name)
        self.output_zip_name = os.path.join(self.build_root, target_folder_name.replace('handout', 'solution') + '.zip')
        self.assignment_test_script = os.path.join(self.assignment_folder, 'test_main.py')
    

def runCompress(dirs):
    os.makedirs(dirs.build_root, exist_ok=True)
    with ZipFile(dirs.output_zip_name, 'w') as f:
        f.write(os.path.join(dirs.script_folder, 'team.txt'), 'team.txt')
        for filename in solution_files[dirs.target_basename]:
            f.write(os.path.join(dirs.assignment_folder, filename), filename)
    print("Solution file generated at: " + dirs.output_zip_name)

def runTest(dirs):
    print("Run test cases...")
    exit_code = os.system("python3 {}".format(dirs.assignment_test_script))
    if(exit_code != 0):
        raise RuntimeError('unit test failed')

def runTestOnCSIF(dirs):
    csif_host_name = 'pc22.cs.ucdavis.edu'
    csif_user_name = input("Input your csif username: ")
    shell_cmds = [
    'rm -rf ecs240_homeworks',
    'git clone git@github.com:XiaoxingChen/ecs240_homeworks.git', 
    'cd ecs240_homeworks', 
    './build.py --test {}'.format(dirs.target_basename), 'exit']
    shell_cmd = '&&'.join(shell_cmds)
    ssh_cmd = 'ssh {}@{} "{}"'.format(csif_user_name, csif_host_name, shell_cmd)
    exit_code = os.system(ssh_cmd)
    if(exit_code != 0):
        raise RuntimeError('unit test failed')
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean', action='store_true', help='Clean build folder')
    parser.add_argument('target_folder', nargs=1, help="Name of the target homework folder")
    parser.add_argument('--test', action='store_true', help='Run test cases')
    parser.add_argument('--compress', action='store_true', help='Compress homework file')
    parser.add_argument('--test-on-csif', action='store_true', help='Run test cases on csif')
    args = parser.parse_args()

    target_folder = os.path.normpath(args.target_folder[0])

    dirs = BuildDirectory(target_folder) 

    if args.clean:
        shutil.rmtree(dirs.build_root, ignore_errors=True)
        quit()

    if args.test or args.compress:
        runTest(dirs)

    if args.test_on_csif:
        runTestOnCSIF(dirs)
    
    if args.compress:
        runCompress(dirs)