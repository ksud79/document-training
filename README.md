# SMSF Annual Return – Azure Document Intelligence Training

This repository is used to train an **Azure Document Intelligence** custom extraction model for the **ATO Self-Managed Superannuation Fund (SMSF) Annual Return 2024** (NAT 71299).

Once trained, the model is consumed by the [smsf-collective](https://github.com/ksud79/smsf-collective) application to automatically extract data from lodged returns.

---

## Overview

The workflow is:

```
PDF Samples → Azure Blob Storage → Label in Studio → Train Model → Test → Extract to JSON → smsf-collective
```

---

## Prerequisites

- Python 3.8+
- Azure subscription with a **Document Intelligence** resource (S0 tier or higher for custom models)
- Azure **Blob Storage** account
- Access to [Azure Document Intelligence Studio](https://documentintelligence.ai.azure.com)

---

## Environment Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/ksud79/document-training.git
   cd document-training
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your Azure credentials:
   ```bash
   cp .env.example .env
   ```

---

## Environment Variables

| Variable | Description |
|---|---|
| `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` | Your Document Intelligence resource endpoint |
| `AZURE_DOCUMENT_INTELLIGENCE_KEY` | Your Document Intelligence API key |
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Blob Storage connection string |
| `AZURE_BLOB_CONTAINER_NAME` | Name of the blob container holding PDF samples |
| `AZURE_BLOB_CONTAINER_SAS_URL` | SAS URL for the container (used for training) |
| `MODEL_ID` | Set after training; used by test and extract scripts |

---

## Step-by-Step Workflow

### Step 1 – Upload PDF Samples to Blob Storage

You need **at least 5** sample SMSF Annual Return PDFs. Upload them to your Azure Blob Storage container.

See [`training/README.md`](training/README.md) for detailed instructions.

> ⚠️ Do NOT commit PDF files to this repository.

### Step 2 – Label Fields in Document Intelligence Studio

1. Open [Azure Document Intelligence Studio](https://documentintelligence.ai.azure.com)
2. Create a new **Custom Extraction** project
3. Connect the project to your blob storage container
4. Label each field on each PDF using the field names defined in [`config/fields.json`](config/fields.json)

See [`training/README.md`](training/README.md) for full labelling instructions.

### Step 3 – Train the Model

```bash
python scripts/train_model.py
```

This will trigger training, poll until complete, print field statistics, and save the model ID to `output/model_id.txt`.

### Step 4 – Test the Model

```bash
python scripts/test_model.py path/to/sample.pdf
```

This will print all extracted fields with confidence scores and save the raw result to `output/test_result.json`.

### Step 5 – Extract to Structured JSON

```bash
python scripts/extract_to_json.py path/to/return.pdf
```

This will extract all fields, map them to canonical names, and save a clean JSON file to `output/extracted_{filename}.json` ready to be consumed by `smsf-collective`.

---

## Repository Structure

```
document-training/
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── config/
│   └── fields.json          # Canonical field name definitions
├── training/
│   └── README.md            # Labelling instructions
├── scripts/
│   ├── train_model.py
│   ├── test_model.py
│   └── extract_to_json.py
└── output/
    └── .gitkeep
```

---

## Field Reference

All field names are documented in [`config/fields.json`](config/fields.json), grouped by section:

- **Section A** – Fund Information
- **Section B** – Income
- **Section C** – Deductions
- **Section D** – Tax Calculation Statement
- **Section E** – Losses
- **Section F** – Member Information
- **Section H** – Assets and Liabilities
- **Section I** – Taxation of Financial Arrangements (TOFA)
- **Section J** – Other Information
- **Section K** – Declarations
