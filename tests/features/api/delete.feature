Feature: DELETE api request

    Here are examples for DELETE api BDD tests
 
 Background: Check API is available
   Given the api under test is available

 Scenario: Delete an object
   Given I add a valid object
   When I delete an object
   Then the message "Object with id = has been deleted." is returned
   And the status code is 200

 Scenario: Delete an object that doesn't exist
   When I delete an object with id 600
   Then the error message "Object with id = 600 doesn't exist." is returned
   And the status code is 404