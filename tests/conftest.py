''' conftest '''
import os
import typing

import boto3
import pytest

if typing.TYPE_CHECKING:
    from mypy_boto3_lambda import LambdaClient
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_ssm import SSMClient

os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

s3: "S3Client" = boto3.client(
    "s3", endpoint_url="http://localhost.localstack.cloud:4566"
)
ssm: "SSMClient" = boto3.client(
    "ssm", endpoint_url="http://localhost.localstack.cloud:4566"
)
awslambda: "LambdaClient" = boto3.client(
    "lambda", endpoint_url="http://localhost.localstack.cloud:4566"
)

@pytest.fixture#(autouse=True)
def _wait_for_lambdas():
    """
    makes sure that the lambdas are available before running integration tests
    """
    awslambda.get_waiter("function_active").wait(FunctionName="presign")
    awslambda.get_waiter("function_active").wait(FunctionName="resize")
    awslambda.get_waiter("function_active").wait(FunctionName="list")

def exist_ssm_param(param_name: str) -> bool:
    '''checks ssm parameter exists'''
    try:
        response = ssm.get_parameter(Name=param_name)
        return True
    except ssm.exceptions.ParameterNotFound:
        return False
