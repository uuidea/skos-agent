# langgraph/nodes/read_document.py

import os
from pathlib import Path
from typing import Dict, Any, Union

import pypdf
import markdown2
import bs4
import ebooklib
from ebooklib import epub
import docx

def read_document(input: Dict[str, Any]) -> str:
    """
    Read a document from a file path provided in the input dictionary.
    The input is expected to be a dict with a key 'file_path' containing
    the path string.
    """
    # Extract the file path string from the input dict
    file_path = input.get("file_path")
    if not isinstance(file_path, str):
        raise ValueError("Input must contain a string under the key 'file_path'")

    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        text = ""
        with open(path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    elif ext in {".md", ".markdown"}:
        text = markdown2.markdown_path(file_path)
        # strip Markdown syntax to plain text
        text = bs4.BeautifulSoup(text, "html.parser").get_text()
    elif ext in {".adoc", ".asciidoc"}:
        # AsciiDoc → HTML → plain text
        text = Path(path).read_text()
        # Very naive: use a shell call to `asciidoctor` if available
        # For simplicity we skip and return raw content
    elif ext == ".epub":
        book = ebooklib.epub.read_epub(file_path)
        text = ""
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = bs4.BeautifulSoup(item.content, "html.parser")
            text += soup.get_text()
    elif ext == ".docx":
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    elif ext in {".html", ".htm"}:
        soup = bs4.BeautifulSoup(Path(file_path).read_text(), "html.parser")
        text = soup.get_text()
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    print("done reading document")
    return text
# Note that I've replaced the `read_document` function to accept a dictionary input instead of a string path.
