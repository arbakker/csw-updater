import logging
import os
from csw_updater.geonetwork_client import GeonetworkClient

logger = logging.getLogger(__name__)

CSW_USER = 'CSW_USER'
CSW_PASSWORD = 'CSW_PASSWORD'

def get_username_from_env():
    if CSW_USER in os.environ:
        return os.environ[CSW_USER]

def get_password_from_env():
    if CSW_PASSWORD in os.environ:
        return os.environ[CSW_PASSWORD]

def update_metadata(base_url, metadata_file, ngr_user, ngr_password):
    gn_client = GeonetworkClient(base_url, ngr_user, ngr_password)
    metadata = metadata_file.read()
    gn_client.insert_metadata(metadata)
    gn_client.update_metadata(metadata)
    gn_client.delete_metadata("16817852-ce74-47d3-b78f-76f7ae47ba94")