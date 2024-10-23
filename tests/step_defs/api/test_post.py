"""step definitions for api test post feature file"""

import logging

import requests
from pytest_bdd import scenarios, then, when
from tests.step_defs.conftest import (API_BASE_URL, API_ENDPOINT, HEADERS,
                                      TIMEOUT)
from tests.step_defs.helpers import (bites_to_json_response_body,
                                     extract_response_id,
                                     log_api_request_and_response_info)

scenarios("../../features/api/post.feature")

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


@when("I add an object with no request body", target_fixture="response")
def add_an_object_no_request_body():
    """add an object with no request body"""
    api_url = API_BASE_URL + API_ENDPOINT
    response = requests.post(api_url, headers=HEADERS, timeout=TIMEOUT)
    log_api_request_and_response_info(add_an_object_no_request_body.__name__, response)
    return response


@then("the added object is returned")
def object_added_is_returned(response):
    """checks object added is returned"""
    pretty_json = bites_to_json_response_body(response)
    # update this to check response against request body and check for createdAt and id keys
    assert pretty_json is not None, "The response body was blank"


@then("the added object can be retrieved")
def get_a_single_object(response):
    """checks a single object is retrieved"""
    expected_response_id = extract_response_id(response)
    api_url = API_BASE_URL + API_ENDPOINT + "/" + expected_response_id
    response = requests.get(api_url, headers=HEADERS, timeout=TIMEOUT)
    log_api_request_and_response_info(get_a_single_object.__name__, response)
    actual_response_id = extract_response_id(response)
    assert expected_response_id == actual_response_id, f"""The expected id:
      {expected_response_id} did not match the actual response id: {actual_response_id}"""
