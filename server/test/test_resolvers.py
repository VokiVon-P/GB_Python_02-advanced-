import pytest

from resolvers import resolve, get_server_action


@pytest.fixture
def initial_action():
    return 'echo1'



def test_resolve(initial_action):
    assert resolve(initial_action) is None


def test_get_server_action():
    apps = get_server_action()
    assert apps is not None
    

    
    