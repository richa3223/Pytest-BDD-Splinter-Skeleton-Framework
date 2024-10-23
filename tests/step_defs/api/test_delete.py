"""step definitions for api test delete feature file"""

import logging

import requests
from pytest_bdd import scenarios, when, parsers
from tests.step_defs.conftest import (API_BASE_URL, API_ENDPOINT, HEADERS,
                                      TIMEOUT)
from tests.step_defs.helpers import log_api_request_and_response_info

scenarios("../../features/api/delete.feature")

LOGGER = logging.getLogger(__name__)

@when(parsers.cfparse("I delete an object with id {object_id}"), target_fixture="response")
def delete_an_object_with_id(object_id: str):
    """delete object by id"""
    api_url = API_BASE_URL + API_ENDPOINT + "/" + object_id
    response = requests.delete(api_url, headers=HEADERS, timeout=TIMEOUT)
    log_api_request_and_response_info(delete_an_object_with_id.__name__, response)
    return response
