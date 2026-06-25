"""
test_model.py — Test the trained Azure Document Intelligence model against a PDF.

Usage:
  python scripts/test_model.py path/to/document.pdf

The model ID is read from output/model_id.txt or the MODEL_ID env var.

Required env vars (set in .env or environment):
  AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
  AZURE_DOCUMENT_INTELLIGENCE_KEY
  MODEL_ID  — (optional if output/model_id.txt exists)
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
KEY      = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def resolve_model_id():
    model_id = os.getenv("MODEL_ID")
    if model_id:
        return model_id
    model_id_file = OUTPUT_DIR / "model_id.txt"
    if model_id_file.exists():
        return model_id_file.read_text().strip()
    return None


def check_env():
    missing = [v for v in ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
                            "AZURE_DOCUMENT_INTELLIGENCE_KEY"] if not os.getenv(v)]
    if missing:
        print(f"ERROR: Missing required env vars: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <pdf_path>", file=sys.stderr)
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    check_env()

    model_id = resolve_model_id()
    if not model_id:
        print("ERROR: Model ID not found. Set MODEL_ID env var or run train_model.py first.",
              file=sys.stderr)
        sys.exit(1)

    client = DocumentIntelligenceClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(KEY),
    )

    print(f"Analysing: {pdf_path.name}")
    print(f"Model:     {model_id}\n")

    with open(pdf_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id=model_id,
            analyze_request=f,
            content_type="application/octet-stream",
        )

    result = poller.result()

    if not result.documents:
        print("No documents extracted.")
        sys.exit(0)

    for doc_idx, document in enumerate(result.documents):
        print(f"--- Document {doc_idx + 1} (type: {document.doc_type}) ---")
        print(f"    Confidence: {document.confidence:.2%}\n")
        if document.fields:
            for field_name, field in sorted(document.fields.items()):
                value = field.value_string or field.content or ""
                confidence = field.confidence if field.confidence is not None else 0.0
                print(f"  {field_name:<40} {str(value):<40} conf: {confidence:.2%}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_file = OUTPUT_DIR / "test_result.json"
    result_file.write_text(json.dumps(result.as_dict(), indent=2))
    print(f"\nRaw result saved to: {result_file}")


if __name__ == "__main__":
    main()
