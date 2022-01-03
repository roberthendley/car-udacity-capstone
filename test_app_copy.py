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
from dotenv import load_dotenv

load_dotenv()

def generate_access_token(client_id, client_secret):
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = f'{{"client_id":"{client_id}}}",' \
        f'"client_secret":"{client_secret}",' \
        f'"audience":"{AUTH0_AUDIENCE}",' \
        '"grant_type":"client_credentials"}'

    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode("utf-8")


class FullTestSuite(unittest.TestCase):
    """This class performs the full suite of test cases for the CAR app"""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client

        # Get a token so that the protected end points can be reached
        auth0_client_id = os.getenv('AUTH0_CLIENT_ADMIN')
        auth0_client_secret = os.getenv('AUTH0_SECRET_ADMIN')

        token_dict: dict = generate_access_token(auth0_client_id,auth0_client_secret)
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

    
# Make the tests conveniently executable
if __name__ == "__main__":
    load_dotenv()
    token_dict: dict = generate_access_token(os.getenv('AUTH0_CLIENT_ADMIN'),os.getenv('AUTH0_SECRET_ADMIN'))
    print (token_dict)
    # unittest.main()
