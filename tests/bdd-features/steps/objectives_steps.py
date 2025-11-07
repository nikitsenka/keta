import requests
from behave import given, when, then
from uuid import UUID


@given('the API is running')
def step_api_is_running(context):
    response = requests.get(f"{context.health_url}/health")
    assert response.status_code == 200, "API is not running"


@when('I create an objective with the following data:')
def step_create_objective(context):
    data = {}
    for row in context.table:
        field = row['field']
        value = row['value']
        data[field] = value

    response = requests.post(
        f"{context.base_url}/objectives",
        json=data,
        headers={"Content-Type": "application/json"}
    )

    context.response = response
    context.response_json = response.json() if response.status_code in [200, 201] else None

    if context.response_json and 'id' in context.response_json:
        context.created_ids.append(context.response_json['id'])


@then('the response status code should be {status_code:d}')
def step_check_status_code(context, status_code):
    assert context.response.status_code == status_code, \
        f"Expected status code {status_code}, but got {context.response.status_code}. Response: {context.response.text}"


@then('the response should contain a valid objective ID')
def step_check_objective_id(context):
    assert context.response_json is not None, "Response JSON is None"
    assert 'id' in context.response_json, "Response does not contain 'id' field"

    try:
        UUID(context.response_json['id'])
    except ValueError:
        raise AssertionError(f"Invalid UUID format: {context.response_json['id']}")


@then('the objective {field} should be "{expected_value}"')
def step_check_objective_field(context, field, expected_value):
    assert context.response_json is not None, "Response JSON is None"
    assert field in context.response_json, f"Response does not contain '{field}' field"
    actual_value = context.response_json[field]
    assert actual_value == expected_value, \
        f"Expected {field} '{expected_value}', but got '{actual_value}'"


@given('I have created an objective with name "{name}"')
def step_create_objective_with_name(context, name):
    data = {
        "name": name,
        "description": f"Test objective: {name}",
        "domain": "test"
    }

    response = requests.post(
        f"{context.base_url}/objectives",
        json=data,
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 201, \
        f"Failed to create objective. Status: {response.status_code}, Response: {response.text}"

    context.response_json = response.json()
    context.objective_id = context.response_json['id']
    context.created_ids.append(context.objective_id)


@when('I upload a document with the following data:')
def step_upload_document(context):
    assert hasattr(context, 'objective_id'), "No objective_id found. Make sure to create an objective first."

    data = {}
    for row in context.table:
        field = row['field']
        value = row['value']
        data[field] = value

    response = requests.post(
        f"{context.base_url}/objectives/{context.objective_id}/sources",
        json=data,
        headers={"Content-Type": "application/json"}
    )

    context.response = response
    context.response_json = response.json() if response.status_code in [200, 201] else None

    if context.response_json and 'id' in context.response_json:
        context.source_id = context.response_json['id']


@then('the response should contain a valid source ID')
def step_check_source_id(context):
    assert context.response_json is not None, "Response JSON is None"
    assert 'id' in context.response_json, "Response does not contain 'id' field"

    try:
        UUID(context.response_json['id'])
    except ValueError:
        raise AssertionError(f"Invalid UUID format: {context.response_json['id']}")


@then('the source {field} should be "{expected_value}"')
def step_check_source_field(context, field, expected_value):
    assert context.response_json is not None, "Response JSON is None"
    assert field in context.response_json, f"Response does not contain '{field}' field"
    actual_value = context.response_json[field]
    assert actual_value == expected_value, \
        f"Expected {field} '{expected_value}', but got '{actual_value}'"


@given('I have uploaded a document with name "{name}" and content "{content}"')
def step_upload_document_with_name_and_content(context, name, content):
    assert hasattr(context, 'objective_id'), "No objective_id found. Make sure to create an objective first."

    data = {
        "name": name,
        "description": f"Test document: {name}",
        "content": content
    }

    response = requests.post(
        f"{context.base_url}/objectives/{context.objective_id}/sources",
        json=data,
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 201, \
        f"Failed to upload document. Status: {response.status_code}, Response: {response.text}"

    response_json = response.json()
    context.source_id = response_json['id']


@when('I trigger extraction for the document')
def step_trigger_extraction(context):
    assert hasattr(context, 'source_id'), "No source_id found. Make sure to upload a document first."

    response = requests.post(
        f"{context.base_url}/sources/{context.source_id}/extract",
        headers={"Content-Type": "application/json"}
    )

    context.response = response
    context.response_json = response.json() if response.status_code in [200, 202] else None


@then('the extraction response should contain message "{expected_message}"')
def step_check_extraction_message(context, expected_message):
    assert context.response_json is not None, "Response JSON is None"
    assert 'message' in context.response_json, "Response does not contain 'message' field"
    actual_message = context.response_json['message']
    assert actual_message == expected_message, \
        f"Expected message '{expected_message}', but got '{actual_message}'"


@then('the extraction response should contain the source ID')
def step_check_extraction_source_id(context):
    assert context.response_json is not None, "Response JSON is None"
    assert 'source_id' in context.response_json, "Response does not contain 'source_id' field"

    response_source_id = context.response_json['source_id']
    assert response_source_id == str(context.source_id), \
        f"Expected source_id '{context.source_id}', but got '{response_source_id}'"


@then('the extraction response should contain status "{expected_status}"')
def step_check_extraction_status(context, expected_status):
    assert context.response_json is not None, "Response JSON is None"
    assert 'status' in context.response_json, "Response does not contain 'status' field"
    actual_status = context.response_json['status']
    assert actual_status == expected_status, \
        f"Expected status '{expected_status}', but got '{actual_status}'"


@given('I have triggered extraction and waited for completion')
def step_trigger_extraction_and_wait(context):
    import time

    assert hasattr(context, 'source_id'), "No source_id found. Make sure to upload a document first."

    response = requests.post(
        f"{context.base_url}/sources/{context.source_id}/extract",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 202, \
        f"Failed to trigger extraction. Status: {response.status_code}, Response: {response.text}"

    max_wait = 240
    start_time = time.time()

    while time.time() - start_time < max_wait:
        status_response = requests.get(
            f"{context.base_url}/sources/{context.source_id}/extraction-status"
        )

        if status_response.status_code == 200:
            status_data = status_response.json()
            current_status = status_data.get('status')

            if current_status == 'COMPLETED':
                return
            elif current_status == 'FAILED':
                raise AssertionError(f"Extraction failed: {status_data.get('error', 'Unknown error')}")

        time.sleep(2)

    raise AssertionError(f"Extraction did not complete within {max_wait} seconds")
