import os
import requests
from behave import fixture, use_fixture


def wait_for_api(base_url, timeout=30):
    import time
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False


@fixture
def api_client(context):
    context.base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
    context.health_url = os.getenv("API_BASE_URL", "http://localhost:8000")

    if not wait_for_api(context.health_url):
        raise RuntimeError("API server is not responding. Make sure docker-compose is running.")

    context.response = None
    context.created_ids = []
    context.created_session_ids = []

    yield context

    for session_id in context.created_session_ids:
        try:
            requests.delete(f"{context.base_url}/chat/sessions/{session_id}")
        except Exception:
            pass

    for obj_id in context.created_ids:
        try:
            requests.delete(f"{context.base_url}/objectives/{obj_id}")
        except Exception:
            pass


def before_all(context):
    use_fixture(api_client, context)


def after_scenario(context, scenario):
    if hasattr(context, 'created_session_ids'):
        for session_id in context.created_session_ids:
            try:
                requests.delete(f"{context.base_url}/chat/sessions/{session_id}")
            except Exception:
                pass
        context.created_session_ids = []

    if hasattr(context, 'created_ids'):
        for obj_id in context.created_ids:
            try:
                requests.delete(f"{context.base_url}/objectives/{obj_id}")
            except Exception:
                pass
        context.created_ids = []
