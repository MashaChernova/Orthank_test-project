from gc import get_objects

import requests
import json
import pytest
import logging
import random

class RestApiConnecter():

    def __init__(self, url):
        self.url = "http://" + url + "/"
        for i in range(6):
            self.upload_instances(f'studies/{i+1}.dcm')
        logging.info('исследования загружены')

    def  __del__(self):
        studies_id_list = self.message_response('studies')
        for study_id in studies_id_list:
            self.remove_instances('studies', study_id)


    def response_status_ok(self, response_for_test):
        response = requests.request("GET", self.url + response_for_test, auth=('orthanc', 'orthanc'))
        try:
            if response.ok:
                return True
            else:
                raise AssertionError(f'The report contains an error, response code: {response.status_code}')
        except:
            raise AssertionError('Failed to get response status')


    def message_response(self, response_for_test):
        logging.info("massage response funktion")
        response = requests.request("GET", self.url + response_for_test, auth=('orthanc', 'orthanc'))
        assert response.ok
        try:
            return response.json()
        except:
            raise AssertionError("Unable to read response text")


    def instance_for_id(self, get_list_response, function_name):
        try:
            list_responce = requests.request("GET", self.url + get_list_response, auth=('orthanc', 'orthanc'))
        except:
            raise AssertionError(f'No response from the server to the request {self.url + get_list_response} was received')
        try:
            list_lenth = len(list_responce.json())
        except:
            raise AssertionError("The answer is not a list")
        try:
            if function_name == "random":
                logging.info('Getting a random value from a list')
                id = random.choice(list_responce.json())
            else:
                logging.info('Getting first value from a list')
                id=list_responce.json()[0]
            logging.info(f"id={id}")
        except:
            raise AssertionError(f"The instances is not found {list_lenth} in {list_responce.json()}")
        try:
            get_instanse_response = get_list_response + f"/{id}"
            logging.info(f'new requests: {get_instanse_response}')
            instance_for_id = requests.request("GET", self.url + get_instanse_response, auth=('orthanc', 'orthanc'))
        except:
            raise AssertionError(f"Unable to retrieve response for request {self.url + get_instanse_response}")
        try:
            assert instance_for_id.ok, "request status isn't ok"
            assert id in instance_for_id.json()
            return instance_for_id.json() #.get('message')
        except:
            logging.info('Answer is not json')
        try:
            assert id in instance_for_id.text
            return instance_for_id.text
        except:
            raise AssertionError(f'Failed to extract json or read text from response {self.url + get_instanse_response} {id}/{list_lenth} in {list_responce.json()}')


    def list_lenth(self, get_list_response):
        try:
            list_responce = requests.request("GET", self.url + get_list_response, auth=('orthanc', 'orthanc'))
        except:
            raise AssertionError(f'No response from the server to the request {self.url + get_list_response} was received')
        try:
            list_len = len(list_responce.json())
            logger.info(f"List length {list_len}")
            return list_len
        except:
            raise AssertionError("The answer is not a list")


    def get_number_for_list(self, get_list_response, type):
        try:
            list_responce = requests.request("GET", self.url + get_list_response, auth=('orthanc', 'orthanc'))
        except:
            raise AssertionError(
                f'No response from the server to the request {self.url + get_list_response} was received')
        try:
            list_lenth = len(list_responce.json())
        except:
            raise AssertionError("The answer is not a list")
        if type in ['first', 0]:
            return 0
        elif type in ['last', -1]:
            return -1
        elif type == 'random':
            num = random.randint(1, list_lenth - 2)
            # logger.info(f'Random value of list element {num} received')
            return num
        else:
            if type < list_lenth:
                return type
            else:
                raise AssertionError('This value is not in the list')


    def get_patient_name(self, patient_number):
        patients_list = self.message_response('patients')
        patient_for_test = patients_list[patient_number]
        patient_info = self.message_response(f'patients/{patient_for_test}')
        assert patient_info.get('ID') == patient_for_test, f"Information about the specified user was not received: {patient_info}"
        patient_name = self.message_response(f'patients/{patient_for_test}/module').get('0010,0010').get('Value')
        return patient_name


    def get_study_info(self, study_number, tag_name):
        try:
            if type(study_number) == int:
                study_id = self.message_response('studies')[study_number]
            else:
                study_id = study_number
            study_info = self.message_response(f'studies/{study_id}')
        except:
            raise AssertionError('Unable to retrieve research information')
        if tag_name in ["StudyDate", "StudyID", "StudyDescription"]:
            try:
                return study_info.get('MainDicomTags').get(tag_name)
            except:
                raise AssertionError('Failed to get tag value')
        elif tag_name in ["PatientBirthDate", "PatientID", "PatientName", "PatientSex"]:
            try:
                return study_info.get('PatientMainDicomTags').get(tag_name)
            except:
                raise AssertionError('Failed to get tag value')
        else:
            try:
                return study_info.get(tag_name)
            except:
                raise AssertionError('Failed to get tag value')


    def upload_instances(self, file_for_upload):
        try:
            with open(file_for_upload, 'rb') as f:
                file_data = f.read()
            response = requests.request("POST", self.url + 'instances', auth=('orthanc', 'orthanc'), data=file_data)
        except Exception as e:
            raise AssertionError(f'Failed to send request: {str(e)}')
        try:
            return response.json()
        except:
            raise AssertionError(f'The report is not json, response code: {response.status_code}')


    def remove_instances(self, request_for_remove, instance_id):
        try:
            req_url = self.url + f'{request_for_remove}/{instance_id}'
            requests.request("DELETE", req_url, auth=('orthanc', 'orthanc'))
        except Exception as e:
            raise AssertionError(f'Failed to send request: {str(e)}')



#https://orthanc.uclouvain.be/demo/changes