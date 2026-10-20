from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Modality(StrEnum):
    TEXT = "text"
    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    TABLE = "table"
    WEB = "web"


class CitationLocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int | None = Field(default=None, ge=1)
    start_second: float | None = Field(default=None, ge=0)
    end_second: float | None = Field(default=None, ge=0)
    bbox: tuple[float, float, float, float] | None = None

    @field_validator("end_second")
    @classmethod
    def end_after_start(cls, value: float | None, info):
        start = info.data.get("start_second")
        if value is not None and start is not None and value < start:
            raise ValueError("end_second must be greater than or equal to start_second")
        return value


class Document(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: UUID = Field(default_factory=uuid4)
    source: str = Field(min_length=1)
    modality: Modality
    title: str | None = None
    checksum: str | None = None
    ingested_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, str] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chunk_id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    text: str = Field(min_length=1)
    source: str = Field(min_length=1)
    modality: Modality
    ordinal: int = Field(ge=0)
    citation: CitationLocation = Field(default_factory=CitationLocation)
    metadata: dict[str, str] = Field(default_factory=dict)

