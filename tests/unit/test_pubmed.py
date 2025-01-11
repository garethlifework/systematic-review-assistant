"""Tests for pubmed_integration module."""

from __future__ import annotations

import pytest

from step2.pubmed_integration import (
    extract_article_info,
    pubmed_fetch_details,
    pubmed_search,
)


@pytest.mark.integration
def test_pubmed_search() -> None:
    """Test PubMed search functionality."""
    query = "systematic review AND machine learning"
    pmids = pubmed_search(query, max_results=5)

    assert isinstance(pmids, list)
    assert len(pmids) <= 5
    assert all(isinstance(pmid, str) for pmid in pmids)


@pytest.mark.integration
def test_pubmed_fetch() -> None:
    """Test fetching article details."""
    # Use a small sample of PMIDs
    pmids = ["123456", "789012"]
    records = pubmed_fetch_details(pmids)

    assert isinstance(records, dict)
    assert "PubmedArticle" in records


@pytest.mark.integration
def test_extract_article_info() -> None:
    """Test article info extraction."""
    # Mock article data
    article = {
        "MedlineCitation": {
            "PMID": "123456",
            "Article": {
                "ArticleTitle": "Test Title",
                "Abstract": {"AbstractText": ["Test abstract"]},
                "Journal": {
                    "Title": "Test Journal",
                    "JournalIssue": {"PubDate": {"Year": "2023"}},
                },
            },
        }
    }

    info = extract_article_info(article)

    assert isinstance(info, dict)
    assert info["pmid"] == "123456"
    assert info["title"] == "Test Title"
    assert info["abstract"] == "Test abstract"
    assert info["journal"] == "Test Journal"
    assert info["year"] == "2023"


@pytest.mark.integration
def test_pubmed_error_handling() -> None:
    """Test error handling in PubMed functions."""
    with pytest.raises(ValueError):
        pubmed_fetch_details([])  # Empty PMID list should raise ValueError
