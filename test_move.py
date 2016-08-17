import Manifest
import tempfile

class Test_Move(object):
    
    def Setup(self):
        self.dir = tempfile.mkdtemp()

    def test_load_yaml(self):
        m = Manifest.Manifest('manifest.yml')
        m._check_broken_manifest()

