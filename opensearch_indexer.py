import json
import logging
from typing import Dict

from opensearchpy import OpenSearch, RequestsHttpConnection

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OpenSearchIndexer:
    def __init__(self, config: Dict[str, Dict[str, str]]):
        self.host = config["opensearch"]["host"]
        self.index_name = config["opensearch"]["index_name"]
        self.client = OpenSearch(
            hosts=[{"host": self.host.replace("https://", ""), "port": 443}],
            http_auth=None,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )
        self._ensure_index()

    def _ensure_index(self) -> None:
        if not self.client.indices.exists(self.index_name):
            body = {
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "content": {"type": "text"},
                        "metadata": {"type": "object", "enabled": False},
                        "embedding": {"type": "dense_vector", "dims": 128},
                    }
                }
            }
            self.client.indices.create(index=self.index_name, body=body)
            logger.info("Created OpenSearch index %s", self.index_name)

    def index_document(self, doc: Dict[str, str]) -> None:
        body = {
            "document_id": doc["id"],
            "title": doc["title"],
            "content": doc.get("text", ""),
            "metadata": doc.get("metadata", {}),
            "embedding": doc.get("embedding", []),
        }
        self.client.index(index=self.index_name, id=doc["id"], body=body)
        logger.info("Indexed document %s in OpenSearch", doc["id"])

    def search_semantic(self, query_vector: list, size: int = 10):
        request = {
            "size": size,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_vector,
                        "k": size,
                    }
                }
            }
        }
        return self.client.search(body=request, index=self.index_name)
