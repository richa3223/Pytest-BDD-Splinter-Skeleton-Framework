'''test list Lambda'''

from tests.conftest import awslambda


def test_list_returns_200():
    '''test list Lambda returns 200'''
    # Act
    response = awslambda.invoke(FunctionName="list")
    
    # Assert
    assert 200 == response["StatusCode"]
