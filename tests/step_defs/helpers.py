"""helpers"""

import json
import logging

LOGGER = logging.getLogger(__name__)

############################## API helper functions ##############################

def bites_to_json_response_body(response) -> str:
    """converts API response body from bytes to pretty json"""
    my_json = response.content.decode('utf8')
    data = json.loads(my_json)
    return json.dumps(data, indent=4, sort_keys=True)


def json_request_body(response) -> str | None:
    """converts request body to pretty json"""
    if response.request.body is not None:
        data = json.loads(response.request.body)
        return json.dumps(data, indent=4, sort_keys=True)
    return None


def extract_response_id(response) -> str:
    """extracts the id value from the response body"""
    my_json = response.content.decode('utf8')
    data = json.loads(my_json)
    return data["id"]


def log_api_request_and_response_info(function_name, response):
    """ logs out the request method and url
        and response body and response status code"""
    LOGGER.info("%s - API request - method:URL: %s:%s", function_name, response.request.method, response.request.url)
    pretty_req_json = json_request_body(response)
    LOGGER.info("%s - API request body: %s", function_name, pretty_req_json)
    pretty_json = bites_to_json_response_body(response)
    LOGGER.info("%s - API response body: %s", function_name, pretty_json)
    LOGGER.info("%s - API response status code: %s", function_name, response.status_code)

############################## API helper functions ##############################