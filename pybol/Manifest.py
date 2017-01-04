"""
:mod:`pybol.Manifest` --- Ship states
====================================

The :mod:`pybol.Manifest` allows streamlined movement of large sets of file structures (states).

.. autoclass:: Manifest
.. autoclass:: State

"""


import sys
import yaml
import os
import shutil
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PyBOL")
logger.info("Starting PyBOL logging")

class Manifest(object):
    """Tool for managing a multistate workflow.

    Parameters
    ----------
    filename : str (optional)
        Path to a predefined manifest in YAML format

    Attributes
    ----------
    states : dict
        Dictionary containing state definitions
    """

    def __init__(self, filename=None):
        self._states = {}
        if filename:
            self.load_manifest_file(filename)
        else:
            logger.info('Creating empty manifest')

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, states):
        if isinstance(states, dict):
            if len(states):
                for s in states:
                    if not isinstance(states[s], State):
                        logger.error('State dict can only contain state objects')
                        raise TypeError('State dict can only contain state objects')
                self._states = states
            else:
                self._states = {}
        else:
            logger.error('state attribute must be specified in a dict')
            raise TypeError('States must be held in a dict')

    def load_manifest_file(self, filename):
        """Loads a manifest file.

        Parameters
        ----------
        filename : str
            Path to the manifest file

        """
        try:
            logger.info('Loading manifest file \'{}\''.format(filename))
            with open(filename, 'r') as f:
                raw = yaml.load(f)
            logger.info('Loaded manifest file')
        except IOError as e:
            logger.error('Could not open file \'{}\''.format(filename))
            raise
        logger.info('Building states')
        self._build_states(raw)
        logger.info('States built')

    def add_state(self, name, path=None, files=[], force=False):
        """Add a state to the manifest.

        Parameters
        ----------
        name : str
            The name of the state to be added
        files : [str] (optional)
            The paths of the files defining the state
        path : str (optional)
            The path the the top level directory, default behavior determines
            this value based on the paths of the files provided.
        force : bool (optional)
            Add new state even if state name exists
        
        """
        if not name in self._states or force:
            self._states[name] = State(name, path=path, files=files)
            logger.info('State \'{}\' added'.format(name))
        else:
            logger.error('State {} already exists'.format(name))

    def remove_state(self, name):
        """Removes a state from the manifest.

        Parameters
        ----------
        name : str
            The name of the state to be removed

        """
        try:
            logger.info('Removing state:', name)
            self._states.pop(name)
        except KeyError:
            logger.error('No state found:', name)

    def clear_states(self):
        """Removes all states from the manifest

        """
        self.states.clear()

    def assemble(self, state, dest):
        """Builds the specified state.

        Parameters
        ----------
        state : str
            A state name held in the manifest
        dest : 
            destination path

        """
        logger.info('Assembling state \'{0}\' in \'{1}\''.format(state,dest))
        self.states[state].assemble(self.path, dest)
        logger.info('Assembled state \'{}\''.format(state))

    def _build_states(self, data):
        """Iterates through all states in the manifest file and populates the 
        states dictionary.

        Parameters
        ----------
        data : dict
            dictionary containing all of the state information.

        """

        try:
            logger.info('Looking for path information.')
            self.path = data.pop('path')
            logger.info('Setting manifest path to \'{}\''.format(self.path))
        except Exception as e:
            raise e
            
        for key in data:
            try:
                try:
                    state_path = data[key].pop('path')
                except:
                    state_path = ''
                self.add_state(key, files=data[key]['files'], path=os.path.join(self.path, key, state_path), force=True)
            except TypeError:
                logger.error('Missing file list in state \'{}\''.format(key))
                raise

    def dump(self, filename):
        """Create a manifest file using the current manifest definition

        Parameters
        ----------
        filename : str
            Destination path for the manifest file

        """
        raise NotImplementedError

    def __len__(self):
        return len(self.states)
                
                                                
class State(object):

    def __init__(self, name, files=[], path=None, full_transfer=False):
        self._name = name
        self._files = files
        self._path = path
        self._full_transfer = full_transfer


        if not path and files:
            self.determine_path()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        if isinstance(new_path, str):
            logger.info('Setting state path to {}'.format(new_path))
            self._path = new_path
        else:
            logger.error('Could not set state path. Must be a string')
            raise ValueError

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            logger.info('Setting state name to {}'.format(name))
            self._name = name
        else:
            logger.error('Could not set state name. Must be a string')
            raise ValueError

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, files):
        self._files = files

    def determine_path(self):
        self.path = os.path.commonprefix([f[0] for f in self.files])

    def clear_files(self):
        """Clears the files held in the state

        """
        del self.files[:]

    def assemble(self, src_path, dest):
        """Builds a state based on its definition.

        Parameters
        ----------
        src_path : str 
            path containing all of the states
        dest : str
            destination path

        """
        
        for f in self.files:
            src_path_f = os.path.join(self.path, f[0])
            dest_f = os.path.join(dest, f[1])
            logger.info("Copying from {0} --> {1}".format(src_path_f,dest_f))
            if not os.path.exists(os.path.dirname(dest_f)):
                logger.info("Creating directory tree")
                os.makedirs(os.path.dirname(dest_f))
            
            if os.path.isdir(src_path_f):
                if os.path.exists(dest_f):
                    shutil.rmtree(dest_f)
                shutil.copytree(src_path_f,dest_f)
            else:
                shutil.copyfile(src_path_f, dest_f)

        logger.info("{0} build complete...".format(self.name))

    def __str__(self):
        return "{0} -- {1}".format(self.name, self.files)

    def __len__(self):
        return len(self.files)
