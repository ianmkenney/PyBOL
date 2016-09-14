import tempfile
import pybol
import os

class Test_Manifest_Files(object):
    
    def setup(self):
        self.dir = tempfile.mkdtemp()
        self.manifests_path = 'pybol/tests/testing_files/manifests'

    def test_good_yaml(self):
        m = pybol.Manifest(filename=os.path.join(self.manifests_path,'good_manifest.yml'))
        assert True
    
    def test_path(self):
        m = pybol.Manifest(filename=os.path.join(self.manifests_path,'good_manifest.yml'))
        assert m.path == 'pybol/tests/testing_files/testing_states'
        assert os.path.exists(m.path)

    def test_bad_yaml(self):
        try:
            m = pybol.Manifest(filename=os.path.join(self.manifests_path,'bad_manifest.yml'))
            assert False
        except KeyError:
            assert True

    def test_no_yaml(self):
        try:
            m = pybol.Manifest(filename="some/manifest.yml")
            assert False
        except IOError:
            assert True

    def test_missing_files(self):
        try:
            m = pybol.Manifest(filename=os.path.join(self.manifests_path,'missing_files.yml'))
            assert False
        except KeyError:
            assert True

    def test_missing_content(self):
        try:
            m = pybol.Manifest(os.path.join(self.manifests_path,'missing_state_content.yml'))
            assert False
        except TypeError:
            assert True

    def test_recursion(self):
        try:
            m = pybol.Manifest(os.path.join(self.manifests_path,'recursion.yml'))
            m.assemble('recursion',self.dir)
        except:
            assert False

    def test_regular_files(self):
        try:
            m = pybol.Manifest(filename=os.path.join(self.manifests_path,'good_manifest.yml'))
            m.assemble('state_a',self.dir)
            m.assemble('state_b',self.dir)
        except:
            assert False

    def test_full_transfer_option(self):
        try:
            m = pybol.Manifest(filename=os.path.join(self.manifests_path,'full_transfer.yml'))
            m.assemble('state_a',self.dir)
            assert len(os.listdir(self.dir)) > 0
        except: 
            assert False
