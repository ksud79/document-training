# from fillpdf import fillpdfs

# fields = fillpdfs.get_form_fields('SMSFAR 2024.pdf')

# for field, value in fields.items():
#     print(field)

import pymupdf

doc = pymupdf.open('SMSFAR 2024.pdf')

for page_num, page in enumerate(doc):
    widgets = page.widgets()
    if widgets:
        for widget in widgets:
            print(f"Page {page_num + 1}: {widget.field_name} ({widget.field_type_string})")
    else:
        print(f"Page {page_num + 1}: no fields")

