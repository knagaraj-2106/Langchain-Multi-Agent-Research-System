import os
import streamlit as st
from dotenv import load_dotenv

# 1. Load API keys silently from .env into environment variables
load_dotenv()

from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

# --- Page Configuration ---
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar: Architecture & Security Status ---
with st.sidebar:
    st.title("🤖 Agent Workflow")
    st.markdown(
        """
        This pipeline orchestrates **4 specialized AI nodes**:
        1. 🔍 **Search Agent** — Finds recent, reliable sources.
        2. 📖 **Reader Agent** — Scrapes deep content from top URLs.
        3. ✍️ **Writer Chain** — Synthesizes findings into a report.
        4. 🎯 **Critic Chain** — Reviews quality and provides feedback.
        """
    )
    st.divider()

    # Check if .env is loaded without ever showing the actual keys
    st.subheader("🔒 Security Status")
    env_loaded = any(
        key.endswith("_API_KEY") for key in os.environ.keys()
    )
    if env_loaded:
        st.success("API credentials loaded securely from environment.")
    else:
        st.warning("No *_API_KEY detected in environment. Check your .env file.")

    if st.button("🗑️ Clear Results", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- Main Header ---
st.title("🔬 Autonomous Multi-Agent Research System")
st.caption("Enter a research topic below to dispatch the Search, Reader, Writer, and Critic agents.")

# --- Input Form ---
with st.form("research_form"):
    col1, col2 = st.columns([5, 1])
    with col1:
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g., Recent advancements in Agentic RAG architectures...",
            label_visibility="collapsed",
        )
    with col2:
        submit_btn = st.form_submit_button("🚀 Run Research", use_container_width=True, type="primary")

# --- Pipeline Execution with Live Step-by-Step Progress ---
if submit_btn:
    if not topic.strip():
        st.error("Please enter a valid research topic before running.")
    else:
        state = {}

        with st.status("Executing Multi-Agent Research Pipeline...", expanded=True) as status:
            try:
                # Step 1: Search Agent
                st.write("🔍 **Step 1/4:** Search Agent is gathering recent, reliable sources...")
                search_agent = build_search_agent()
                search_result = search_agent.invoke({
                    "messages": [(
                        "user", f"Find the recent, reliable and detailed information about :{topic}"
                    )]
                })
                state["search_results"] = search_result["messages"][-1].content

                # Step 2: Reader Agent
                st.write("📖 **Step 2/4:** Reader Agent is scraping top resources for deeper context...")
                reader_agent = build_reader_agent()
                reader_result = reader_agent.invoke({
                    "messages": [(
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}"
                    )]
                })
                state["scraped_content"] = reader_result["messages"][-1].content

                # Step 3: Writer Chain
                st.write("✍️ **Step 3/4:** Writer Agent is drafting the comprehensive report...")
                research_combined = (
                    f"SEARCH RESULTS : \n {state['search_results']} \n\n"
                    f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
                )
                report_out = writer_chain.invoke({
                    "topic": topic,
                    "research": research_combined,
                })
                state["report"] = report_out.content if hasattr(report_out, "content") else str(report_out)

                # Step 4: Critic Chain
                st.write("🎯 **Step 4/4:** Critic Agent is reviewing and auditing the final report...")
                feedback_out = critic_chain.invoke({
                    "report": state["report"]
                })
                state["feedback"] = feedback_out.content if hasattr(feedback_out, "content") else str(feedback_out)

                # Save results in session_state so they persist when clicking Download
                st.session_state["research_state"] = state
                st.session_state["current_topic"] = topic

                status.update(label="✅ Research Pipeline Completed Successfully!", state="complete", expanded=False)

            except Exception as e:
                status.update(label="❌ Pipeline Failed", state="error", expanded=True)
                st.error(f"An error occurred during execution: {e}")

# --- Display Results ---
if "research_state" in st.session_state:
    res = st.session_state["research_state"]
    saved_topic = st.session_state.get("current_topic", "research")

    st.divider()

    tab_report, tab_critic, tab_scraped, tab_search = st.tabs([
        "📄 Final Report",
        "🎯 Critic Review",
        "📖 Scraped Content",
        "🔍 Raw Search Results",
    ])

    with tab_report:
        st.subheader(f"Research Report: {saved_topic}")
        st.markdown(res["report"])
        st.download_button(
            label="📥 Download Report (.md)",
            data=res["report"],
            file_name=f"{saved_topic.lower().replace(' ', '_')}_report.md",
            mime="text/markdown",
        )

    with tab_critic:
        st.subheader("Critic Agent Evaluation & Feedback")
        st.info(res["feedback"])

    with tab_scraped:
        st.subheader("Deep Scraped Source Content")
        st.markdown(res["scraped_content"])

    with tab_search:
        st.subheader("Initial Search Agent Findings")
        st.markdown(res["search_results"])