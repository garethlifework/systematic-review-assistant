from __future__ import annotations

from typing import Any


def build_pubmed_query(
    keywords: list[str],
    inclusion_criteria: dict[str, Any],
    exclusion_criteria: dict[str, Any],
    additional_filters: dict[str, Any] | None = None,
) -> str:
    """Constructs a PubMed-compatible query string from user-defined keywords and criteria.

    Args:
        keywords (list): A list of keyword strings.
        inclusion_criteria (dict): Key-value pairs describing required conditions.
        exclusion_criteria (dict): Key-value pairs describing excluded conditions.
        additional_filters (dict): Any other PubMed-specific filters (e.g. publication date).

    Returns:
        str: PubMed query string ready for E-utilities.
    """
    # Basic example: combine all keywords with OR logic, then wrap with parentheses
    # and combine them with AND for mandatory terms from inclusion_criteria, etc.

    # 1) Combine keywords
    if not keywords:
        msg = "At least one keyword is required"
        raise ValueError(msg)

    keyword_query = " OR ".join([f"({kw})" for kw in keywords])

    # 2) Incorporate inclusion criteria
    # For example, if inclusion_criteria has "language: english", "study_type: clinical_trial", etc.
    # You might transform them into specific PubMed tags: e.g., "clinical trial[pt]" for publication type
    # This is highly dependent on your mapping conventions.

    inclusion_query_parts = []
    for key, val in inclusion_criteria.items():
        # Example placeholder. You'd adapt to real param/values:
        if key == "language":
            # e.g. English => "english[lang]"
            inclusion_query_parts.append(f"{val}[lang]")
        elif key == "study_type":
            # e.g. clinical trial => "clinical trial[pt]"
            inclusion_query_parts.append(f"{val}[pt]")
        # Add more logic as needed

    inclusion_query = " AND ".join(inclusion_query_parts)

    # 3) Exclusion criteria
    # Similar logic; just use NOT. For instance, if "exclusion_criteria" has "reviews"
    # we'd do something like NOT "review[pt]"
    exclusion_query_parts = []
    for key, val in exclusion_criteria.items():
        if key == "exclude_study_type":
            exclusion_query_parts.append(f"NOT {val}[pt]")
        # expand as needed

    exclusion_query = " AND ".join(exclusion_query_parts)

    # 4) Additional filters, e.g. date range: "2020:2023[dp]"
    filter_query_parts = []
    if additional_filters:
        pub_date_range = additional_filters.get("date_range")
        if pub_date_range:
            # Example: '2020:2023' => "2020:2023[dp]"
            filter_query_parts.append(f"{pub_date_range}[dp]")
        # Add more as needed (journal filters, etc.)

    filter_query = " AND ".join(filter_query_parts)

    # Combine everything
    combined_query = keyword_query
    if inclusion_query:
        combined_query += f" AND {inclusion_query}"
    if exclusion_query:
        combined_query += f" AND {exclusion_query}"
    if filter_query:
        combined_query += f" AND {filter_query}"

    # Clean up or handle edge cases
    return combined_query.strip()
