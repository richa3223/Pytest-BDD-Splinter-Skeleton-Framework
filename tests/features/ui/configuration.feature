Feature: Configuration

 Background: Check the app is open
   Given the resize app is open

 Scenario: Load Lambda Function URLs from API
   When the Load from API button is pressed
   Then a popup appears with the message "Function URL configurations loaded"
   And the functionUrlPresign field is populated with a URL
   And the functionUrlList field is populated with a URL

Scenario: Apply the Lambda Function URLs
   Given the Lambda Function APIs have been loaded
   When the Apply button is pressed
   Then a popup appears with the message "Configuration saved"
   And the functionUrlPresign field is populated with a URL
   And the functionUrlList field is populated with a URL

Scenario: Clear the Lambda Function URLs
   Given the Lambda Function APIs have been loaded
   When the Clear button is pressed
   Then a popup appears with the message "Configuration cleared"
   And the functionUrlPresign field is empty
   And the functionUrlList field is empty