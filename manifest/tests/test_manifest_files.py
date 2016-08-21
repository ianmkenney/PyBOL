import tempfile
import manifest
import os

class Test_Manifest_Files(object):
    
    def setup(self):
        self.dir = tempfile.mkdtemp()
        self.manifests_path = 'manifest/tests/testing_files/manifests'

    def test_good_yaml(self):
        m = manifest.Manifest(os.path.join(self.manifests_path,'good_manifest.yml'))
        assert True

    def test_bad_yaml(self):
        try:
            m = manifest.Manifest(os.path.join(self.manifests_path,'bad_manifest.yml'))
            assert False
        except KeyError:
            assert True

    def test_no_yaml(self):
        try:
            m = manifest.Manifest("some/manifest.yml")
            assert False
        except IOError:
            assert True

    def test_missing_files(self):
        try:
            m = manifest.Manifest(os.path.join(self.manifests_path,'missing_files.yml'))
            assert False
        except KeyError:
            assert True

    def test_missing_content(self):
        try:
            m = manifest.Manifest(os.path.join(self.manifests_path,'missing_state_content.yml'))
            assert False
        except ValueError:
            assert True

    def test_recursion(self):
        try:
            m = manifest.Manifest(os.path.join(self.manifests_path,'recursion.yml'))
            m.assemble('recursion',self.dir)
        except:
            assert False

    def test_regular_files(self):
        try:
            m = manifest.Manifest(os.path.join(self.manifests_path,'good_manifest.yml'))
            m.assemble('state_a',self.dir)
            m.assemble('state_b',self.dir)
        except:
            assert False
