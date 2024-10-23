"""step definitions for upload file feature file"""

import typing

import boto3
from pytest_bdd import given, parsers, scenarios, then

if typing.TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client

s3: "S3Client" = boto3.client(
   "s3", endpoint_url="http://localhost.localstack.cloud:4566"
)

scenarios("../../features/ui/upload_file.feature")

@given(parsers.parse("the file {file_path} is selected"))
def select_file(browser, file_path: str):
    """click button by id"""
    browser.attach_file('file', file_path.replace('"', ''))


@then(parsers.parse("image {image_name} is present in list your files"))
def image_present_in_list_your_files(browser, image_name: str):
    """check list your files for image"""
    browser.find_by_text('Original').is_visible()
    container = browser.find_by_id('imagesContainer')
    assert image_name.replace('"', '') in container.first.value
    assert "Original" in container.first.value
    assert "Resized" in container.first.value


@then(parsers.parse("the {image_name} is deleted from the buckets"))
def image_deleted_from_buckets(image_name: str):
    """delete image from buckets"""
    image_name = image_name.replace('"', '')
    images_response = s3.delete_object(
    Bucket='localstack-thumbnails-app-images',
    Key=image_name
    )
    assert 204 == images_response["ResponseMetadata"]["HTTPStatusCode"]

    resized_response = s3.delete_object(
    Bucket='localstack-thumbnails-app-resized',
    Key=image_name
    )
    assert 204 == resized_response["ResponseMetadata"]["HTTPStatusCode"]
