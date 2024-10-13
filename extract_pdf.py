import pdfplumber

def extract_text_from_pdf(path, max_pages=None):
	with pdfplumber.open(path) as pdf:
		text = ''
		for page in pdf.pages[:min(max_pages, len(pdf.pages))]:
			text += page.extract_text().encode('utf-8', errors='replace').decode('utf-8')

	return text
