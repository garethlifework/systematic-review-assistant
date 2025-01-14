"""This type stub file was generated by pyright.
"""

from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import Any, Literal

from langchain_core.runnables.config import RunnableConfig
from langgraph.channels.base import BaseChannel
from langgraph.checkpoint.base import Checkpoint, CheckpointMetadata, PendingWrite
from langgraph.types import PregelExecutableTask, PregelTask, StateSnapshot
from typing_extensions import TypedDict

class TaskPayload(TypedDict):
    id: str
    name: str
    input: Any
    triggers: list[str]

class TaskResultPayload(TypedDict):
    id: str
    name: str
    error: str | None
    interrupts: list[dict]
    result: list[tuple[str, Any]]

class CheckpointTask(TypedDict):
    id: str
    name: str
    error: str | None
    interrupts: list[dict]
    state: RunnableConfig | None

class CheckpointPayload(TypedDict):
    config: RunnableConfig | None
    metadata: CheckpointMetadata
    values: dict[str, Any]
    next: list[str]
    parent_config: RunnableConfig | None
    tasks: list[CheckpointTask]

class DebugOutputBase(TypedDict):
    timestamp: str
    step: int

class DebugOutputTask(DebugOutputBase):
    type: Literal["task"]
    payload: TaskPayload

class DebugOutputTaskResult(DebugOutputBase):
    type: Literal["task_result"]
    payload: TaskResultPayload

class DebugOutputCheckpoint(DebugOutputBase):
    type: Literal["checkpoint"]
    payload: CheckpointPayload

type DebugOutput = DebugOutputTask | DebugOutputTaskResult | DebugOutputCheckpoint
TASK_NAMESPACE = ...

def map_debug_tasks(
    step: int, tasks: Iterable[PregelExecutableTask]
) -> Iterator[DebugOutputTask]:
    """Produce "task" events for stream_mode=debug."""

def map_debug_task_results(
    step: int,
    task_tup: tuple[PregelExecutableTask, Sequence[tuple[str, Any]]],
    stream_keys: str | Sequence[str],
) -> Iterator[DebugOutputTaskResult]:
    """Produce "task_result" events for stream_mode=debug."""

def map_debug_checkpoint(
    step: int,
    config: RunnableConfig,
    channels: Mapping[str, BaseChannel],
    stream_channels: str | Sequence[str],
    metadata: CheckpointMetadata,
    checkpoint: Checkpoint,
    tasks: Iterable[PregelExecutableTask],
    pending_writes: list[PendingWrite],
    parent_config: RunnableConfig | None,
    output_keys: str | Sequence[str],
) -> Iterator[DebugOutputCheckpoint]:
    """Produce "checkpoint" events for stream_mode=debug."""

def print_step_tasks(step: int, next_tasks: list[PregelExecutableTask]) -> None: ...
def print_step_writes(
    step: int, writes: Sequence[tuple[str, Any]], whitelist: Sequence[str]
) -> None: ...
def print_step_checkpoint(
    metadata: CheckpointMetadata,
    channels: Mapping[str, BaseChannel],
    whitelist: Sequence[str],
) -> None: ...
def tasks_w_writes(
    tasks: Iterable[PregelTask | PregelExecutableTask],
    pending_writes: list[PendingWrite] | None,
    states: dict[str, RunnableConfig | StateSnapshot] | None,
    output_keys: str | Sequence[str],
) -> tuple[PregelTask, ...]:
    """Apply writes / subgraph states to tasks to be returned in a StateSnapshot."""
