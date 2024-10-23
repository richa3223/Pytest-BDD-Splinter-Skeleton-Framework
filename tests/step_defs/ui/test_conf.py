"""step definitions for configuration feature file"""

import time

from pytest_bdd import parsers, scenarios, then, when

scenarios("../../features/ui/configuration.feature")

@when(parsers.parse("the {button_text} button is pressed"))
def click_button(browser, button_text: str):
    """click button by text"""
    button = browser.find_by_text(button_text)
    button.first.click()
    time.sleep(10)


@then(parsers.cfparse("the {field_id} field is empty"))
def check_url_field_is_empty(browser, field_id: str):
    """check url field is empty"""
    url_field = browser.find_by_id(field_id).first.value
    assert url_field == ''
    