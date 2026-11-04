from io import BytesIO
from pypdf import PdfWriter

def test_resume_requires_auth(client):
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    data = BytesIO()
    writer.write(data)
    response = client.post('/api/resume/analyze', files={'file': ('resume.pdf', data.getvalue(), 'application/pdf')})
    assert response.status_code in (401, 403)

def test_resume_rejects_non_pdf(client):
    response = client.post('/api/resume/analyze', files={'file': ('resume.txt', b'hello', 'text/plain')})
    assert response.status_code in (401, 403, 415)
