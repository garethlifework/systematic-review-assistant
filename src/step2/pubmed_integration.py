from __future__ import annotations

import os
from typing import Any, cast

from Bio import Entrez
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Get credentials from .env file
email = os.getenv("NCBI_EMAIL")
api_key = os.getenv("NCBI_API_KEY")

if email is None or api_key is None:
    msg = "Missing NCBI_EMAIL or NCBI_API_KEY in .env file"
    raise ValueError(msg)

# Type ignore for Entrez attributes which are dynamically set
Entrez.email = email  # type: ignore
Entrez.api_key = api_key  # type: ignore


def pubmed_search(query: str, max_results: int = 1000) -> list[str]:
    """Searches PubMed with the given query and returns a list of PMIDs."""
    try:
        # Type ignore for untyped Entrez functions
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)  # type: ignore
        record = Entrez.read(handle)  # type: ignore
        handle.close()
        pmid_list = record.get("IdList", [])  # type: ignore

        if not pmid_list:
            msg = "No results found for query: {!r}"
            logger.warning(msg, query)

        return cast(list[str], pmid_list)

    except Exception as e:
        msg = f"PubMed search failed: {e!s}"
        logger.opt(exception=True).error(msg)
        raise


def pubmed_fetch_details(pmids: list[str]) -> dict[str, Any]:
    """Fetches article details for each PMID using EFetch."""
    if not pmids:
        msg = "No PMIDs provided"
        raise ValueError(msg)

    try:
        # Process PMIDs in batches to avoid overwhelming the server
        batch_size = 100
        all_records = {}

        for i in range(0, len(pmids), batch_size):
            batch_ids = ",".join(pmids[i : i + batch_size])

            # Type ignore for untyped Entrez functions
            handle = Entrez.efetch(db="pubmed", id=batch_ids, retmode="xml")  # type: ignore
            records = Entrez.read(handle)  # type: ignore
            handle.close()

            # Add records to the collection
            if isinstance(records, dict):
                all_records.update(records)
            else:
                all_records.update(
                    {str(i): record for i, record in enumerate(records, start=i)}  # type: ignore
                )

        return all_records

    except Exception as e:
        msg = f"Failed to fetch PubMed details: {e!s}"
        logger.opt(exception=True).error(msg)
        raise


def extract_article_info(article: dict[str, Any]) -> dict[str, str]:
    """Extracts key information from a PubMed article record."""
    try:
        medline = article["MedlineCitation"]
        article_info = medline["Article"]

        # Handle PMID correctly (it's a string element)
        pmid = str(medline["PMID"])

        # Handle abstract (might be a list of StringElements)
        abstract_text = article_info.get("Abstract", {}).get(
            "AbstractText", ["No abstract"]
        )
        if isinstance(abstract_text, list):
            abstract = " ".join(str(text) for text in abstract_text)
        else:
            abstract = str(abstract_text)

        return {
            "pmid": pmid,
            "title": str(article_info.get("ArticleTitle", "No title")),
            "abstract": abstract,
            "journal": str(article_info.get("Journal", {}).get("Title", "No journal")),
            "year": str(
                article_info.get("Journal", {})
                .get("JournalIssue", {})
                .get("PubDate", {})
                .get("Year", "No year")
            ),
        }

    except KeyError:
        msg = "Could not extract article information"
        logger.opt(exception=True).error(msg)
        raise
