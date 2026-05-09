# Enterprise Knowledge Data Platform

A sample data engineering project for enterprise document ingestion, transformation, Snowflake analytics, and OpenSearch semantic retrieval.

## Overview

- Ingests structured and unstructured documents from SharePoint.
- Transforms documents and extracts metadata using AWS Lambda and Python.
- Loads data into Snowflake for analytics and natural language query support.
- Indexes embeddings in OpenSearch for semantic retrieval.
- Supports event-driven near real-time synchronization via AWS events.

## Project Structure

- `architecture.md` - architecture design and integration overview.
- `config.yaml` - platform configuration settings.
- `requirements.txt` - Python dependencies.
- `serverless.yml` - AWS Lambda deployment and event definitions.
- `template.yaml` - AWS SAM deployment template.
- `Dockerfile` - container image build definition.
- `.env.example` - local environment variable sample file.
- `scripts/cli.py` - CLI for local ingestion, transformation, and sync.
- `scripts/sample_query.py` - OpenSearch sample query script.
- `sharepoint_client.py` - SharePoint extraction utility.
- `snowflake_loader.py` - Snowflake loading and warehouse integration.
- `opensearch_indexer.py` - OpenSearch indexing and retrieval.
- `lambdas/ingest_documents.py` - Lambda to ingest documents from SharePoint.
- `lambdas/transform_metadata.py` - Lambda to transform documents and metadata.
- `lambdas/sync_event_handler.py` - Event-driven synchronization handler.
- `utils.py` - common helpers for JSON, logging, and config.
- `snowflake/schema.sql` - Snowflake schema and table DDL.
- `tests/` - unit tests for core helpers and clients.

## Getting Started

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Configure `config.yaml` with SharePoint, AWS, Snowflake, and OpenSearch parameters.

3. Deploy the AWS Lambda stack using your preferred deployment tool.

4. Run ingestion and transformation functions to begin document processing.

## Local Development

- Use `scripts/cli.py` to run ingestion, transform, or sync locally:

```bash
python scripts/cli.py ingest
python scripts/cli.py transform
python scripts/cli.py sync
```

- Run the sample OpenSearch query script:

```bash
python scripts/sample_query.py
```

## Docker

Build and run the container locally:

```bash
docker build -t enterprise-knowledge-platform .
```

## Tests

Run tests with pytest:

```bash
pytest tests
```

## Snowflake Schema

Create the Snowflake schema and tables from `snowflake/schema.sql`.
