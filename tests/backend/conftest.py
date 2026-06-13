import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def reset_app_state():
    """Reset the in-memory app state before and after each test."""
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))

    yield

    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def client(reset_app_state):
    """Provide a FastAPI test client with isolated app state."""
    return TestClient(app)
