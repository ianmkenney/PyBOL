import sys
import yaml
import os
import shutil

class Manifest(object):
    """Tool for managing a multistate workflow. Requires a properly formatted
    manifest file; see example.
    """

    states = {}
        
    def __init__(self, filename):
        try:
            with open(filename, 'r') as f:
                raw = yaml.load(f)
            self.src_path = raw.pop('path')
        except IOError:
            print('Cannot open', filename)
            raise FileNotFoundError
        except KeyError:
            print('No path provided. Check manifest file.')
            raise KeyError

        self._build_states(raw)

    def assemble(self, state, dest):
        """Builds the specified state.

        Keyword arguments:
        state -- a state from the manifest file.
        dest -- destination path.
        """
        self.states[state].assemble(self.src_path, dest)

    def _build_states(self, data):
        """Iterates through all states in the manifest file and populates the 
        states dictionary.

        Keyword arguments:
        data -- dictionary containing all of the state information.
        """
        for key in data:
            self.states[key] = State(self.src_path, key, data[key])

    def _check_broken_manifest(self):
        self.broken = False
        for state in self.states:
            if self.states[state].broken:
                self.broken = True
                print('State {} is broken.'.format(state))
        if self.broken:
            raise Exception
                
                                                
class State(object):

    def __init__(self, path, name, values):
        self.name = name
        try:
            self.file_list = values.pop('files')
            print('\n\033[4m'+"Checking state integrity ({}):".format(self.name)+'\033[0m')
            broken = False

            for f in self.file_list:
                exists = os.path.exists(os.path.join(path, name, f[0]))
                if not exists:
                    broken = True
                print("   {1:17} <-- {0}".format(f[0], self._format_integrity(exists)))
        except KeyError:
            print(name, 'missing file list.')

        self.broken = broken

        
    def assemble(self, src_path, dest):
        """Builds a state according to the information provided in the
        manifest file.

        Keyword arguments:
        src_path -- path containing all of the states.
        dest -- destination path. 
        """

        for f in self.file_list:
            src_path_f = os.path.join(src_path, self.name, f[0])
            dest_f = os.path.join(dest, f[1])
            if not os.path.exists(os.path.dirname(dest_f)):
                os.makedirs(os.path.dirname(dest_f))
            shutil.copyfile(src_path_f, dest_f)
        print("{0} build complete...".format(self.name))

    def _format_integrity(self, exists):
        self.colors = {True  : '\033[92m',
                  False : '\033[91m',
        }
        
        message = {True  : 'Found',
                   False : 'Missing',
        }

        return self.colors[exists]+message[exists]+'\033[0m'
