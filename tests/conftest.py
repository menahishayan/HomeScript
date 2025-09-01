"""Shared pytest fixtures for the homescript test suite."""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock
from typing import Dict, Any

import pytest


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_config():
    """Provide a mock configuration dictionary."""
    return {
        'host': 'localhost',
        'port': 8080,
        'username': 'test_user',
        'password': 'test_pass',
        'timeout': 30
    }


@pytest.fixture
def mock_requests_session():
    """Provide a mock requests session."""
    session = Mock()
    session.get.return_value = Mock()
    session.post.return_value = Mock()
    session.put.return_value = Mock()
    session.delete.return_value = Mock()
    return session


@pytest.fixture
def mock_response():
    """Provide a mock HTTP response."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'status': 'success'}
    response.text = '{"status": "success"}'
    response.headers = {'Content-Type': 'application/json'}
    return response


@pytest.fixture
def mock_environment(monkeypatch):
    """Provide a clean environment for testing."""
    test_env = {
        'HOME': '/tmp/test_home',
        'PATH': '/usr/local/bin:/usr/bin:/bin'
    }
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    return test_env


@pytest.fixture
def sample_device_data():
    """Provide sample device data for testing."""
    return {
        'devices': [
            {
                'id': 'device_1',
                'name': 'Test Device 1',
                'type': 'switch',
                'state': 'on'
            },
            {
                'id': 'device_2', 
                'name': 'Test Device 2',
                'type': 'sensor',
                'value': 25.5
            }
        ]
    }


@pytest.fixture
def mock_file_system(tmp_path):
    """Provide a mock file system structure."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    
    return {
        'base': tmp_path,
        'config': config_dir,
        'data': data_dir,
        'logs': log_dir
    }


@pytest.fixture(scope="session")
def test_data_dir():
    """Provide path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def mock_logger():
    """Provide a mock logger."""
    logger = Mock()
    logger.info = Mock()
    logger.warning = Mock()
    logger.error = Mock()
    logger.debug = Mock()
    return logger


@pytest.fixture
def disable_network_calls(monkeypatch):
    """Disable actual network calls during testing."""
    import requests
    
    def mock_request(*args, **kwargs):
        raise RuntimeError("Network calls are disabled in tests")
    
    monkeypatch.setattr(requests, "get", mock_request)
    monkeypatch.setattr(requests, "post", mock_request)
    monkeypatch.setattr(requests, "put", mock_request)
    monkeypatch.setattr(requests, "delete", mock_request)


@pytest.fixture
def capsys_disabled(capsys):
    """Fixture to temporarily disable capsys when needed."""
    with capsys.disabled():
        yield capsys