import sqlite3

from app.retrieval import KeywordIndex
from app.schemas.documents import DocumentChunk, Modality
from uuid import uuid4


def test_keyword_index_incremental_search() -> None:
    index = KeywordIndex(sqlite3.connect(":memory:"))
    chunk = DocumentChunk(
        document_id=uuid4(), text="BM25 finds rare tokens like quokka",
        source="guide.txt", modality=Modality.TEXT, ordinal=0,
    )
    assert index.upsert([chunk]) == 1
    assert index.upsert([chunk]) == 1
    hits = index.search("quokka")
    assert len(hits) == 1
    assert hits[0].chunk.chunk_id == chunk.chunk_id
    assert hits[0].score > 0
    assert index.search("nonmatching") == []


def test_keyword_query_is_not_sql() -> None:
    index = KeywordIndex(sqlite3.connect(":memory:"))
    assert index.search("' OR 1=1 --") == []
