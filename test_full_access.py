from datetime import date
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Headers
from werkzeug.test import TestResponse
from werkzeug.wrappers import response
import http
from api import create_app
from config import DevConfig
from dotenv import load_dotenv

CLIENT_ID_VAR = "AUTH0_CLIENT_ADMIN"
CLIENT_SECRET_VAR = "AUTH0_SECRET_ADMIN"
GOOD_CONTACT_DATA = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }


def generate_auth_token():
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
    AUTH0_CLIENT_ID = os.getenv(CLIENT_ID_VAR)
    AUTH0_CLIENT_SECRET = os.getenv(CLIENT_SECRET_VAR)

    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": AUTH0_AUDIENCE,
        "grant_type": "client_credentials"
    }

    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data)

class FullAccessTestSuite(unittest.TestCase):
    """This class performs the full suite of test cases for the CAR app"""

    @classmethod
    def setUpClass(cls) -> None:
        # load the environment variables
        load_dotenv()
        cls._auth_token = generate_auth_token()    

    def setUp(self):
        self.app = create_app(DevConfig)
        self.client = self.app.test_client
        self.headers: dict = {
            "Authorization": f"Bearer {self._auth_token}"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    # =========================================================================
    # Internal Contact Tests
    # =========================================================================
    def add_contact(self, contact_data) -> TestResponse:
        return self.client().post(
            '/api/contacts',
            headers=self.headers,
            json=contact_data)

    def test_add_contact_success(self):
        
        response = self.add_contact(GOOD_CONTACT_DATA)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 200,
            msg="The Reponse Code was not 200"
        )
        self.assertIn(
            'success', data,
            msg="The response does not indicate call success"
        )
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successful"
        )
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_add_contact_fail(self):
        # fails - no contact type
        contact_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "status": "A"
        }

        response = self.add_contact(contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 400,
            msg=f"The Reponse Code was not 400")
        self.assertIn(
            'success', data,
            msg=f"The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg=f"The response did not report as failed")

    def test_get_contact_list_success(self):
        response = self.client().get('/api/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertIn(
            'data', data,
            msg="The response does not contain a questions array")
        self.assertIn(
            'success', data, msg="The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="The success indicator is not equal to true")

    def test_get_contact_list_fail(self):
        response = self.client().get('/api/contacts?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_get_contact_success(self):

        contact_response = self.add_contact(GOOD_CONTACT_DATA)
        contact = json.loads(contact_response.data)
        contact_id = contact.get('data').get('id')
        response = self.client().get(
            f'/api/contacts/{contact_id}',
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successful")
        self.assertIn(
            'data', data,
            msg="The reponse did not contain the contact data")

    def test_get_contact_fail(self):
        test_name = "Test: Get Contact fail"
        response = self.client().get('/api/contacts/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=f"{test_name} - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    def test_update_contact_success(self):

        # Create the contact to be updated
        contact_response = self.add_contact(GOOD_CONTACT_DATA)
        contact = json.loads(contact_response.data)
        contact_id = contact.get('data').get('id')

        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{contact_id}',
            headers=self.headers,
            json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successfult")
        self.assertIn(
            'data', data,
            msg="The reponse did not contain the contact data")

    def test_update_contact_failed(self):

        # Create the contact to be updated
        contact_response = self.add_contact(GOOD_CONTACT_DATA)
        contact = json.loads(contact_response.data)
        contact_id = contact.get('data').get('id')

        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "invaild_type",
            "status": "I"
        }
        test_name = "Test: Update Contact fail"
        response = self.client().patch(
            f'/api/contacts/{contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 400,
            msg=f"{test_name} - Status Code was not 400")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    def test_delete_contact_success(self):

        # Create the contact to be deleted
        contact_response = self.add_contact(GOOD_CONTACT_DATA)
        contact = json.loads(contact_response.data)
        contact_id = contact.get('data').get('id')

        response = self.client().delete(
            f'/api/contacts/{contact_id}',
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successful")
        self.assertIn(
            'id', data,
            msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], contact_id,
            msg="The deleted contact did not match the id sent")

    def test_delete_contact_fail(self):
        response = self.client().delete(
            '/api/contacts/99',
            headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="the response did not report as failed")

    # =========================================================================
    # Client Tests
    # =========================================================================
    def test_add_client_success(self):
        client_data = {
            "name": "The Powerhouse",
            "bus_reg_nbr": "12345678901",
            "abbreviation": "TPH"
        }

        test_name = "Test: Add Client success"
        response = self.client().post(
            '/api/clients',
            headers=self.headers,
            json=client_data)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - The Reponse Code was not 200")
        self.assertIn(
            'success', data,
            msg=f"{test_name} - The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - The response did not report as successful")
        self.assertIn(
            'data', data,
            msg=f"{test_name} - The reponse did not contain the contact data")

        contact_data: dict = data.get('data')
        self.client_id = contact_data.get('id', 1)

    def test_add_client_fail(self):
        client_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }
        test_name = "Test: Add Client fail"
        response = self.client().post(
            '/api/clients',
            headers=self.headers,
            json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 400,
            msg=f"{test_name} - The Reponse Code was not 400")
        self.assertIn(
            'success', data,
            msg=f"{test_name} - The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    def test_get_client_list_success(self):
        test_name = "Test: Get Client List success"
        response = self.client().get('/api/clients', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - Status Code was not 200")
        self.assertIn(
            'data', data,
            msg=f"{test_name} - The response does not contain a questions array")
        self.assertIn(
            'success', data,
            msg=f"{test_name} - The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - The success indicator is not equal to true")

    def test_get_client_list_fail(self):
        test_name = "Test: Get Client List fail"
        response = self.client().get('/api/clients?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=f"{test_name} - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - the response did not report as failed")

    def test_get_client_success(self):
        test_name = "Test: Get Client success"
        response = self.client().get(
            f"/api/clients/{self.client_id}",
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - The response did not report as successful")
        self.assertIn(
            'data', data,
            msg=f"{test_name} - The reponse did not contain the contact data")

    def test_get_client_fail(self):
        test_name = "Test: Get Client fail"
        response = self.client().get('/api/clients/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=f"{test_name} - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    def test_update_client_success(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "I"
        }
        test_name = "Test: Update Contact success"
        response = self.client().patch(
            f"/api/clients/{self.client_id}",
            headers=self.headers,
            json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - The response did not report as successfult")
        self.assertIn(
            'data', data,
            msg=f"{test_name} - The reponse did not contain the contact data")

    def test_update_client_failed(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "invaild_type",
            "status": "I"
        }
        test_name = "Test: Update Contact fail"
        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 400,
            msg=f"{test_name} - Status Code was not 400")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    # =========================================================================
    # Client Contact Tests
    # =========================================================================
    def add_client_contact(self, contact_data) -> TestResponse:
        # return the response
        return self.client().post(
            '/api/clients',
            headers=self.headers,
            json=contact_data)

    def update_client_contact(self, contact_data, client_contact_id=99) -> TestResponse:
        # return the response
        return self.client().patch(
            f"/api/clients/{self.client_id}/contacts/{client_contact_id}",
            headers=self.headers,
            json=contact_data)

    def test_add_client_contact_success(self):
        contact_data = {
            "name": "Will Power",
            "client_id": self.client_id,
            "email_address": "wpower@company.com.au",
            "phone": "0412987654",
            "position_title": "Test Contact"
        }

        response = self.add_client_contact(contact_data)
        data: dict = json.loads(response.data)

        self.assertEqual(
            response.status_code, 200,
            msg="The Reponse Code was not 200.")
        self.assertIn(
            'success', data,
            msg="The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successful")
        self.assertIn(
            'data', data,
            msg="The reponse did not contain the contact data")

        client_contact: dict = data.get('data')
        self.client_contact_id = client_contact.get('id', 1)

    def test_add_client_contact_fail(self):
        # fails - no client id
        contact_data = {
            "name": "Will Power",
            "phone": "0412987654",
            "position_title": "Test Contact"
        }

        response = self.add_client_contact(contact_data)
        data: dict = json.loads(response.data)

        self.assertEqual(
            response.status_code, 400,
            msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data,
            msg="The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_get_client_contact_list_success(self):
        test_name = "Test: Get Client Contact List success"
        response = self.client().get(
            f"/api/clients/{self.client_id}/contacts",
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - Status Code was not 200")
        self.assertIn(
            'data', data,
            msg=f"{test_name} - The response does not contain a questions array")
        self.assertIn(
            'success', data,
            msg=f"{test_name} - The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - The success indicator is not equal to true")

    def test_get_client_contact_list_fail(self):
        test_name = "Test: Get Client Contact List fail"
        response = self.client().get('/api/clients/99/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=f"{test_name} - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    def test_get_client_contact_success(self):
        test_name = "Test: Get Client Contact success"
        response = self.client().get(
            f"/api/clients/{self.client_id}/contacts/{self.client_contact_id}",
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - The response did not report as successful")
        self.assertIn(
            'data', data,
            msg=f"{test_name} - The reponse did not contain the contact data")

    def test_get_client_contact_fail(self):
        test_name = "Test: Get Client Contact fail"
        response = self.client().get(
            f"/api/clients/{self.client_id}/contacts/99",
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=f"{test_name} - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    def test_update_client_contact_success(self):
        contact_data = {
            "name": "William Power",
            "phone": "9876543210",
            "position_title": "Test Contact",
            "email_address": "will@power.com"
        }

        # Run the update attempt
        response = self.update_client_contact(contact_data, self.client_contact_id)
        # get the response body
        data = json.loads(response.data)
        # run the tests
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg="the response did not report as successfult")
        self.assertIn(
            'data', data,
            msg="The reponse did not contain the contact data")

    def test_update_client_contact_fail(self):
        contact_data = {
            "name": "William Power",
            "phone": "9876543210",
            "position_title": "Test Contact",
            "email_address": "will@power.com"
        }

        # Run the update attempt
        response = self.update_client_contact(contact_data)
        # get the response body
        data = json.loads(response.data)
        # run the tests
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_delete_client_contact_success(self):

        response = self.client().delete(
            f"/api/clients/{self.client_id}/contacts/{self.client_contact_id}",
            headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successful")
        self.assertIn(
            'id', data,
            msg="The reponse did not contain the deleted Id")
        self.assertEqual(
            data['id'], self.client_id,
            msg="The deleted contact did not match the id sent")

    def test_delete_client_contact_fail(self):
        response = self.client().delete(
            f"/api/clients/{self.client_id}/contacts/99",
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    # =========================================================================
    # Client Delete Tests
    # =========================================================================

    def test_delete_client_success(self):
        test_name = "Test: Delete Client success"
        response = self.client().delete(
            f'/api/clients/{self.client_id}',
            headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - The response did not report as successful")
        self.assertIn(
            'id', data,
            msg=f"{test_name} - The reponse did not contain the deleted Id")
        self.assertEqual(
            data['id'], self.client_id,
            msg=f"{test_name} - The deleted contact did not match the id sent")

    def test_delete_client_fail(self):
        test_name = "Test: Delete Client fail"
        response = self.client().delete('/api/clients/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=f"{test_name} - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - the response did not report as failed")

    # =========================================================================
    # Report Tests
    # =========================================================================

    def test_add_report_success(self):
        report_data = {
            "client_id": 1,
            "client_contact_id": 1,
            "consulant_id": 1,
            "client_manager_id": 2,
            "report_date": "2021-08-02",
            "report_from_date": "2021-08-01",
            "report_to_date": "2021-08-02",
            "engagement_reference": "LC1234"
        }

        response = self.client().post('/api/reports', headers=self.headers,  json=report_data)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Add Report success - The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Add Report success - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Report success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the report data")

        # save the repot id for later tests
        self.report_id = data.get('id', default=1, type=int)

    def test_add_report_fail(self):

        report_data = {
            "client_id": 99,
            "client_contact_id": 1,
            "consulant_id": 1,
            "client_manager_id": 2,
            "report_date": "2021-08-02",
            "report_from_date": "2021-08-01",
            "report_to_date": "2021-08-02",
            "engagement_reference": "LC1234"
        }

        response = self.client().post('/api/reports', headers=self.headers,  json=report_data)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Add Report fail - The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Add Report fail - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Add Report fail - the response did not report as failed")

    def test_get_report_list_success(self):
        response = self.client().get('/api/reports', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get report list - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get reports list - the response does not contain a data object")
        self.assertIn(
            'success', data, msg="Test: Get reports list - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get reports list - the success indicator is not equal to true")

    def test_get_report_list_fail(self):
        test_name = "Get Reports List fail - "
        response = self.client().get('/api/reports?page=99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg=test_name + "Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=test_name + "The response did not report as failed")

    def test_get_report_success(self):
        test_name = "Get Report success - "
        response = self.client().get(
            f"/api/reports/{self.report_id}", headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=test_name + "Status Code was not 200")
        self.assertIn(
            'data', data,
            msg=test_name + "The response does not contain a data object")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=test_name + "The success indicator is not equal to true")

    def test_get_report_fail(self):
        test_name = "Get Report fail - "
        response = self.client().get("/api/reports/99", headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=test_name + "Status Code was not 404")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg=test_name + "The success indicator is not equal to false")

    def test_update_report_success(self):
        test_name = "Update Report success - "
        report_data = {
            "client_id": 1,
            "client_contact_id": 1,
            "consulant_id": 1,
            "client_manager_id": 2,
            "report_date": "2021-08-02",
            "report_from_date": "2021-08-01",
            "report_to_date": "2021-08-02",
            "engagement_reference": "LC1234",
            "report_status": "complete"
        }

        response = self.client().patch(
            f"/api/reports/{self.report_id}", headers=self.headers,  json=report_data)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=test_name + "The Reponse Code was not 200")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=test_name + "The response did not report as failed")
        self.assertIn(
            'data', data,
            msg=test_name + "The reponse did not contain the report data")

    def test_update_report_failed(self):
        test_name = "Update Report fail - "
        report_data = {
            "client_id": 1,
            "client_contact_id": 1,
            "consulant_id": 1,
            "client_manager_id": 2,
            "report_date": "2021-08-02",
            "report_from_date": "2021-08-01",
            "report_to_date": "2021-08-02",
            "engagement_reference": "LC1234",
            "report_status": "invalid_status"
        }

        response = self.client().patch(
            f"/api/reports/{self.report_id}", headers=self.headers,  json=report_data)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 400,
            msg=test_name + "The Reponse Code was not 400")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=test_name + "The response did not report as failed")
        self.assertIn(
            'data', data,
            msg=test_name + "The reponse did not contain the report data")

    # =========================================================================
    # Report Item Tests
    # =========================================================================
    def test_add_report_item_success(self):
        report_data = {
            "item_type": "requested_task",
            "item_sequence_nbr": 1,
            "item_description": "aliquam etiam erat velit scelerisque in dictum non consectetur a erat nam at lectus urna duis convallis convallis tellus id",
            "item_complete": True,
            "request_expected_outcome": "nunc lobortis mattis aliquam faucibus purus in massa tempor nec"
        }
        test_name = "Test: Add Report Item success - "
        response = self.client().post(
            f"/api/reports/{self.report_id}/items",
            headers=self.headers,
            json=report_data)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=test_name + "Test: Add Report Item success - The Reponse Code was not 200")
        self.assertIn(
            'success', data,
            msg=test_name + "Test: Add Report Item success - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=test_name + "Test: Add Report Item success - the response did not report as successful")
        self.assertIn(
            'data', data,
            msg=test_name + "The reponse did not contain the report item data")

        self.report_item_id = data.get('report_item_nbr', default=1, type=int)

    def test_add_report_item_fail(self):

        report_data = {
            "item_type": "requested_task",
            "item_sequence_nbr": 1,
            "item_complete": True,
            "request_expected_outcome": "nunc lobortis mattis aliquam faucibus purus in massa tempor nec"
        }
        test_name = "Test: Add Report Item fail - "
        endpoint = f"/api/reports/{self.report_id}/items"
        response = self.client().post(endpoint, headers=self.headers,  json=report_data)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 400,
            msg=test_name + "The Reponse Code was not 400")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg=test_name + "The response did not report as failed")

    def test_get_report_items_list_success(self):
        test_name = "Test: Get Report Item List success - "
        response = self.client().get(
            f"/api/reports/{self.report_id}/items", headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=test_name + "The Reponse Code was not 200")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=test_name + "The response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the report item data")

    def test_get_report_items_list_fail(self):
        test_name = "Test: Get Report Item List fail - "
        response = self.client().post("/api/reports/99/items",
                                      headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=test_name + "The Reponse Code was not 404")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg=test_name + "The response did not report as failed")

    def test_get_report_item_success(self):
        test_name = "Test: Get Report Item success - "
        response = self.client().get(
            f"/api/reports/{self.report_id}/items/{self.report_item_id}",
            headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=test_name + "The Reponse Code was not 200")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=test_name + "The response did not report as successful")
        self.assertIn(
            'data', data,
            msg=test_name + "The reponse did not contain the report item data")

    def test_get_report_item_failed(self):
        test_name = "Test: Get Report Item fail - "
        response = self.client().get(
            f"/api/reports/{self.report_id}/items/99",
            headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=test_name + "The Reponse Code was not 404")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg=test_name + "The response did not report as failed")

    def test_update_report_item_success(self):
        report_data = {
            "item_type": "requested_task",
            "item_sequence_nbr": 1,
            "item_description": "aliquam etiam erat velit scelerisque in dictum non consectetur a erat nam at lectus urna duis convallis convallis tellus id",
            "item_complete": True,
            "request_expected_outcome": "nunc lobortis mattis aliquam faucibus purus in massa tempor nec"
        }
        test_name = "Test: Update Report Item success - "
        response = self.client().patch(
            f"/api/reports/{self.report_id}/items/{self.report_item_id}",
            headers=self.headers,
            json=report_data)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=test_name + "The Reponse Code was not 200")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=test_name + "The response did not report as successful")
        self.assertIn(
            'data', data,
            msg=test_name + "The reponse did not contain the report item data")

    def test_update_report_item_failed(self):

        report_data = {
            "item_type": "requested_task",
            "item_sequence_nbr": 1,
            "item_description": None,
            "item_complete": True,
            "request_expected_outcome": "nunc lobortis mattis aliquam faucibus purus in massa tempor nec"
        }
        test_name = "Test: Update Report Item success - "
        endpoint = f"/api/reports/{self.report_id}/items/{self.report_item_id}"
        response = self.client().patch(endpoint, headers=self.headers,  json=report_data)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 400,
            msg=test_name + "The Reponse Code was not 400")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg=test_name + "The response did not report as failed")

    def test_delete_report_item_success(self):
        test_name = "Test: Delete Report Item success - "
        endpoint = f"/api/reports/{self.report_id}/items/{self.report_item_id}"
        response = self.client().delete(endpoint, headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg=test_name + "The Reponse Code was not 200")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=test_name + "The response did not report as successful")

    def test_delete_report_item_failed(self):
        test_name = "Test: Delete Report Item fail - "
        endpoint = f"/api/reports/{self.report_id}/items/99"
        response = self.client().delete(endpoint, headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg=test_name + "The Reponse Code was not 200")
        self.assertIn(
            'success', data,
            msg=test_name + "The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=test_name + "The response did not report as successful")

    def test_delete_report_success(self):
        test_name = "Test: Delete Report success - "
        endpoint = f"/api/reports/{self.report_id}"
        response = self.client().delete(endpoint, headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=test_name + "Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg=test_name + "The response did not report as successful")

    def test_delete_report_fail(self):
        test_name = "Test: Delete Report fail - "
        response = self.client().delete('/api/reports/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=test_name + "Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=test_name + "The response did not report as failed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
