import requests
from behave import given, when, then
from uuid import UUID
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase


@when('I create a chat session with the following data:')
def step_create_chat_session(context):
    assert hasattr(context, 'objective_id'), "No objective_id found. Make sure to create an objective first."

    data = {
        "objective_id": context.objective_id
    }

    for row in context.table:
        field = row['field']
        value = row['value']
        data[field] = value

    response = requests.post(
        f"{context.base_url}/chat/sessions",
        json=data,
        headers={"Content-Type": "application/json"}
    )

    context.response = response
    context.response_json = response.json() if response.status_code in [200, 201] else None

    if context.response_json and 'id' in context.response_json:
        context.session_id = context.response_json['id']
        context.created_session_ids.append(context.session_id)


@then('the response should contain a valid session ID')
def step_check_session_id(context):
    assert context.response_json is not None, "Response JSON is None"
    assert 'id' in context.response_json, "Response does not contain 'id' field"

    try:
        UUID(context.response_json['id'])
    except ValueError:
        raise AssertionError(f"Invalid UUID format: {context.response_json['id']}")


@then('the chat session {field} should be "{expected_value}"')
def step_check_chat_session_field(context, field, expected_value):
    assert context.response_json is not None, "Response JSON is None"
    assert field in context.response_json, f"Response does not contain '{field}' field"
    actual_value = context.response_json[field]
    assert actual_value == expected_value, \
        f"Expected {field} '{expected_value}', but got '{actual_value}'"


@given('I have created a chat session named "{name}"')
def step_create_chat_session_with_name(context, name):
    assert hasattr(context, 'objective_id'), "No objective_id found. Make sure to create an objective first."

    data = {
        "objective_id": context.objective_id,
        "name": name
    }

    response = requests.post(
        f"{context.base_url}/chat/sessions",
        json=data,
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 201, \
        f"Failed to create chat session. Status: {response.status_code}, Response: {response.text}"

    response_json = response.json()
    context.session_id = response_json['id']
    context.created_session_ids.append(context.session_id)


@when('I send a message with content "{content}"')
def step_send_message(context, content):
    assert hasattr(context, 'session_id'), "No session_id found. Make sure to create a chat session first."

    context.last_user_message = content
    
    data = {
        "content": content
    }

    response = requests.post(
        f"{context.base_url}/chat/sessions/{context.session_id}/messages",
        json=data,
        headers={"Content-Type": "application/json"}
    )

    context.response = response
    context.response_json = response.json() if response.status_code in [200, 201] else None


@then('the response should contain a valid message ID')
def step_check_message_id(context):
    assert context.response_json is not None, "Response JSON is None"
    assert 'id' in context.response_json, "Response does not contain 'id' field"

    try:
        UUID(context.response_json['id'])
    except ValueError:
        raise AssertionError(f"Invalid UUID format: {context.response_json['id']}")


@then('the message {field} should be "{expected_value}"')
def step_check_message_field(context, field, expected_value):
    assert context.response_json is not None, "Response JSON is None"
    assert field in context.response_json, f"Response does not contain '{field}' field"
    actual_value = context.response_json[field]
    assert actual_value == expected_value, \
        f"Expected {field} '{expected_value}', but got '{actual_value}'"


@then('the message content should not be empty')
def step_check_message_content_not_empty(context):
    assert context.response_json is not None, "Response JSON is None"
    assert 'content' in context.response_json, "Response does not contain 'content' field"
    content = context.response_json['content']
    assert content and len(content.strip()) > 0, "Message content is empty"


@then('the message response should be faithful to the sources')
def step_check_message_faithfulness(context):
    assert context.response_json is not None, "Response JSON is None"
    assert 'content' in context.response_json, "Response does not contain 'content' field"
    assert 'sources' in context.response_json, "Response does not contain 'sources' field"
    
    actual_output = context.response_json['content']
    sources = context.response_json.get('sources', [])
    
    if not sources:
        return
    
    retrieval_context = [
        f"{src.get('source_name', 'Unknown')}: {src.get('snippet', '')}"
        for src in sources
    ]
    
    if not retrieval_context or not any(ctx.strip() for ctx in retrieval_context):
        return
    
    user_query = getattr(context, 'last_user_message', '')
    
    test_case = LLMTestCase(
        input=user_query,
        actual_output=actual_output,
        retrieval_context=retrieval_context
    )
    
    metric = FaithfulnessMetric(threshold=0.9)
    
    try:
        metric.measure(test_case)
        assert metric.score >= metric.threshold, (
            f"Faithfulness score {metric.score:.2f} is below threshold {metric.threshold}. "
            f"Reason: {metric.reason}"
        )
    except Exception as e:
        raise AssertionError(f"Faithfulness evaluation failed: {str(e)}")


@then('the message content should contain "{expected_text}"')
def step_check_message_content_contains(context, expected_text):
    assert context.response_json is not None, "Response JSON is None"
    assert 'content' in context.response_json, "Response does not contain 'content' field"
    content = context.response_json['content']
    assert expected_text in content, \
        f"Expected message content to contain '{expected_text}', but got: {content}"


@then('the message content should contain date information')
def step_check_message_contains_date_info(context):
    assert context.response_json is not None, "Response JSON is None"
    assert 'content' in context.response_json, "Response does not contain 'content' field"
    content = context.response_json['content'].lower()

    date_keywords = [
        'march', 'january', 'february', 'april', 'may', 'june', 'july',
        'august', 'september', 'october', 'november', 'december',
        '2023', '2024', 'released', 'launched', 'announced'
    ]

    has_date_info = any(keyword in content for keyword in date_keywords)
    assert has_date_info, \
        f"Expected message content to contain date information (months, years, or temporal verbs), but got: {context.response_json['content']}"


@then('the message content should be relevant to the answer "{expected_answer}"')
def step_check_message_relevance_to_answer(context, expected_answer):
    from deepeval.metrics import AnswerRelevancyMetric

    assert context.response_json is not None, "Response JSON is None"
    assert 'content' in context.response_json, "Response does not contain 'content' field"

    actual_output = context.response_json['content']
    user_query = getattr(context, 'last_user_message', '')

    test_case = LLMTestCase(
        input=user_query,
        actual_output=actual_output,
        expected_output=expected_answer
    )

    metric = AnswerRelevancyMetric(threshold=0.9)

    try:
        metric.measure(test_case)
        assert metric.score >= metric.threshold, (
            f"Answer Relevancy score {metric.score:.2f} is below threshold {metric.threshold}. "
            f"Reason: {metric.reason}"
        )
    except Exception as e:
        raise AssertionError(f"Answer Relevancy evaluation failed: {str(e)}")
