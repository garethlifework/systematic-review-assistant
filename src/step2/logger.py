# logger.py
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def log_pubmed_search(
    query_string: str, pmid_list: list[str], log_file: str = "search_log.json"
) -> None:
    record = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "query": query_string,
        "num_pmids": len(pmid_list),
        "pmids": pmid_list,
    }
    try:
        with Path(log_file).open("r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(record)

    with Path(log_file).open("w") as f:
        json.dump(data, f, indent=2)
