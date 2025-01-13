"""Core domain models."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Any, Literal

import uuid6
from pydantic import BaseModel, Field
from pydantic.types import StringConstraints

CriterionType = Literal["inclusion", "exclusion"]

ScreeningResult = Literal["include", "exclude", "uncertain"]


class Criterion(BaseModel):
    """A criterion for including or excluding a paper."""

    description: Annotated[str, StringConstraints(min_length=1)]
    type: CriterionType
    rationale: str | None = None


class ResearchQuestion(BaseModel):
    """The research question."""

    id: uuid6.UUID = Field(default_factory=uuid6.uuid7)
    question: Annotated[str, StringConstraints(min_length=1)]
    review_criteria: ReviewCriteria
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReviewCriteria(BaseModel):
    """The review criteria."""

    inclusion: list[Criterion] = Field(..., min_length=1)
    exclusion: list[Criterion] = Field(default=[], min_length=0)


class ScreeningDecision(BaseModel):
    """A decision made by a reviewer."""

    id: uuid6.UUID = Field(default_factory=uuid6.uuid7)
    srid: uuid6.UUID
    docid: uuid6.UUID | str | int
    result: ScreeningResult
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: list[str]
    model_id: str | None = Field(
        default=None,
        description="The ID of the model that made the decision",
        examples=["claude-3-5-sonnet-latest", "gpt-4o"],
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PaperMetadata(BaseModel):
    """Metadata for a paper."""

    pmid: str = Field(..., pattern=r"^\d{8}$")
    title: str
    abstract: str
    authors: list[str] | None = None
    publication_year: int = Field(gt=1900, lt=2100)
    journal: str
    mesh_terms: list[str] | None = None


# RAG Models
class SearchConfig(BaseModel):
    max_chunks: int = Field(default=5, gt=0)
    min_relevance: float = Field(default=0.7, ge=0.0, le=1.0)
    model_name: str = "BAAI/bge-large-en"


class ChunkMetadata(BaseModel):
    paper_id: str
    section: str
    section_level: int = Field(ge=0)
    chunk_index: int = Field(ge=0)
    token_count: int = Field(gt=0)
    embedding_model: str


class SearchResult(BaseModel):
    text: str
    section: str
    relevance: float = Field(ge=0.0, le=1.0)
    metadata: ChunkMetadata


# PRISMA Models
class PrismaSection(BaseModel):
    count: int = Field(ge=0)
    details: dict[str, int] = {}
    notes: str | None = None


class PrismaState(BaseModel):
    version: int = Field(ge=1)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    database_records: PrismaSection
    register_records: PrismaSection
    other_sources: PrismaSection
    duplicates: PrismaSection
    automated_exclusions: PrismaSection
    records_screened: PrismaSection
    records_excluded: PrismaSection
    full_text_assessed: PrismaSection
    studies_included: PrismaSection

    class Config:
        json_schema_extra = {
            "example": {
                "version": 1,
                "database_records": {
                    "count": 1200,
                    "details": {"PubMed": 800, "Scopus": 400},
                },
            }
        }


# Event Models
class ReviewEvent(BaseModel):
    event_type: str
    review_id: uuid6.UUID
    user_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: dict[str, Any] | None = None


class CriteriaUpdated(ReviewEvent):
    event_type: Literal["criteria_updated"] = "criteria_updated"
    data: dict[str, type[ReviewCriteria] | str] = {
        "old_criteria": ReviewCriteria,
        "new_criteria": ReviewCriteria,
        "reason": str,
    }


# Queue Job Models

JobType = Literal["chunk_embed", "index_update"]


class ProcessingJob(BaseModel):
    """Processing job."""

    pmid: str = Field(..., pattern=r"^\d{8}$")
    project_id: uuid6.UUID
    job_type: JobType
    payload: dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_schema_extra = {
            "example": {
                "paper_id": "PMC123456",
                "job_type": "chunk_embed",
                "priority": 1,
                "payload": {"model": "BAAI/bge-large-en", "chunk_size": 512},
            }
        }
