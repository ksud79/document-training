import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

html_content = """
<html>
<body>
    <h1>Test SMSF Form</h1>
    <p>TFN: 123 456 789</p>
    <p>Fund Name: Smith Family Super Fund</p>
</body>
</html>
"""

pdfkit.from_string(html_content, 'test_output.pdf', configuration=config)
print("PDF created successfully!")