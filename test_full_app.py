from datetime import date
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Headers
from werkzeug.wrappers import response
import http
from api import create_app
from config import TestConfig

def generate_access_token():
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_1')
    AUTH0_SECRET = os.getenv('AUTH0_SECRET_1')

    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = f'{{"client_id":"{AUTH0_CLIENT_ID}}}",' \
        f'"client_secret":"{AUTH0_SECRET}",' \
        f'"audience":"{AUTH0_AUDIENCE}",' \
        '"grant_type":"client_credentials"}'

    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


class FullTestSuite(unittest.TestCase):
    """This class performs the full suite of test cases for the CAR app"""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client

        # Get a token so that the protected end points can be reached

        token_dict: dict = generate_access_token()
        self.headers: dict = {
            "Authorization": f"Bearer {token_dict.get('access_token')}"}
        self.contact_id = 0
        self.client_id = 0
        self.client_contact_id = 0
        self.report_id = 0
        self.report_item_id = 0

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    # =========================================================================
    # Internal Contact Tests
    # =========================================================================

    def test_add_contact_success(self):

        contact_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }
        test_name = "Test: Add Contact success"
        response = self.client().post(
            '/api/contacts',
            headers=self.headers,
            json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - The Reponse Code was not 200")
        self.assertIn(
            'success', data,
            msg=f"{test_name} - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.contact_id = data.get('id', default=1)

    def test_add_contact_fail(self):
        contact_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }
        test_name = "Test: Add Contact fail"
        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 400,
            msg=f"{test_name} - The Reponse Code was not 400")
        self.assertIn(
            'success', data,
            msg=f"{test_name} - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - the response did not report as failed")

    def test_get_contact_list_success(self):
        test_name = "Test: Get Contacts List success"
        response = self.client().get('/api/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - Status Code was not 200")
        self.assertIn(
            'data', data,
            msg=f"{test_name} - The response does not contain a questions array")
        self.assertIn(
            'success', data, msg=f"{test_name} - The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - The success indicator is not equal to true")

    def test_get_contact_list_fail(self):
        test_name = "Test: Get Contacts List fail"
        response = self.client().get('/api/contacts?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=f"{test_name} - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    def test_get_contact_success(self):
        test_name = "Test: Get Contact Success"
        response = self.client().get(
            f'/api/contacts/{self.contact_id}',
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
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "I"
        }
        test_name = "Test: Update Contact success"
        response = self.client().patch(
            f'/api/contacts/{self.contact_id}',
            headers=self.headers,
            json=contact_data)

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

    def test_update_contact_failed(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "invaild_type",
            "status": "I"
        }
        test_name = "Test: Update Contact fail"
        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 400,
            msg=f"{test_name} - Status Code was not 400")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    def test_delete_contact_success(self):
        test_name = "Test: Delete Contact success"
        response = self.client().delete(
            f'/api/contacts/{self.contact_id}',
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
            msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], self.contact_id,
            msg=f"{test_name} - The deleted contact did not match the id sent")

    def test_delete_contact_fail(self):
        test_name = "Test: Delete Contact fail"
        response = self.client().delete(
            '/api/contacts/99',
            headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=f"{test_name} - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - the response did not report as failed")

    # =========================================================================
    # Client Tests
    # =========================================================================
    def test_add_client_success(self):
        client_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
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

        self.client_id = data.get('id', default=1)

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
    def test_add_client_contact_success(self):
        client_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }
        test_name = "Test: Add Client Contacts success"
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

        self.client_contact_id = data.get('id', default=1)

    def test_add_client_contact_fail(self):
        client_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }
        test_name = "Test: Add Client Contacts fail"
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
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "I"
        }
        test_name = "Test: Update Client Contact success"
        response = self.client().patch(
            f"/api/clients/{self.client_id}/contacts/{self.client_contact_id}",
            headers=self.headers,
            json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - the response did not report as successfult")
        self.assertIn(
            'data', data,
            msg=f"{test_name} - The reponse did not contain the contact data")

    def test_update_client_contact_fail(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "invaild_type",
            "status": "I"
        }
        test_name = "Test: Update Client Contact fail"
        response = self.client().patch(
            f"/api/clients/{self.client_id}/contacts/99",
            headers=self.headers,
            json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=f"{test_name} - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - the response did not report as failed")

    def test_delete_client_contact_success(self):
        test_name = "Test: Delete Client Contact success"
        response = self.client().delete(
            f"/api/clients/{self.client_id}/contacts/{self.client_contact_id}",
            headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg=f"{test_name} - Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg=f"{test_name} - the response did not report as successful")
        self.assertIn(
            'id', data,
            msg="The reponse did not contain the deleted Id")
        self.assertEqual(
            data['id'], self.client_id,
            msg=f"{test_name} - The deleted contact did not match the id sent")

    def test_delete_client_contact_fail(self):
        test_name = "Test: Delete Client Contact fail"
        response = self.client().delete(
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


class ClientMgrTest(unittest.TestCase):
    """This class performs the client manager suite of test cases for the CAR app"""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client

        client_id = os.getenv('AUTH0_CLIENT_2')
        secret = os.getenv('AUTH0_SECRET_2')

        # Get a token so that the protected end points can be reached
        token_dict: dict = generate_access_token(client_id, secret)
        self.headers: dict = {
            "Authorization": f"Bearer {token_dict.get('access_token')}"}
        self.contact_id = 1
        self.client_id = 1

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_contact_list_success(self):
        response = self.client().get('/api/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contacts - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get Contacts - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get Contacts - the success indicator is not equal to true")

    def test_get_contact_list_fail(self):
        response = self.client().get('/api/contacts?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get Contacts Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get Contacts Fail - the response did not report as failed")

    def test_add_contact_success(self):
        contact_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.contact_id = data.get('id', default=1)

    def test_add_contact_fail(self):
        contact_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get Contacts Fail - the response did not report as failed")

    def test_get_contact_success(self):
        response = self.client().get(
            f'/api/contacts/{self.contact_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get Contacts Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_contact_fail(self):
        response = self.client().get('/api/contacts/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get Contacts Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get Contacts Fail 404 - the response did not report as failed")

    def test_update_contact_success(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update Contacts Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_contact_failed(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update Contacts Success - the response did not report as failed")

    def test_delete_contact_success(self):
        response = self.client().delete(
            f'/api/contacts/{self.contact_id}', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Delete Contact - Status Code was not 200")
        self.assertEqual(
            data['success'], True, msg="Test: Delete Contact - the response did not report as successful")
        self.assertIn(
            'id', data, msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], self.contact_id, msg="Test: Delete Contact - the deleted contact did not match the id sent")

    def test_delete_contact_fail(self):
        response = self.client().delete('/api/contacts/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")

    # -------------------------------------------------------------------------
    # Client Tests
    # -------------------------------------------------------------------------
    def test_get_client_list_success(self):
        response = self.client().get('/api/clients', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get clients - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get clients - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get clients - the success indicator is not equal to true")

    def test_get_client_list_fail(self):
        response = self.client().get('/api/clients?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_add_client_success(self):
        client_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.client_id = data.get('id', default=1)

    def test_add_client_fail(self):
        client_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_get_client_success(self):
        response = self.client().get(
            f'/api/clients/{self.client_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get clients Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_client_fail(self):
        response = self.client().get('/api/clients/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get clients Fail 404 - the response did not report as failed")

    def test_update_client_success(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update clients Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_client_failed(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update clients Success - the response did not report as failed")

    def test_delete_client_success(self):
        response = self.client().delete(
            f'/api/clients/{self.client_id}', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Delete Contact - Status Code was not 200")
        self.assertEqual(
            data['success'], True, msg="Test: Delete Contact - the response did not report as successful")
        self.assertIn(
            'id', data, msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], self.client_id, msg="Test: Delete Contact - the deleted contact did not match the id sent")

    def test_delete_client_fail(self):
        response = self.client().delete('/api/clients/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")


class ConsultantTest(unittest.TestCase):
    """This class performs the client manager suite of test cases for the CAR app"""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client

        client_id = os.getenv('AUTH0_CLIENT_3')
        secret = os.getenv('AUTH0_SECRET_3')

        # Get a token so that the protected end points can be reached
        token_dict: dict = generate_access_token(client_id, secret)
        self.headers: dict = {
            "Authorization": f"Bearer {token_dict.get('access_token')}"}
        self.contact_id = 1
        self.client_id = 1

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_contact_list_success(self):
        response = self.client().get('/api/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contacts - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get Contacts - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get Contacts - the success indicator is not equal to true")

    def test_get_contact_list_fail(self):
        response = self.client().get('/api/contacts?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get Contacts Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get Contacts Fail - the response did not report as failed")

    def test_add_contact_success(self):
        contact_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.contact_id = data.get('id', default=1)

    def test_add_contact_fail(self):
        contact_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get Contacts Fail - the response did not report as failed")

    def test_get_contact_success(self):
        response = self.client().get(
            f'/api/contacts/{self.contact_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get Contacts Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_contact_fail(self):
        response = self.client().get('/api/contacts/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get Contacts Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get Contacts Fail 404 - the response did not report as failed")

    def test_update_contact_success(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update Contacts Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_contact_failed(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update Contacts Success - the response did not report as failed")

    def test_delete_contact_success(self):
        response = self.client().delete(
            f'/api/contacts/{self.contact_id}', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Delete Contact - Status Code was not 200")
        self.assertEqual(
            data['success'], True, msg="Test: Delete Contact - the response did not report as successful")
        self.assertIn(
            'id', data, msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], self.contact_id, msg="Test: Delete Contact - the deleted contact did not match the id sent")

    def test_delete_contact_fail(self):
        response = self.client().delete('/api/contacts/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")

    # -------------------------------------------------------------------------
    # Client Tests
    # -------------------------------------------------------------------------
    def test_get_client_list_success(self):
        response = self.client().get('/api/clients', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get clients - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get clients - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get clients - the success indicator is not equal to true")

    def test_get_client_list_fail(self):
        response = self.client().get('/api/clients?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_add_client_success(self):
        client_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.client_id = data.get('id', default=1)

    def test_add_client_fail(self):
        client_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_get_client_success(self):
        response = self.client().get(
            f'/api/clients/{self.client_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get clients Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_client_fail(self):
        response = self.client().get('/api/clients/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get clients Fail 404 - the response did not report as failed")

    def test_update_client_success(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update clients Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_client_failed(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update clients Success - the response did not report as failed")

    def test_delete_client_fail(self):
        response = self.client().delete('/api/clients/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
