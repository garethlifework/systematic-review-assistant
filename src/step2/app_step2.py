# app_step2.py
from __future__ import annotations

import streamlit as st
from llama_index_integration import build_llama_index_from_pubmed
from logger import log_pubmed_search
from pubmed_integration import pubmed_fetch_details, pubmed_search


def run_step2_search_and_index() -> None:
    st.title("Step 2: Automated PubMed Query & Indexing (BioPython)")

    # Retrieve the search criteria from Step 1 (if stored in session state)
    if "research_criteria" not in st.session_state:
        st.warning(
            "Please complete Step 1 first to define your research question/criteria."
        )
        return

    # For example, we might have:
    # st.session_state["research_criteria"] = {
    #   "keywords": ["lung cancer", "immunotherapy", "clinical trials"],
    #   "date_range": "2020:2023",
    #   ...
    # }

    # Let the user confirm or modify the query
    query_string = st.text_input(
        "Enter PubMed Query (Boolean syntax supported):",
        value="(lung cancer) AND (immunotherapy) AND (clinical trial)",
    )

    max_results = st.number_input("Max Results", value=500, min_value=1)

    if st.button("Run PubMed Search"):
        st.write(f"**Searching PubMed** with query: {query_string}")
        pmid_list = pubmed_search(query_string, max_results)

        # Log
        log_pubmed_search(query_string, pmid_list)

        if not pmid_list:
            st.warning("No PMIDs found. Try adjusting your query.")
            return

        st.success(f"Found {len(pmid_list)} PMIDs.")

        # Fetch details
        pubmed_records = pubmed_fetch_details(pmid_list)
        st.write(f"Fetched details for {len(pubmed_records)} records.")

        # Build LlamaIndex
        index = build_llama_index_from_pubmed(
            [pubmed_records], index_path="pubmed_index.json"
        )
        if index:
            st.success("LlamaIndex built and saved as pubmed_index.json.")
            # Store data in session for Step 3
            st.session_state["pubmed_records"] = pubmed_records
            st.session_state["pubmed_index_built"] = True


# If you want to run this directly:
if __name__ == "__main__":
    run_step2_search_and_index()
