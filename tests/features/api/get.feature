Feature: GET api request

    Here are examples for GET api BDD tests
 
 Background: Check API is available
   Given the api under test is available

 Scenario: Get a list of objects
   When I request all objects
   Then a list of objects is returned
   And the status code is 200

 Scenario: Get single object that doesn't exist
   When I get a single object with id 600
   Then the error message "Oject with id=600 was not found." is returned
   And the status code is 404