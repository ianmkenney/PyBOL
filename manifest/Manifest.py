import sys
import yaml
import os
import shutil
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("manifest")
logger.info("Starting manifest logging")

class Manifest(object):
    """Tool for managing a multistate workflow. Requires a properly formatted
    manifest file; see example.
    """

    states = {}
    
    def __init__(self, filename=None):
        if filename:
            try:
                logger.info('Loading manifest file \'{}\''.format(filename))
                with open(filename, 'r') as f:
                    raw = yaml.load(f)
                    self._path = raw.pop('path')
                logger.info('Loaded manifest file')
            except IOError as e:
                logger.error('Could not open file \'{}\''.format(filename))
                raise
            except KeyError as e:
                logger.error('No path provided. Check manifest file')
                raise
            logger.info('Building states')
            self._build_states(raw)
            logger.info('States built')
    
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    def assemble(self, state, dest):
        """Builds the specified state.

        Keyword arguments:
        state -- a state from the manifest file.
        dest -- destination path.
        """
        logger.info('Assembling state \'{}\''.format(state))
        self.states[state].assemble(self._path, dest)
        logger.info('Assembled state \'{}\''.format(state))

    def _build_states(self, data):
        """Iterates through all states in the manifest file and populates the 
        states dictionary.

        Keyword arguments:
        data -- dictionary containing all of the state information.
        """
        for key in data:
            self.states[key] = State(self._path, key, data[key])

    def _check_broken_manifest(self):
        self.broken = False
        for state in self.states:
            if self.states[state].broken:
                self.broken = True
                logger.warning('State {} is broken.'.format(state))
        if self.broken:
            raise Exception
                
                                                
class State(object):

    def __init__(self, path, name, values):
        self.name = name

        if not values:
            logger.error('State {} missing content'.format(name))
            raise ValueError

        try:
            self.file_list = values.pop('files')
            logger.info('\033[4m'+"Checking state integrity ({}):".format(self.name)+'\033[0m')
            broken = False

            for f in self.file_list:
                exists = os.path.exists(os.path.join(path, name, f[0]))
                if not exists:
                    logger.warning('{} does not exist'.format(os.path.join(path, name, f[0])))
                    broken = True
                logger.info("   {1:17} <-- {0}".format(f[0], self._format_integrity(exists)))
        except KeyError:
            logger.error(name, 'missing file list.')
            raise

        self.broken = broken

        
    def assemble(self, src_path, dest):
        """Builds a state according to the information provided in the
        manifest file.

        Keyword arguments:
        src_path -- path containing all of the states.
        dest -- destination path. 
        """
        for f in self.file_list:
            print(f)
            src_path_f = os.path.join(src_path, self.name, f[0])
            dest_f = os.path.join(dest, f[1])
            logger.info("Copying from {0} --> {1}".format(src_path_f,dest_f))
            if not os.path.exists(os.path.dirname(dest_f)):
                logger.info("Creating directory tree")
                os.makedirs(os.path.dirname(dest_f))
            
            if os.path.isdir(src_path_f):
                shutil.copytree(src_path_f,dest_f)
            else:
                shutil.copyfile(src_path_f, dest_f)
        logger.info("{0} build complete...".format(self.name))

    def _format_integrity(self, exists):
        
        message = {True  : '\033[92mFound\033[0m',
                   False : '\033[91mMissing\033[0m',
        }

        return message[exists]
