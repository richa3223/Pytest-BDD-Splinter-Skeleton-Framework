"""test presign Lambda"""

import json

from tests.conftest import awslambda, exist_ssm_param, s3, ssm

IMAGES_SSM_PARAMETER = "/localstack-thumbnail-app/buckets/images"

def test_presign_images_bucket_not_found():
    """
    test presign Lambda when the images bucket is not found
    Lamdba returns a 200 and ParameterNotFound error message
    """
    # Arrange
    # delete the ssm parameter if present
    if exist_ssm_param(IMAGES_SSM_PARAMETER):
        ssm_delete_response = ssm.delete_parameter(
            Name="/localstack-thumbnail-app/buckets/images"
        )
        print("This is the ssm delete response - " + str(ssm_delete_response))
        ssm_delete_status_code = ssm_delete_response["ResponseMetadata"][
            "HTTPStatusCode"
        ]
        assert 200 == ssm_delete_status_code

    # test the presign lambda
    expected_error_message = ("An error occurred (ParameterNotFound) when"
    " calling the GetParameter operation: Parameter"
    " /localstack-thumbnail-app/buckets/images not found.")
    expected_error_type = "ParameterNotFound"
    payload = {"Records": "Blah"}
    json_object = json.dumps(payload, indent=4)
    print("This is the payload - " + str(payload))

    # Act
    response = awslambda.invoke(FunctionName="presign", Payload=json_object)

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
        Name=IMAGES_SSM_PARAMETER,
        Value="localstack-thumbnails-app-images",
        Type="String",
    )
    print("This is the ssm response - " + str(ssm_put_response))
    ssm_put_status_code = ssm_put_response["ResponseMetadata"]["HTTPStatusCode"]
    assert 200 == ssm_put_status_code


def test_presign_images_already_present():
    """
    test presign Lambda when the images already present
    Lamdba returns a 409 and image already exist error message
    """
    # Arrange
    # upload image to S3
    s3.upload_file(
        "C:/repos/sample-serverless-image-resizer-s3-lambda/tests/nyan-cat.png",
        "localstack-thumbnails-app-images",
        "nyan-cat.png",
    )

    # test the presign lambda
    expected_body_message = (
        "localstack-thumbnails-app-images/nyan-cat.png already exists"
    )
    payload = {"rawPath": "nyan-cat.png"}
    json_object = json.dumps(payload, indent=4)
    print("This is the payload - " + str(payload))

    # Act
    response = awslambda.invoke(FunctionName="presign", Payload=json_object)

    # extract response body
    print(f"response:{response}")
    payload = response["Payload"]
    print(f"payload:{payload}")
    body = payload.read()
    print(f"body:{body}")
    json_body = json.loads(body.decode("utf-8"))
    print(f"json_body:{json_body}")
    lambda_status_code = json_body.get("statusCode")
    actual_body_message = json_body["body"]

    # Assert
    assert 409 == lambda_status_code
    assert expected_body_message == actual_body_message

    # Clean up
    # delete image from s3
    s3_response = s3.delete_object(
        Bucket="localstack-thumbnails-app-images", Key="nyan-cat.png"
    )


def test_presign():
    """
    test presign Lambda happy path
    Lamdba returns a 200 and a URL
    """
    # Arrange
    # test the presign lambda
    payload = {"rawPath": "nyan-cat.png"}
    json_object = json.dumps(payload, indent=4)
    print("This is the payload - " + str(payload))

    # Act
    response = awslambda.invoke(FunctionName="presign", Payload=json_object)

    print(f"response:{response}")
    payload = response["Payload"]
    print(f"payload:{payload}")
    coded_body = payload.read()
    print(f"body:{coded_body}")
    decoded_body = json.loads(coded_body.decode("utf-8"))
    print(f"json_body:{decoded_body}")
    json_body = json.loads(decoded_body["body"])

    expected_body_url = (
        "https://localhost.localstack.cloud:4566/localstack-thumbnails-app-images"
    )
    expected_body_key = "nyan-cat.png"
    lambda_status_code = decoded_body.get("statusCode")
    actual_body_url = json_body["url"]
    actual_body_key = json_body["fields"]["key"]

    # Assert    
    assert 200 == lambda_status_code
    assert expected_body_url == actual_body_url
    assert expected_body_key == actual_body_key
