"""This type stub file was generated by pyright.
"""

from collections.abc import Awaitable, Callable, Hashable, Sequence
from typing import (
    Any,
    NamedTuple,
    Self,
    overload,
)

from langchain_core.runnables import Runnable
from langchain_core.runnables.base import RunnableLike
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.graph import Graph as DrawableGraph
from langgraph.constants import Send
from langgraph.pregel import Pregel
from langgraph.pregel.write import ChannelWrite
from langgraph.types import All, Checkpointer
from langgraph.utils.runnable import RunnableCallable

logger = ...

class NodeSpec(NamedTuple):
    runnable: Runnable
    metadata: dict[str, Any] | None = ...
    ends: tuple[str, ...] | None = ...

class Branch(NamedTuple):
    path: Runnable[Any, Hashable | list[Hashable]]
    ends: dict[Hashable, str] | None
    then: str | None = ...
    def run(
        self,
        writer: Callable[
            [Sequence[str | Send], RunnableConfig], ChannelWrite | None
        ],
        reader: Callable[[RunnableConfig], Any] | None = ...,
    ) -> RunnableCallable: ...

class Graph:
    def __init__(self) -> None: ...
    @overload
    def add_node(
        self, node: RunnableLike, *, metadata: dict[str, Any] | None = ...
    ) -> Self: ...
    @overload
    def add_node(
        self,
        node: str,
        action: RunnableLike,
        *,
        metadata: dict[str, Any] | None = ...,
    ) -> Self: ...
    def add_node(
        self,
        node: str | RunnableLike,
        action: RunnableLike | None = ...,
        *,
        metadata: dict[str, Any] | None = ...,
    ) -> Self: ...
    def add_edge(self, start_key: str, end_key: str) -> Self: ...
    def add_conditional_edges(
        self,
        source: str,
        path: Callable[..., Hashable | list[Hashable]] | Callable[..., Awaitable[Hashable | list[Hashable]]] | Runnable[Any, Hashable | list[Hashable]],
        path_map: dict[Hashable, str] | list[str] | None = ...,
        then: str | None = ...,
    ) -> Self:
        """Add a conditional edge from the starting node to any number of destination nodes.

        Args:
            source (str): The starting node. This conditional edge will run when
                exiting this node.
            path (Union[Callable, Runnable]): The callable that determines the next
                node or nodes. If not specifying `path_map` it should return one or
                more nodes. If it returns END, the graph will stop execution.
            path_map (Optional[dict[Hashable, str]]): Optional mapping of paths to node
                names. If omitted the paths returned by `path` should be node names.
            then (Optional[str]): The name of a node to execute after the nodes
                selected by `path`.

        Returns:
            None

        Note: Without typehints on the `path` function's return value (e.g., `-> Literal["foo", "__end__"]:`)
            or a path_map, the graph visualization assumes the edge could transition to any node in the graph.

        """

    def set_entry_point(self, key: str) -> Self:
        """Specifies the first node to be called in the graph.

        Equivalent to calling `add_edge(START, key)`.

        Parameters:
            key (str): The key of the node to set as the entry point.

        Returns:
            None
        """

    def set_conditional_entry_point(
        self,
        path: Callable[..., Hashable | list[Hashable]] | Callable[..., Awaitable[Hashable | list[Hashable]]] | Runnable[Any, Hashable | list[Hashable]],
        path_map: dict[Hashable, str] | list[str] | None = ...,
        then: str | None = ...,
    ) -> Self:
        """Sets a conditional entry point in the graph.

        Args:
            path (Union[Callable, Runnable]): The callable that determines the next
                node or nodes. If not specifying `path_map` it should return one or
                more nodes. If it returns END, the graph will stop execution.
            path_map (Optional[dict[str, str]]): Optional mapping of paths to node
                names. If omitted the paths returned by `path` should be node names.
            then (Optional[str]): The name of a node to execute after the nodes
                selected by `path`.

        Returns:
            None
        """

    def set_finish_point(self, key: str) -> Self:
        """Marks a node as a finish point of the graph.

        If the graph reaches this node, it will cease execution.

        Parameters:
            key (str): The key of the node to set as the finish point.

        Returns:
            None
        """

    def validate(self, interrupt: Sequence[str] | None = ...) -> Self: ...
    def compile(
        self,
        checkpointer: Checkpointer = ...,
        interrupt_before: All | list[str] | None = ...,
        interrupt_after: All | list[str] | None = ...,
        debug: bool = ...,
    ) -> CompiledGraph: ...

class CompiledGraph(Pregel):
    builder: Graph
    def __init__(self, *, builder: Graph, **kwargs: Any) -> None: ...
    def attach_node(self, key: str, node: NodeSpec) -> None: ...
    def attach_edge(self, start: str, end: str) -> None: ...
    def attach_branch(self, start: str, name: str, branch: Branch) -> None: ...
    async def aget_graph(
        self, config: RunnableConfig | None = ..., *, xray: int | bool = ...
    ) -> DrawableGraph: ...
    def get_graph(
        self, config: RunnableConfig | None = ..., *, xray: int | bool = ...
    ) -> DrawableGraph:
        """Returns a drawable representation of the computation graph."""
