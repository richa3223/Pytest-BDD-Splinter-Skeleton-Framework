"""test resize Lambda"""

import json

from tests.conftest import awslambda, exist_ssm_param, ssm

RESIZED_SSM_PARAMETER = "/localstack-thumbnail-app/buckets/resized"

def test_resize():
    """
    test resize Lambda happy path
    Lamdba returns a 200
    """
    # Act
    response = awslambda.invoke(FunctionName="resize")

    # Assert
    assert 200 == response["StatusCode"]


def test_resize_error():
    """
    test resize Lambda when the images bucket is not found
    Lamdba returns a 200 and ParameterNotFound error message
    """
    # Arrange
    # delete the ssm parameter
    if exist_ssm_param(RESIZED_SSM_PARAMETER):
        ssm_delete_response = ssm.delete_parameter(Name=RESIZED_SSM_PARAMETER)
        print("This is the ssm delete response - " + str(ssm_delete_response))
        ssm_delete_status_code = ssm_delete_response["ResponseMetadata"][
            "HTTPStatusCode"
        ]
        assert 200 == ssm_delete_status_code

    # test the resize lambda
    expected_error_message = ("An error occurred (ParameterNotFound) when"
    " calling the GetParameter operation: Parameter"
    " /localstack-thumbnail-app/buckets/resized not found.")
    expected_error_type = "ParameterNotFound"
    payload = {"rawPath": "Blah"}
    json_object = json.dumps(payload, indent=4)
    print("This is the payload - " + str(payload))

    # Act
    response = awslambda.invoke(FunctionName="resize", Payload=json_object)
    print(f"response:{response}")
    payload = response["Payload"]
    print(f"payload:{payload}")
    body = payload.read()
    print(f"body:{body}")
    json_body = json.loads(body.decode("utf-8"))
    print(f"json_body:{json_body}")
    lambda_status_code = response.get("StatusCode")
    actual_error_message = json_body["errorMessage"]
    actual_error_type = json_body["errorType"]

    # Assert
    assert 200 == lambda_status_code
    assert expected_error_message == actual_error_message
    assert expected_error_type == actual_error_type

    # Clean up
    # add the ssm parameter back in
    ssm_put_response = ssm.put_parameter(
        Name=RESIZED_SSM_PARAMETER,
        Value="localstack-thumbnails-app-images",
        Type="String",
    )
    print("This is the ssm response - " + str(ssm_put_response))
    ssm_put_status_code = ssm_put_response["ResponseMetadata"]["HTTPStatusCode"]
    assert 200 == ssm_put_status_code
