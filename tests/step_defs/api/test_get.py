"""step definitions for api test get feature file"""

import json
import logging

import requests
from pytest_bdd import parsers, scenarios, then, when
from tests.step_defs.conftest import (API_BASE_URL, API_ENDPOINT, HEADERS,
                                      TIMEOUT)
from tests.step_defs.helpers import (bites_to_json_response_body,
                                     log_api_request_and_response_info)

scenarios("../../features/api/get.feature")

LOGGER = logging.getLogger(__name__)

@when("I request all objects", target_fixture='response')
def get_all_objects():
    """request a list of objects"""
    api_url = API_BASE_URL + API_ENDPOINT
    response = requests.get(api_url, headers=HEADERS, timeout=TIMEOUT)
    log_api_request_and_response_info(get_all_objects.__name__, response)
    return response


@when(parsers.cfparse("I get a single object with id {object_id}"), target_fixture="response")
def request_single_object(object_id: str):
    """request a single object"""
    api_url = API_BASE_URL + API_ENDPOINT + "/" + object_id
    response = requests.get(api_url, headers=HEADERS, timeout=TIMEOUT)
    log_api_request_and_response_info(request_single_object.__name__, response)
    return response


@then("a list of objects is returned")
def list_of_objects_returns(response):
    """checks a list of objects is returned"""
    pretty_json = bites_to_json_response_body(response)
    assert pretty_json is not None, "The response body was blank"
