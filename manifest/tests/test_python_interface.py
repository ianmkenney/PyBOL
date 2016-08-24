import manifest

class Test_Python_Interface(object):

    def test_empty_manifest(self):
        try:
            m = manifest.Manifest()
            assert True
        except:
            assert False

    def test_set_path_after_instantiation(self):
        try:
            m = manifest.Manifest()
            m.path = '/some/absolute/path'
            assert True
        except:
            assert False

    def test_set_states_empty(self):
        try:
            m = manifest.Manifest()
            m.states = {}
            assert m.states == {}
        except:
            assert False

    def test_set_states_list(self):
        try:
            m = manifest.Manifest()
            m.states = []
            assert False
        except TypeError:
            assert True

    def test_set_states(self):
        try:
            m = manifest.Manifest()
            m.states = {'state_a':manifest.State('state_a')}
            assert True
        except:
            assert False

    def test_set_states_no_state(self):
        try:
            m = manifest.Manifest()
            m.states = {'state_a':{'files':None}}
            assert False
        except TypeError:
            assert True

    def test_remove_state(self):
        m = manifest.Manifest()
        m.states = {'state_a':manifest.State('state_a')}
        m.remove_state('state_a')
        assert len(m) == 0 

    def test_remove_fake_state(self):
        m = manifest.Manifest()
        m.states = {'state_a':manifest.State('state_a')}
        m.remove_state('state_b')
        assert len(m) == 1

    def test_set_bad_name(self):
        m = manifest.Manifest()
        m.states = {'state_a':manifest.State('state_a')}
        try:
            m.states['state_a'].name = ['not a string']
            assert False
        except ValueError:
            assert True

    def test_clear_files(self):
        s = manifest.State('state',files=[['a'],['b']])
        assert len(s) == 2
        s.clear_files()
        assert len(s) == 0 

    def test_print(self):
        try:
            s = manifest.State('state',files=[['a'],['b']])
            print(s)
            assert True
        except:
            assert False
        
