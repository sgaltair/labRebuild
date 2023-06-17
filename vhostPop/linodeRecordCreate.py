import requests
import json
from vhostPopConfig import *

baseUrl = "https://api.linode.com/v4"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-type": "application/json"}


def createRecord(recordName: str, recordType: str):
    # Creates a domain record of the specified name and type, if it doesn't exist.
    newRecord = {
        "name": recordName,
        "target": TARGET_IP,
        "type": recordType,
    }

    existingRecords = requests.get(
        f"{baseUrl}/domains/{DOMAIN_ID}/records", headers=headers
    ).json()
    existingRecords = {
        result["name"]: result["id"] for result in existingRecords["data"]
    }

    if newRecord["name"] not in existingRecords.keys():
        try:
            response = requests.post(
                f"{baseUrl}/domains/{DOMAIN_ID}/records",
                headers=headers,
                data=json.dumps(newRecord),
            ).json()
            return True
        except:
            raise
    else:
        return False
