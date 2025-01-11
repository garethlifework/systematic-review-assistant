"""Tests for llama_index_integration module."""

from __future__ import annotations

from pathlib import Path

import pytest
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.schema import TextNode

from step2.llama_index_integration import (
    build_llama_index_from_pubmed,
    pubmed_records_to_textnodes,
)


@pytest.fixture
def test_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for tests."""
    return tmp_path / "test_pubmed_index"
    # Clean up is handled automatically by pytest's tmp_path


@pytest.mark.integration
def test_pubmed_records_to_textnodes() -> None:
    # Test data
    pubmed_records = [
        {
            "MedlineCitation": {
                "PMID": "123456",
                "Article": {
                    "ArticleTitle": "Sample Title",
                    "Abstract": {"AbstractText": ["This is a sample abstract."]},
                },
            }
        }
    ]

    # Test document creation
    documents = pubmed_records_to_textnodes(pubmed_records)

    # Assertions
    assert len(documents) == 1
    assert isinstance(documents[0], TextNode)
    assert (
        documents[0].text
        == "PMID: 123456\nTitle: Sample Title\nAbstract: This is a sample abstract."
    )


@pytest.mark.integration
def test_build_llama_index_from_pubmed(test_dir: Path) -> None:
    # Test data
    pubmed_records = [
        {
            "MedlineCitation": {
                "PMID": "123456",
                "Article": {
                    "ArticleTitle": "Test Title",
                    "Abstract": {"AbstractText": ["Test abstract"]},
                },
            }
        }
    ]

    # Test index creation
    index = build_llama_index_from_pubmed(pubmed_records, str(test_dir))

    # Assertions
    assert isinstance(index, VectorStoreIndex)
    assert Path.exists(test_dir)
