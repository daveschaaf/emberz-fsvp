import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("AIRTABLE_API_KEY")
BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
BASE_URL = f"https://api.airtable.com/v0/{BASE_ID}"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_records(table_name):
    """Fetch all records from a table, handling pagination."""
    url = f"{BASE_URL}/{requests.utils.quote(table_name)}"
    records = []
    params = {}

    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
        params["offset"] = offset

    return records

def create_record(table_name, fields):
    """Create a new record in a table."""
    url = f"{BASE_URL}/{requests.utils.quote(table_name)}"
    response = requests.post(url, headers=HEADERS, json={"fields": fields})
    response.raise_for_status()
    return response.json()

def update_record(table_name, record_id, fields):
    """Update an existing record by ID."""
    url = f"{BASE_URL}/{requests.utils.quote(table_name)}/{record_id}"
    response = requests.patch(url, headers=HEADERS, json={"fields": fields})
    response.raise_for_status()
    return response.json()

def delete_record(table_name, record_id):
    """Delete a record by ID."""
    url = f"{BASE_URL}/{requests.utils.quote(table_name)}/{record_id}"
    response = requests.delete(url, headers=HEADERS)
    response.raise_for_status()
