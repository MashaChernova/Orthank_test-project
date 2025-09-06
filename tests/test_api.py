import pytest
import logging
from rest_api_connecter import RestApiConnecter


response_list = ['changes', 'exports', 'instances', 'tools', 'modalities', 'patients', 'peers', 'plugins', 'series', 'statistics', 'studies', 'tools/log-level']
@pytest.mark.parametrize('response_for_test',
                         response_list,
                         ids=response_list)
def test_response_status(api_connecter, response_for_test):
    logging.info("base_url")
    assert api_connecter.response_status_ok(response_for_test)

response_list = ['changes', 'exports', 'instances', 'tools', 'modalities', 'patients', 'peers', 'plugins', 'series', 'statistics', 'studies']
@pytest.mark.parametrize('response_for_test',
                         response_list,
                         ids=response_list)
def test_massege_not_empty(api_connecter, response_for_test):
    assert api_connecter.message_response(response_for_test) != '', "Empty response received"

response_list = ['changes', 'exports','tools', 'statistics'] # 'instances', 'modalities', 'patients', 'peers', 'plugins', 'series', 'studies'
@pytest.mark.parametrize('response_for_test',
                         response_list,
                         ids=response_list)
@pytest.mark.xfail
def test_rundom_instance_response_ok(api_connecter, response_for_test):
    assert api_connecter.instance_for_id(response_for_test, "random")

response_list = ['changes', 'exports','tools', 'statistics','instances', 'modalities', 'patients', 'peers', 'plugins', 'series', 'studies'] # ,'instances', 'modalities', 'patients', 'peers', 'plugins', 'series', 'studies'
@pytest.mark.parametrize('response_for_test',
                         response_list,
                         ids=response_list)
@pytest.mark.xfail
def test_rundom_instance_response_text(api_connecter, response_for_test):
    massege = api_connecter.instance_for_id(response_for_test, "random")
    assert massege == 0, massege