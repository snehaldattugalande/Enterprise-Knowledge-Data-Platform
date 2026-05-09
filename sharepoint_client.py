import base64
import json
import logging
import os
from typing import Any, Dict, List

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SharePointClient:
    def __init__(self, config: Dict[str, Any]):
        self.tenant_id = config["sharepoint"]["tenant_id"]
        self.client_id = config["sharepoint"]["client_id"]
        self.client_secret = config["sharepoint"]["client_secret"]
        self.site_url = config["sharepoint"]["site_url"].rstrip("/")
        self.library_name = config["sharepoint"]["library_name"]
        self.access_token = self._authenticate()

    def _authenticate(self) -> str:
        token_url = (
            f"https://accounts.accesscontrol.windows.net/{self.tenant_id}/tokens/OAuth/2"
        )
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "resource": "00000003-0000-0ff1-ce00-000000000000/"
            + self.site_url,
        }
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        token_data = response.json()
        return token_data["access_token"]

    def list_documents(self) -> List[Dict[str, Any]]:
        endpoint = (
            f"{self.site_url}/_api/web/lists/GetByTitle('{self.library_name}')/items"
        )
        headers = {"Authorization": f"Bearer {self.access_token}", "Accept": "application/json;odata=verbose"}
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("d", {}).get("results", [])

    def get_document_content(self, item_id: int) -> bytes:
        endpoint = (
            f"{self.site_url}/_api/web/lists/GetByTitle('{self.library_name}')/items({item_id})/File/$value"
        )
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.content

    def extract_document_records(self) -> List[Dict[str, Any]]:
        documents = self.list_documents()
        records = []
        for item in documents:
            item_id = item.get("Id")
            content = self.get_document_content(item_id)
            text_base64 = base64.b64encode(content).decode("utf-8")
            records.append(
                {
                    "id": item_id,
                    "title": item.get("Title"),
                    "created": item.get("Created"),
                    "modified": item.get("Modified"),
                    "author": item.get("Author", {}).get("Title"),
                    "content_base64": text_base64,
                    "metadata": item,
                }
            )
        return records
