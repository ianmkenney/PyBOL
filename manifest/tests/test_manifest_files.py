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
