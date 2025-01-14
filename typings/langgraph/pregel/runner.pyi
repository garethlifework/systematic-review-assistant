"""This type stub file was generated by pyright.
"""

import asyncio
import concurrent.futures
from collections.abc import AsyncIterator, Callable, Iterable, Iterator, Sequence
from typing import (
    Any,
)

from langgraph.pregel.algo import Call
from langgraph.pregel.executor import Submit
from langgraph.types import PregelExecutableTask, RetryPolicy

class PregelRunner:
    """Responsible for executing a set of Pregel tasks concurrently, committing
    their writes, yielding control to caller when there is output to emit, and
    interrupting other tasks if appropriate.
    """
    def __init__(
        self,
        *,
        submit: Submit,
        put_writes: Callable[[str, Sequence[tuple[str, Any]]], None],
        schedule_task: Callable[
            [PregelExecutableTask, int, Call | None], PregelExecutableTask | None
        ],
        use_astream: bool = ...,
        node_finished: Callable[[str], None] | None = ...,
    ) -> None: ...
    def tick(
        self,
        tasks: Iterable[PregelExecutableTask],
        *,
        reraise: bool = ...,
        timeout: float | None = ...,
        retry_policy: RetryPolicy | None = ...,
        get_waiter: Callable[[], concurrent.futures.Future[None]] | None = ...,
    ) -> Iterator[None]: ...
    async def atick(
        self,
        tasks: Iterable[PregelExecutableTask],
        *,
        reraise: bool = ...,
        timeout: float | None = ...,
        retry_policy: RetryPolicy | None = ...,
        get_waiter: Callable[[], asyncio.Future[None]] | None = ...,
    ) -> AsyncIterator[None]: ...
    def commit(
        self,
        task: PregelExecutableTask,
        fut: None | concurrent.futures.Future[Any] | asyncio.Future[Any],
        exception: BaseException | None = ...,
    ) -> None: ...
