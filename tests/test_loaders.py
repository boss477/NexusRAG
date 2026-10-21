from pathlib import Path

import pytest

from app.ingestion.loaders import load_document
from app.schemas.documents import Modality


def test_text_loader_emits_canonical_chunks(tmp_path: Path) -> None:
    path = tmp_path / "notes.md"
    path.write_text("alpha beta gamma", encoding="utf-8")

    document, chunks = load_document(path, max_chars=6)

    assert document.modality == Modality.TEXT
    assert document.checksum
    assert [chunk.ordinal for chunk in chunks] == list(range(len(chunks)))
    assert all(chunk.document_id == document.document_id for chunk in chunks)


def test_loader_rejects_unknown_extension(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text("a,b", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported document extension"):
        load_document(path)


def test_loader_requires_existing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_document(tmp_path / "missing.txt")

