import os
import json
import http
from dotenv import load_dotenv

GOOD_CONTACT_DATA = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }


GOOD_CLIENT_DATA = {
            "name": "The Powerhouse",
            "bus_reg_nbr": "12345678901",
            "abbreviation": "TPH"
        }

GOOD_CLIENT_CONTACT_DATA = {
            "name": "Will Power",
            "client_id": 0,
            "email_address": "wpower@company.com.au",
            "phone": "0412987654",
            "position_title": "Test Contact"
        }

def generate_auth_token(client_id, client_secret) -> dict:
    load_dotenv()
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
    AUTH0_CLIENT_ID = os.getenv(client_id)
    AUTH0_CLIENT_SECRET = os.getenv(client_secret)

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