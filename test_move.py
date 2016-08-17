import Manifest
import tempfile

class Test_Move(object):
    
    def Setup(self):
        self.dir = tempfile.mkdtemp()

    def test_load_yaml(self):
        m = Manifest.Manifest('manifest.yml')
        assert True
