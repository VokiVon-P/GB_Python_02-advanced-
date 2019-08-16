import pytest
from datetime import datetime
from .routes import actionmapping
from .controllers import echo_controller


@pytest.fixture
def initial_action():
    return actionmapping[0].get('action')


@pytest.fixture
def initial_code():
    return 200


@pytest.fixture
def initial_data():
    return 'Test echo data'


@pytest.fixture
def initial_request(initial_action, initial_data):
    return {
        'action': initial_action,
        'time': datetime.now().timestamp(),        
        'data': initial_data
    }


def test_action_echo_controller(initial_request, initial_action):
    actual_response = echo_controller(initial_request)
    assert actual_response.get('action') == initial_action


def test_code_echo_controller(initial_request, initial_code, initial_data):
    actual_response = echo_controller(initial_request)
    assert actual_response.get('code') == initial_code


def test_data_echo_controller(initial_request, initial_code, initial_data):
    actual_response = echo_controller(initial_request)
    assert actual_response.get('data') == initial_data
    