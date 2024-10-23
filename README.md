# Pytest-BDD-Splinter-Skeleton-Framework
This framework currently has examples of:
- AWS component integration testing using pytest with boto3 for integrating with deployed AWS services such as Lambdas and S3 buckets
- API testing using pytest-bdd
- UI testing using pytest-bdd with splinter

The free AWS sample applications available from [LocalStack](https://docs.localstack.cloud/overview/) are used to provide a locally deployable AWS service to run the AWS component integration tests against. Like an AWS emulator. LocalStack requires it's own VS Code session to run.

Please familiarise yourself with the following:
- **Pytest:** Python based test framework [pytest](https://docs.pytest.org/en/stable/index.html)
- **Pytest-BDD:** Pytest based behavioural driven development framework using Gherkin language [pytest-bdd](https://pytest-bdd.readthedocs.io)
- **Pytest-Splinter:** Provides an API layer on top of Selenium designed for easy and efficient UI testing [pytest-splinter](https://splinter.readthedocs.io/en/stable/index.html)
- **Boto3:** The AWS SDK for Python to create, configure, manage and most importantly test AWS services such Lambdas [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html#)

The example tests provided in this skeleton exist to demonstrate good practice and useful Pytest, Pytest-BDD, Pytest-Splinter and Boto3 functionality. To demonstrate this, the example tests have been scripted against a third party AWS service that is neither controlled nor maintained by BJSS and may change at any time. For this, please only consider the existing test scenarios as carefully considered approach & structure guidelines when implementing this framework.

## Prerequisites

### Required

- **Python:** Package manager for JavaScript ([install information](https://www.python.org/downloads/))
- **Docker Desktop:** Required for running LocalStack
  - If you haven't used Docker before please download ([Docker desktop](https://www.docker.com/products/docker-desktop/)) and email IT support for access to the BJSS docker organisation group

### Recommended

- **Visual Studio Code:** Recommended IDE

## Getting Started

Clone the Pytest-BDD-Splinter-Skeleton-Framework to your local machine.

Install the following extension in VS Code:

- **Python:** Python language support with extension access points for IntelliSense (Pylance), Debugging (Python Debugger), linting, formatting
- **Pytest BDD:** Pytest BDD support extension providing autocompletion of BDD steps in feature files and more
- **Cucumber (Gherkin) Full Support:** Similar to Pytest BDD but also provides cucumber icons for feature files

Add the python.exe path to your machines system variables:

- Locate your python.exe file location for example C:\Users\<user.name>\AppData\Local\Programs\Python\Python311\Scripts and add this to the path system variables. You may need admin access on your machine to do this and a machine restart may be required

From within the `Pytest-BDD-Splinter-Skeleton-Framework` directory:

- Run `python -m ensurepip` to make sure you're running the latest version of pip
- Run `pip install -r requirements.txt` to install all the required dependencies

## Running Tests

### Lambda Tests

1. Open another second VS Code session and follow the [LocalStack quick start guide](https://docs.localstack.cloud/getting-started/quickstart/)
   - Install LocalStack
   - Configure an Auth Token
   - Clone the sample-serverless-image-resizer-s3-lambda repo
   - Set up a virtual environment
   - install the requirements-dev.txt file
   - run the bin/deploy.sh command to configure the AWS components
2. Once LocalStack is up and running you can run the Lambda tests from Pytest BDD framework VS Code session
   - Run all Lambda tests:
     - Change directory to tests `cd tests` and run `pytest test_lambdas -vv -s`
       - N.b. some tests may fail see additional information LocalStack fix
   - Run individual Lambda test:
     - Change directory to test_lambdas `cd tests\test_lambdas` and run `pytest test_list.py -vv -s`

### UI Tests

1. The UI tests require LocalStack to be running. See step 1 in the Lambda Tests section above
2. Once LocalStack is up and running you can run the Lambda tests from Pytest BDD framework VS Code session
   - Run all UI tests:
     - Change directory to step_defs `cd tests\step_defs` and run `pytest ui -vv -s --gherkin-terminal-reporter`
       - N.b. some tests may fail see additional information LocalStack fix
   - Run individual UI test:
     - Change directory to ui `cd tests\step_defs\ui` and run `pytest test_conf.py -vv -s --gherkin-terminal-reporter`

### API Tests

1. The API don't require LocalStack to be running.
2. The API tests use a free to use [rest api](https://restful-api.dev/)
   - Run all API tests:
     - Change directory to step_defs `cd tests\step_defs` and run `pytest api -vv -s --gherkin-terminal-reporter`
       - N.b. some tests may fail see additional information
   - Run individual API test:
     - Change directory to api `cd tests\step_defs\api` and run `pytest test_get.py -vv -s --gherkin-terminal-reporter`

## Additional Information

### LocalStack Fix

Occasionally LocalStack doesn't deploy all components first time of trying. Depending on the issue this can cause test failures and LocalStack 40* errors in Docker.

A common issue is a missing ssm parameter. To fix, locate the `ssm put-parameter` config in the deploy.sh file. Then using the Localstack [Resource Browser](https://app.localstack.cloud/inst/default/resources) and apply the ssm parameters manually.

### Pytest BDD Fix

There is a known issue with pytest-bdd version 8 and above where the same fixture can't be updated by multiple scenario steps. Here is the outstanding [issue](https://github.com/pytest-dev/pytest-bdd/issues/689).

The temporary fix can be found [here](https://github.com/pytest-dev/pytest-bdd/issues/689#issuecomment-2103369153). Copy the code from the fix into the `compat.py` file as per the instructions.
