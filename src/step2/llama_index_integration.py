# llama_index_integration.py
from __future__ import annotations

import sys
from typing import Any

from llama_index.core.indices import VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.core.storage.storage_context import StorageContext
from loguru import logger

logger.remove(0)
logger.add(sys.stderr, format="{time:YYYY-MM-DD at HH:mm:ss!UTC} | {level} | {message}")


def pubmed_records_to_textnodes(pubmed_records: list[dict[str, Any]]) -> list[TextNode]:
    """Converts BioPython PubMed records into LlamaIndex Documents.

    Each record can contain multiple 'PubmedArticle' or 'PubmedBookArticle' items.
    """
    text_nodes = []
    for record in pubmed_records:
        try:
            medline_citation = record.get("MedlineCitation", {})
            article = medline_citation.get("Article", {})

            pmid = medline_citation.get("PMID", "No PMID")
            title = article.get("ArticleTitle", "No Title")

            # Handle potentially missing abstract
            abstract = "No Abstract Available"
            if "Abstract" in article and "AbstractText" in article["Abstract"]:
                abstract_text = article["Abstract"]["AbstractText"]
                if isinstance(abstract_text, list) and abstract_text:
                    abstract = abstract_text[0]
                elif isinstance(abstract_text, str):
                    abstract = abstract_text

            content = f"PMID: {pmid}\nTitle: {title}\nAbstract: {abstract}"
            doc = TextNode(text=content)
            text_nodes.append(doc)
        except Exception as e:
            logger.warning(f"Error processing record: {e}")
            continue

    return text_nodes


def build_llama_index_from_pubmed(
    pubmed_records: list[dict[str, Any]], index_path: str, settings: Any = None
) -> VectorStoreIndex | None:
    """Given a list of BioPython PubMed records, build and save a VectorStoreIndex.

    Args:
        pubmed_records (list): List of PubMed records
        index_path (str): Path to save the index
        settings (Settings, optional): LlamaIndex settings configuration

    Returns:
        VectorStoreIndex or None: The created index, or None if no documents were processed
    """
    text_nodes = pubmed_records_to_textnodes(pubmed_records)
    if not text_nodes:
        logger.warning("No documents were created from the PubMed records")
        return None

    try:
        # Create a storage context for persistence
        storage_context = StorageContext.from_defaults()

        # Create the index with storage context
        index = VectorStoreIndex(
            text_nodes,
            settings=settings,
            storage_context=storage_context,
            show_progress=True,
        )

        # Persist the index
        storage_context.persist(persist_dir=index_path)
        return index

    except Exception as e:
        logger.opt(exception=True).error("Error building index: {}", e)
        return None


# Add this if you want to test the file directly
if __name__ == "__main__":
    # Example usage
    test_record = {
        "MedlineCitation": {
            "PMID": "12345",
            "Article": {
                "ArticleTitle": "Test Title",
                "Abstract": {"AbstractText": ["This is a test abstract"]},
            },
        }
    }

    docs = pubmed_records_to_textnodes([test_record])
    logger.info("Test document created:")
    logger.info("Document text: {!r}", docs[0].text)
