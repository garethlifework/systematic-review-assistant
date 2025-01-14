"""This type stub file was generated by pyright.
"""

from typing import Any

from langgraph.types import PregelExecutableTask, RetryPolicy

logger = ...
SUPPORTS_EXC_NOTES = ...

def run_with_retry(
    task: PregelExecutableTask,
    retry_policy: RetryPolicy | None,
    configurable: dict[str, Any] | None = ...,
) -> None:
    """Run a task with retries."""

async def arun_with_retry(
    task: PregelExecutableTask,
    retry_policy: RetryPolicy | None,
    stream: bool = ...,
    configurable: dict[str, Any] | None = ...,
) -> None:
    """Run a task asynchronously with retries."""
