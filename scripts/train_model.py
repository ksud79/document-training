"""
train_model.py — Train an Azure Document Intelligence custom extraction model.

Required env vars (set in .env or environment):
  AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
  AZURE_DOCUMENT_INTELLIGENCE_KEY
  AZURE_BLOB_CONTAINER_SAS_URL   — SAS URL for the blob container holding training PDFs
  MODEL_ID                       — (optional) defaults to smsf-annual-return-2024
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceAdministrationClient
from azure.ai.documentintelligence.models import (
    BuildDocumentModelRequest,
    AzureBlobContentSource,
    DocumentBuildMode,
)
from azure.core.credentials import AzureKeyCredential

load_dotenv()

ENDPOINT   = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
KEY        = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
SAS_URL    = os.getenv("AZURE_BLOB_CONTAINER_SAS_URL")
MODEL_ID   = os.getenv("MODEL_ID", "smsf-annual-return-2024")

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

def check_env():
    missing = [v for v in ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
                            "AZURE_DOCUMENT_INTELLIGENCE_KEY",
                            "AZURE_BLOB_CONTAINER_SAS_URL"] if not os.getenv(v)]
    if missing:
        print(f"ERROR: Missing required env vars: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

def main():
    check_env()

    admin_client = DocumentIntelligenceAdministrationClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(KEY),
    )

    print(f"Starting training for model: {MODEL_ID}")
    print(f"Training data source: {SAS_URL[:60]}...")

    request = BuildDocumentModelRequest(
        model_id=MODEL_ID,
        build_mode=DocumentBuildMode.TEMPLATE,
        azure_blob_source=AzureBlobContentSource(container_url=SAS_URL),
        description="SMSF Annual Return 2024 (NAT 71226) custom extraction model",
    )

    poller = admin_client.begin_build_document_model(request)

    print("Training in progress — polling every 10 seconds...")
    while not poller.done():
        time.sleep(10)
        print("  ...", flush=True)

    model = poller.result()
    print(f"\nTraining complete!")
    print(f"  Model ID:      {model.model_id}")
    print(f"  Created:       {model.created_date_time}")
    if model.description:
        print(f"  Description:   {model.description}")

    if hasattr(model, "doc_types") and model.doc_types:
        for doc_type_name, doc_type in model.doc_types.items():
            print(f"\nDocument type: {doc_type_name}")
            if hasattr(doc_type, "field_schema") and doc_type.field_schema:
                for field_name, field_info in doc_type.field_schema.items():
                    confidence = ""
                    if hasattr(doc_type, "field_confidence") and doc_type.field_confidence:
                        conf_val = doc_type.field_confidence.get(field_name)
                        if conf_val is not None:
                            confidence = f"  (confidence: {conf_val:.2%})"
                    print(f"  {field_name}: {field_info.get('type', 'unknown')}{confidence}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model_id_file = OUTPUT_DIR / "model_id.txt"
    model_id_file.write_text(model.model_id)
    print(f"\nModel ID saved to: {model_id_file}")


if __name__ == "__main__":
    main()
