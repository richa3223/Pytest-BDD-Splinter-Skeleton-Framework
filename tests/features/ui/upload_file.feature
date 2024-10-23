Feature: Upload file

 Background: Check the app is open
   Given the resize app is open

 Scenario: Upload a file when there is no URLs configured
   Given the file "C:/Whale_Image.JPG" is selected
   When the Upload button is pressed
   Then a popup appears with the message "error getting pre-signed URL. check the logs!"

Scenario: Upload a file when the URLs are configured
   Given the Lambda Function APIs have been loaded
   And the file "C:/Whale_Image.JPG" is selected
   When the Upload button is pressed
   Then a popup appears with the message "success!"
   And image "Whale_Image.JPG" is present in list your files
   And the "Whale_Image.JPG" is deleted from the buckets