Feature: POST api request

    Here are examples for POST api BDD tests
 
 Background: Check API is available
   Given the api under test is available

 Scenario: Add a valid object
   When I add a valid object
   Then the added object is returned
   And the status code is 200
   And the added object can be retrieved
   And I delete the object
   And the message "Object with id = has been deleted." is returned

 Scenario: Add an object with no request body
   When I add an object with no request body
   Then the error message "400 Bad Request. If you are trying to create or update the data, potential issue is that you are sending incorrect body json or it is missing at all." is returned
   And the status code is 400