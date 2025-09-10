import pytest
import logging
import pydicom
from pydicom import dcmread

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
def test_random_instance_response_ok(api_connecter, response_for_test):
    assert api_connecter.instance_for_id(response_for_test, "random")


response_list = ['instances', 'patients', 'plugins', 'series', 'studies'] # ,'instances', 'modalities', 'patients', 'peers', 'plugins', 'series', 'studies'
@pytest.mark.parametrize('response_for_test',
                         response_list,
                         ids=response_list)
def test_random_instance_response_text(api_connecter, response_for_test):
    message = api_connecter.instance_for_id(response_for_test, "random")
    assert message != 0, message


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

@pytest.mark.only2
def test_upload_ok(api_connecter):
    dicom_files_path = "studies/"
    i=9
    file_path = f'{dicom_files_path}/{i}.dcm'
    logging.info(file_path)
    request = api_connecter.upload_instances(file_path)
    try:
        study_id = request.get('ID')
    except AttributeError:
        raise AssertionError(len(request))
    message = api_connecter.message_response(f'instances/{study_id}')
    assert message != 0, message


@pytest.mark.only1
def test_upload_patient_name(api_connecter):
    dicom_files_path = "studies/"
    i=10
    file_path = f'{dicom_files_path}/{i}.dcm'
    logging.info(file_path)
    request = api_connecter.upload_instances(file_path)
    try:
        instance_id = request.get('ID')
        study_id = request.get('ParentStudy')
    except AttributeError:
        raise AssertionError(type(request))
    patient_name = api_connecter.get_study_info(study_id, 'PatientName')
    ds = dcmread(file_path)
    patient_name_from_dicom = ds.PatientName
    assert patient_name == patient_name_from_dicom, f"{patient_name} insert {patient_name_from_dicom}"
    api_connecter.remove_instances('instances',instance_id)


@pytest.mark.only
@pytest.mark.parametrize('study_number_type', ['random', -1, 0])
def test_remove_success(api_connecter, study_number_type):
    study_number = api_connecter.get_number_for_list('studies', study_number_type)
    study_id = api_connecter.get_study_info(study_number, "ID")
    api_connecter.remove_instances('studies', study_id)
    assert study_id not in api_connecter.message_response('studies'), f"The study {study_id} remains on the server"

