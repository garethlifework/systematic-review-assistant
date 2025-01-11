from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import cast

import streamlit as st
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig

from step1.suggestion_agent import ReviewCriteria, SuggestionAgent

# Load environment variables from .env if present
load_dotenv()


def init_agent_config() -> RunnableConfig:
    if "agent_config" in st.session_state:
        return cast(RunnableConfig, st.session_state.agent_config)

    config = RunnableConfig(
        recursion_limit=1000, configurable={"thread_id": str(uuid.uuid4().hex)}
    )
    st.session_state.agent_config = config
    return config


def init_suggestion_agent() -> SuggestionAgent:
    """Initialize the suggestion agent."""
    return SuggestionAgent(model="gpt-4o", temperature=0.0)


# Set up page
st.set_page_config(page_title="AI-Assisted Systematic Review - Step 1", layout="wide")
st.title("Step 1: Define Research Question & Criteria")

# Initialize session state variables
if "research_question" not in st.session_state:
    st.session_state["research_question"] = ""
if "inclusion_criteria" not in st.session_state:
    st.session_state["inclusion_criteria"] = ""
if "exclusion_criteria" not in st.session_state:
    st.session_state["exclusion_criteria"] = ""
if "llm_suggestions" not in st.session_state:
    st.session_state["llm_suggestions"] = ""
if "suggestions_agent" not in st.session_state:
    st.session_state["suggestions_agent"] = init_suggestion_agent()

# Layout for input fields and LLM feedback
col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter Your Criteria")
    st.session_state["research_question"] = st.text_area(
        "Research Question",
        st.session_state["research_question"],
        placeholder="E.g. 'Does intervention X improve outcome Y in population Z?'",
    )
    st.session_state["inclusion_criteria"] = st.text_area(
        "Inclusion Criteria",
        st.session_state["inclusion_criteria"],
        placeholder="E.g. Adults >18, Intervention X, Outcome Y, RCTs, English",
    )
    st.session_state["exclusion_criteria"] = st.text_area(
        "Exclusion Criteria",
        st.session_state["exclusion_criteria"],
        placeholder="E.g. Children <18, Non-human studies, Case reports",
    )

    validate_button = st.button("Validate & Suggest Improvements")

with col2:
    st.subheader("LLM Suggestions")
    if st.session_state["llm_suggestions"]:
        st.markdown(st.session_state["llm_suggestions"])
    else:
        st.write("No suggestions yet. Click the 'Validate' button to get feedback.")

# LLM Interaction
if validate_button:
    criteria = ReviewCriteria(
        research_question=st.session_state["research_question"],
        inclusion_criteria=st.session_state["inclusion_criteria"],
        exclusion_criteria=st.session_state["exclusion_criteria"],
    )
    st.session_state["llm_suggestions"] = st.session_state[
        "suggestions_agent"
    ].get_suggestions(criteria)
    st.rerun()

st.subheader("Finalize & Save")
st.write("Once you are happy with the criteria, click the 'Save Criteria' button.")

save_button = st.button("Save Criteria")
if save_button:
    criteria_data = {
        "research_question": st.session_state["research_question"],
        "inclusion_criteria": st.session_state["inclusion_criteria"],
        "exclusion_criteria": st.session_state["exclusion_criteria"],
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }

    # Create directories if they don't exist
    Path("criteria").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)

    filename = f"criteria/criteria_{datetime.now(tz=timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(criteria_data, f, indent=2)

    # Log the event
    with open("logs/criteria_setup_log.txt", "a") as log_file:
        log_file.write(f"---\n{datetime.datetime.now().isoformat()}\n")
        log_file.write(f"Final Criteria:\n{json.dumps(criteria_data, indent=2)}\n")
        if st.session_state["llm_suggestions"]:
            log_file.write("LLM Suggestions:\n")
            log_file.write(st.session_state["llm_suggestions"] + "\n")

    st.success(f"Criteria saved to {filename}")
