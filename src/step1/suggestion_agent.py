"""Suggestion agent for systematic review criteria."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import cast

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START
from langgraph.graph.message import MessagesState
from langgraph.graph.state import CompiledStateGraph, StateGraph
from loguru import logger


@dataclass
class ReviewCriteria:
    """Data class for systematic review criteria."""

    research_question: str
    inclusion_criteria: str
    exclusion_criteria: str

    def to_prompt(self) -> str:
        """Convert criteria to a prompt for the agent."""
        user_input_summary = f"""\
        Research Question: {self.research_question}
        Inclusion Criteria: {self.inclusion_criteria}
        Exclusion Criteria: {self.exclusion_criteria}
        """

        return f"""\
        The user provided the following systematic review setup:

        {user_input_summary}

        Please:
        1. Check if the criteria are clear and unambiguous.
        2. Suggest any improvements or additional details that might help during the screening process.
        3. Identify any contradictions or points needing clarification.
        """


class SuggestionAgent:
    """Agent for providing suggestions on systematic review criteria."""

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.0) -> None:
        """Initialize the agent with model configuration."""
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.workflow = self._create_workflow()
        self.memory = MemorySaver()
        self.agent = self._compile_agent()
        self.messages: list[BaseMessage] = []
        self.config = self._create_config()

    def _create_workflow(self) -> StateGraph:
        """Create the agent workflow."""
        workflow = StateGraph(state_schema=MessagesState)

        def call_model(state: MessagesState) -> dict[str, AIMessage]:
            """Call the model with the current state."""
            response = cast(AIMessage, self.llm.invoke(state["messages"]))
            return {"messages": response}

        workflow.add_node("model", call_model)
        workflow.add_edge(START, "model")
        return workflow

    def _compile_agent(self) -> CompiledStateGraph:
        """Compile the agent with memory."""
        return self.workflow.compile(checkpointer=self.memory)

    def _create_config(self) -> RunnableConfig:
        """Create agent configuration."""
        return RunnableConfig(
            recursion_limit=1000, configurable={"thread_id": str(uuid.uuid4().hex)}
        )

    def get_suggestions(self, criteria: ReviewCriteria) -> str:
        """Get suggestions for the given criteria."""
        # Create prompt from criteria
        prompt = criteria.to_prompt()

        # Add message to history
        self.messages.append(HumanMessage(content=prompt))

        # Update agent state
        state = {"messages": self.messages}
        result = self.agent.invoke(state, config=self.config)

        # Store response
        ai_message = result["messages"][-1]
        if isinstance(ai_message, AIMessage):
            self.messages.append(ai_message)
            return cast(str, ai_message.content)
        msg = "Unexpected message type: {!r}"
        logger.error(msg, type(ai_message))
        raise ValueError(msg.format(type(ai_message)))

    def get_message_history(self) -> list[BaseMessage]:
        """Get the full message history."""
        return self.messages.copy()

    def clear_history(self) -> None:
        """Clear the message history."""
        self.messages = []
