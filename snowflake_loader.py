import logging
from typing import Dict

import snowflake.connector

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SnowflakeLoader:
    def __init__(self, config: Dict[str, str]):
        self.account = config["snowflake"]["account"]
        self.user = config["snowflake"]["user"]
        self.password = config["snowflake"]["password"]
        self.warehouse = config["snowflake"]["warehouse"]
        self.database = config["snowflake"]["database"]
        self.schema = config["snowflake"]["schema"]
        self.role = config["snowflake"]["role"]

    def _connect(self):
        return snowflake.connector.connect(
            user=self.user,
            password=self.password,
            account=self.account,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema,
            role=self.role,
        )

    def load_document_record(self, record: Dict[str, str]) -> None:
        insert_sql = (
            "INSERT INTO DOCUMENT_CATALOG (DOCUMENT_ID, TITLE, AUTHOR, CREATED_AT, MODIFIED_AT, METADATA, CONTENT_BASE64) "
            "VALUES (%(id)s, %(title)s, %(author)s, %(created)s, %(modified)s, %(metadata)s, %(content_base64)s)"
        )
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(insert_sql, record)
                logger.info("Loaded record %s into Snowflake", record.get("id"))

    def create_schema(self) -> None:
        ddl = f"""
        CREATE TABLE IF NOT EXISTS {self.database}.{self.schema}.DOCUMENT_CATALOG (
            DOCUMENT_ID INTEGER,
            TITLE TEXT,
            AUTHOR TEXT,
            CREATED_AT TIMESTAMP_NTZ,
            MODIFIED_AT TIMESTAMP_NTZ,
            METADATA VARIANT,
            CONTENT_BASE64 TEXT
        );
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(ddl)
                logger.info("Snowflake schema and DOCUMENT_CATALOG table verified")
