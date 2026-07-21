from markitdown import MarkItDown
from streamlit.runtime.uploaded_file_manager import UploadedFile

def extract_pdf_text(cv_pdf: UploadedFile) -> str:
    """Extracts CV in PDF format as a text in markdown style"""

    md = MarkItDown()
    result = md.convert(cv_pdf)

    return result.markdown