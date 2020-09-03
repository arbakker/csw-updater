from urllib.parse import urljoin

import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.

LOGIN_PATH = "srv/dut/info?type=me"
CWS_PUBLICATION_PATH = "srv/dut/csw-publication"


class GeonetworkClient:
    def __init__(self, url, username, password):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        self.username = username
        self.password = password
        self.url = url
        if not url.endswith("/"):
            self.url = f"{url}/"
        self.ns = {"csw": "http://www.opengis.net/cat/csw/2.0.2",
                   "gmd": "http://www.isotc211.org/2005/gmd", "dc": "http://purl.org/dc/elements/1.1/",
                   "dct": "http://purl.org/dc/terms/"}
        self.session = requests.Session()
        self.login()

    def login(self):
        try:
            headers = {"Content-Type": "application/xml"}
            url = urljoin(self.url, LOGIN_PATH)
            body = f"<request><username>{self.username}</username><password>{self.password}</password></request>"
            response = self.session.post(url, data=body, verify=False, auth=(self.username, self.password))
            print(f"login status_code: {response.status_code}")
            print(f"user: {self.username}, pass: {self.password}")
            if (response.status_code == 200 or response.status_code == 301):
                response_text = response.text
                if response_text and "signin.html" in response_text:
                    return True
            return False
        except Exception as e:
            print(f"Error occured logging in to {self.url}")
            raise

    def update_metadata(self, metadata):
        self.csw_transaction_request(metadata, "Update")

    def insert_metadata(self, metadata):
        self.csw_transaction_request(metadata, "Insert")

    def delete_metadata(self, metadata_identifier):
        self.csw_transaction_delete_request(metadata_identifier)

    def csw_transaction_delete_request(self, metadata_identifier):
        try:
            template = """<?xml version="1.0" encoding="UTF-8"?>
    <csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ogc="http://www.opengis.net/ogc" version="2.0.2" service="CSW">
    <csw:Delete>
        <csw:Constraint version="1.1.0">
        <ogc:Filter>
            <ogc:PropertyIsEqualTo>
            <ogc:PropertyName>dc:identifier</ogc:PropertyName>
            <ogc:Literal>{metadata_identifier}</ogc:Literal>
            </ogc:PropertyIsEqualTo>
        </ogc:Filter>
        </csw:Constraint>
    </csw:Delete>
    </csw:Transaction>"""
            url = urljoin(self.url, CWS_PUBLICATION_PATH)
            print(f"url: {url}")
            body = template.replace("{metadata_identifier}", metadata_identifier)
            print(f"body: {body}")
            headers = {"Content-Type": "application/xml", "Accept": "application/xml"}
            response = self.session.post(url, data=body, verify=False, headers=headers,
                                         auth=(self.username, self.password))
            print(f"update_metadata status_code: {response.status_code}")
            print(f"update_metadata response body: {response.text}")
            if (response.status_code == 200 or response.status_code == 301):
                return True
            else:
                return False
        except Exception as e:
            print(f"Error occured logging in to {self.url}")
            raise

    def csw_transaction_request(self, metadata, csw_request_type):
        try:
            url = urljoin(self.url, CWS_PUBLICATION_PATH)
            print(f"url: {url}")
            template = """<?xml version="1.0" encoding="UTF-8"?>
<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" version="2.0.2" service="CSW">
  <csw:{csw_request_type}>
    {metadata}
  </csw:{csw_request_type}>
</csw:Transaction>"""
            template = template.replace("{metadata}", metadata)
            body = template.replace("{csw_request_type}", csw_request_type)
            print(f"body: {body}")
            headers = {"Content-Type": "application/xml", "Accept": "application/xml"}
            response = self.session.post(url, data=body, verify=False, headers=headers,
                                         auth=(self.username, self.password))
            print(f"update_metadata status_code: {response.status_code}")
            print(f"update_metadata response body: {response.text}")
            if (response.status_code == 200 or response.status_code == 301):
                return True
            else:
                return False
        except Exception as e:
            print(f"Error occured logging in to {self.url}")
            raise