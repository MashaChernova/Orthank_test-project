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


response_list = ['instances', 'patients', 'plugins', 'series', 'studies'] # 'instances', 'modalities', 'patients', 'peers', 'plugins', 'series', 'studies' #'changes', 'exports','tools', 'statistics'
@pytest.mark.parametrize('response_for_test',
                         response_list,
                         ids=response_list)
def test_rundom_instance_response_ok(api_connecter, response_for_test):
    assert api_connecter.instance_for_id(response_for_test, "random")


response_list = ['instances', 'patients', 'plugins', 'series', 'studies'] # ,'instances', 'modalities', 'patients', 'peers', 'plugins', 'series', 'studies'
@pytest.mark.parametrize('response_for_test',
                         response_list,
                         ids=response_list)
def test_rundom_instance_response_text(api_connecter, response_for_test):
    message = api_connecter.instance_for_id(response_for_test, "random")
    assert messege != 0, message


@pytest.mark.parametrize('study_id_number', [0, -1], ids=['first study', 'latest study'])
@pytest.mark.parametrize('patient_id_number', [0, -1], ids=['first patient', 'latest patient'])
def test_patients_list(api_connecter, patient_id_number, study_id_number):
    patients_list = api_connecter.message_response('patients')
    patient_for_test = patients_list[patient_id_number]
    patient_info = api_connecter.message_response(f'patients/{patient_for_test}')
    assert patient_info.get('ID') == patient_for_test, f"Information about the specified user was not received: {patient_info}"
    patient_series = api_connecter.message_response(f'patients/{patient_for_test}/series')
    series_for_test = patient_series[study_id_number].get('ID')
    patient_from_series_info = api_connecter.message_response(f'series/{series_for_test}/patient').get('ID')
    assert patient_from_series_info == patient_for_test, f'The patient ID specified in the study {patient_for_test} the patient ID for which this study was received {patient_from_series_info}'

