"""
upload_to_blob.py — Upload filled sample PDFs from output/ to Azure Blob Storage.

Required env vars (set in .env or environment):
  AZURE_STORAGE_CONNECTION_STRING
  AZURE_BLOB_CONTAINER_NAME
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

load_dotenv()

CONN_STR       = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME")

if not CONN_STR:
    print("ERROR: AZURE_STORAGE_CONNECTION_STRING is not set.", file=sys.stderr)
    sys.exit(1)
if not CONTAINER_NAME:
    print("ERROR: AZURE_BLOB_CONTAINER_NAME is not set.", file=sys.stderr)
    sys.exit(1)

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

def main():
    if not OUTPUT_DIR.exists():
        print(f"ERROR: output directory not found: {OUTPUT_DIR}", file=sys.stderr)
        sys.exit(1)

    pdfs = sorted(OUTPUT_DIR.glob("*.pdf"))
    if not pdfs:
        print("No PDFs found in output/. Run generate_forms.py first.")
        sys.exit(0)

    client = BlobServiceClient.from_connection_string(CONN_STR)
    container = client.get_container_client(CONTAINER_NAME)

    try:
        container.create_container()
        print(f"Created container: {CONTAINER_NAME}")
    except ResourceExistsError:
        print(f"Container already exists: {CONTAINER_NAME}")

    uploaded = 0
    skipped  = 0

    for pdf_path in pdfs:
        blob_name = pdf_path.name
        blob_client = container.get_blob_client(blob_name)

        try:
            blob_client.get_blob_properties()
            print(f"  SKIP (exists): {blob_name}")
            skipped += 1
            continue
        except Exception:
            pass

        with open(pdf_path, "rb") as f:
            blob_client.upload_blob(f)
        print(f"  Uploaded: {blob_name}")
        uploaded += 1

    print(f"\nDone. {uploaded} uploaded, {skipped} skipped.")


if __name__ == "__main__":
    main()
