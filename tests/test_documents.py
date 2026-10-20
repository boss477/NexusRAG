from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.documents import CitationLocation, Document, DocumentChunk, Modality


def test_document_chunk_preserves_citation_metadata() -> None:
    document = Document(source="report.pdf", modality=Modality.PDF)
    chunk = DocumentChunk(
        document_id=document.document_id,
        source=document.source,
        modality=document.modality,
        text="Revenue increased during the quarter.",
        ordinal=0,
        citation=CitationLocation(page=12),
    )
    assert chunk.citation.page == 12
    assert chunk.document_id == document.document_id


def test_chunk_rejects_empty_text() -> None:
    with pytest.raises(ValidationError):
        DocumentChunk(document_id=uuid4(), source="notes.txt", modality=Modality.TEXT, text="", ordinal=0)


def test_citation_rejects_reversed_timestamps() -> None:
    with pytest.raises(ValidationError):
        CitationLocation(start_second=20, end_second=10)

