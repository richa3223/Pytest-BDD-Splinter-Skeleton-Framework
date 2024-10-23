"""conftest"""

import json
import logging

import pytest
import requests
from pytest_bdd import given, parsers, then, when
from splinter import Browser, Config
from helpers import extract_response_id, log_api_request_and_response_info

APP_URL = "https://webapp.s3-website.localhost.localstack.cloud:4566/"
API_BASE_URL = "https://api.restful-api.dev/"
API_ENDPOINT = "objects"
HEADERS = {"content-type": "application/json"}
TIMEOUT = 60

new_object = {
   "name": "Banana MicBook Amateur 3000",
   "data": {
      "year": 2031,
      "price": 21849.99,
      "CPU model": "Entel Treecore i500",
      "Hard disk size": "1 PB"
   }
}

LOGGER = logging.getLogger(__name__)

@pytest.fixture(name="browser")
def fixture_browser():
    """browser fixture"""
    browser_config = Config(fullscreen=True)#, headless=True)
    b = Browser('chrome', config=browser_config)
    b.visit(APP_URL)
    yield b
    b.quit()

@pytest.fixture
def obj_id_fixture():
    """obj id"""  
    return []

@pytest.hookimpl
def pytest_bdd_before_scenario(scenario):
    """scenario set up tasks"""
    print("Before scenario: " + str(scenario.name))


@pytest.hookimpl
def pytest_bdd_after_scenario(scenario):
    """scenario clean up tasks"""
    print("After scenario: " + str(scenario.name))

############################## UI common steps ##############################

@given("the resize app is open")
def the_resize_app_is_open(browser):
    """open resize app"""
    browser.find_by_text('Serverless thumbnail generator')


@when(parsers.parse("the {button_text} button is pressed"))
def click_button(browser, button_text: str):
    """click button by text"""
    if "Upload" in button_text:
        button = browser.find_by_text(button_text + " ")
    else:
        button = browser.find_by_text(button_text)
    button.first.click()


@then(parsers.cfparse("a popup appears with the message {pop_text}"))
def check_pop_up_message(browser, pop_text: str):
    """checks pop up message text and clicks ok"""
    alert = browser.get_alert()
    alert_text = alert.text
    assert pop_text.replace('"', '') == alert_text
    alert.accept()


@given("the Lambda Function APIs have been loaded")
def lambda_apis_loaded(browser):
    """loads the lambda apis"""
    click_button(browser, "Load from API")
    check_pop_up_message(browser, "Function URL configurations loaded")
    check_url_field_is_populated(browser, "functionUrlPresign")


@then(parsers.cfparse("the {field_id} field is populated with a URL"))
def check_url_field_is_populated(browser, field_id: str):
    """check url field contains a url"""
    url_field = browser.find_by_id(field_id).first.value
    assert "http://" in url_field

############################## UI common steps ##############################

############################## API common steps ##############################

@given("I add a valid object", target_fixture="response")
@when("I add a valid object", target_fixture="response")
def add_a_valid_object():
    """add a valid object"""
    api_url = API_BASE_URL + API_ENDPOINT
    payload = json.dumps(new_object)
    response = requests.post(api_url, data=payload, headers=HEADERS, timeout=TIMEOUT)
    log_api_request_and_response_info(add_a_valid_object.__name__, response)
    return response


@then("I delete the object", target_fixture="response")
@when("I delete an object", target_fixture="response")
def delete_a_single_object(response, obj_id_fixture):
    """deletes a single object"""
    expected_response_id = extract_response_id(response)
    api_url = API_BASE_URL + API_ENDPOINT + "/" + expected_response_id
    response = requests.delete(api_url, headers=HEADERS, timeout=TIMEOUT)
    log_api_request_and_response_info(delete_a_single_object.__name__, response)
    check_status_code(response, 200)
    obj_id_fixture.append(expected_response_id)
    return response


@given("the api under test is available")
def api_under_test_available():
    """check the api under is test is available"""
    base_url = API_BASE_URL
    LOGGER.info("Checking the base API url is available, base URL: %s", base_url)
    base_response = requests.get(base_url, timeout=TIMEOUT)
    assert 200 == base_response.status_code, f"""The API is not currently
                   available. Base url response code is {base_response.status_code}"""


@then(parsers.parse("the status code is {status_code:d}"))
def check_status_code(response, status_code):
    """check status code"""
    assert status_code == response.status_code, f"""The expected status:
      {status_code} did not match the actual status: {response.status_code}"""


@then(parsers.parse("the error message {expected_error_message} is returned"))
def check_response_body_error_message(response, expected_error_message: str):
    """checks for error message in the response"""
    my_json = response.content.decode('utf8')
    data = json.loads(my_json)
    actual_error_message = data["error"]
    assert expected_error_message.replace('"', '') == actual_error_message, f"""The expected error message:
     {expected_error_message} did not match the actual error message: {actual_error_message}"""
    

@then(parsers.parse("the message {expected_message} is returned"))
def check_response_body_message(response, obj_id_fixture, expected_message: str):
    """checks for message in the response"""
    if "deleted" in expected_message:
        message_array = expected_message.split("=")
        expected_response_message = message_array[0] + "= " + obj_id_fixture[0] + message_array[1]
    if "deleted" not in expected_message:
        expected_response_message = expected_message
    my_json = response.content.decode('utf8')
    data = json.loads(my_json)
    actual_response_message = data["message"]
    assert expected_response_message.replace('"', '') == actual_response_message, f"""The expected message:
      {expected_response_message} did not match the actual response message: {actual_response_message}"""

############################## API common steps ##############################
