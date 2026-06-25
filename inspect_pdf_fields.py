import pymupdf  # PyMuPDF

def inspect_pdf_fields(pdf_path):
    doc = pymupdf.open(pdf_path)
    print(f"PDF: {pdf_path}")
    print(f"Pages: {doc.page_count}\n")
    
    all_fields = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        widgets = page.widgets()
        if widgets:
            print(f"--- Page {page_num + 1} ---")
            for widget in widgets:
                field_info = {
                    "page": page_num + 1,
                    "name": widget.field_name,
                    "type": widget.field_type_string,
                    "value": widget.field_value,
                    "rect": widget.rect,
                }
                all_fields.append(field_info)
                print(f"  Field: '{widget.field_name}'")
                print(f"    Type:  {widget.field_type_string}")
                print(f"    Value: {widget.field_value}")
                print(f"    Rect:  {widget.rect}")
    
    print(f"\nTotal fields found: {len(all_fields)}")
    return all_fields

# Run it — adjust path to your PDF
fields = inspect_pdf_fields(r"C:\Users\kevin\smsf-pdf-tools\SMSFAR 2024-smart form.pdf")