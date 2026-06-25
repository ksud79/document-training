"""
extract_to_json.py — Extract structured data from an SMSF return PDF using the trained model.

Usage:
  python scripts/extract_to_json.py path/to/document.pdf

Output is written to output/extracted_<filename>.json, grouped by section
as defined in config/fields.json.

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

REPO_ROOT  = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "output"
FIELDS_JSON = REPO_ROOT / "config" / "fields.json"


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


def load_field_map():
    """Build a mapping of pdf_field -> (section_key, field_meta) from fields.json."""
    if not FIELDS_JSON.exists():
        print(f"WARNING: {FIELDS_JSON} not found — output will not be grouped by section.")
        return {}

    with open(FIELDS_JSON) as f:
        config = json.load(f)

    field_map = {}
    for section_key, section in config.get("sections", {}).items():
        for field in section.get("fields", []):
            field_map[field["pdf_field"]] = {
                "section": section_key,
                "section_description": section.get("description", ""),
                "name": field.get("name", field["pdf_field"]),
                "description": field.get("description", ""),
                "type": field.get("type", "string"),
            }
    return field_map


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

    field_map = load_field_map()

    client = DocumentIntelligenceClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(KEY),
    )

    print(f"Extracting: {pdf_path.name}")
    print(f"Model:      {model_id}\n")

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

    # Build structured output grouped by section
    sections: dict = {}
    unmatched: dict = {}

    for document in result.documents:
        if not document.fields:
            continue
        for field_name, field in document.fields.items():
            value = field.value_string or field.content or ""
            confidence = field.confidence if field.confidence is not None else 0.0
            entry = {
                "value": value,
                "confidence": round(confidence, 4),
            }

            meta = field_map.get(field_name)
            if meta:
                sec = meta["section"]
                if sec not in sections:
                    sections[sec] = {
                        "description": meta["section_description"],
                        "fields": {},
                    }
                sections[sec]["fields"][field_name] = {
                    "name": meta["name"],
                    "description": meta["description"],
                    **entry,
                }
            else:
                unmatched[field_name] = entry

    output = {
        "source_file": pdf_path.name,
        "model_id": model_id,
        "sections": sections,
    }
    if unmatched:
        output["unmatched_fields"] = unmatched

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"extracted_{pdf_path.stem}.json"
    out_file.write_text(json.dumps(output, indent=2))

    total = sum(len(s["fields"]) for s in sections.values()) + len(unmatched)
    print(f"Extracted {total} fields across {len(sections)} sections.")
    print(f"Output saved to: {out_file}")


if __name__ == "__main__":
    main()
