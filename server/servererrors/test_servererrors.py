import pytest
from datetime import datetime
from .routes import actionmapping
from .controllers import get_server_errors


@pytest.fixture
def initial_action():
    return actionmapping[0].get('action')


@pytest.fixture
def initial_data():
    return 'Test server error'


@pytest.fixture
def initial_request(initial_action, initial_data):
    return {
        'action': initial_action,
        'time': datetime.now().timestamp(),        
        'data': initial_data
    }


def test_servererrors_get_server_errors(initial_request):
    try:
        get_server_errors(initial_request)
    except Exception as e:
        assert str(e) == 'Custom server error'


