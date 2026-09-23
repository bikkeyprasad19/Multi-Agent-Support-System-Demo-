import os
import streamlit as st
from google import genai
from google.genai import types
from tools import DATABASE, ESCALATION_QUEUE, EXECUTION_LOGS, lookup_order, issue_refund, escalate_to_human

st.set_page_config(page_title="AI Support Orchestrator", layout="wide")

st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col_chat, col_logs = st.columns([1, 1], gap="medium")

with col_logs:
    st.subheader("System Telemetry & Live Tools")
    tab_trace, tab_db, tab_handoff = st.tabs(["AI Tool Execution Trace", "Live Database", "Escalation Queue"])
    
    with tab_trace:
        if not EXECUTION_LOGS:
            st.info("AI reasoning and tool logs will appear here during execution.")
        for log in reversed(EXECUTION_LOGS):
            with st.expander(f"Tool Executed: `{log['name']}`", expanded=True):
                st.write("**Arguments Passed by AI:**", log["args"])
                st.write("**Tool Output / Action Taken:**", log["result"])

    with tab_db:
        st.json(DATABASE)

    with tab_handoff:
        if not ESCALATION_QUEUE:
            st.caption("No pending tickets.")
        for item in ESCALATION_QUEUE:
            st.error(f"Action Required: Ticket {item['ticket_id']}")
            st.json(item)

with col_chat:
    st.subheader("Customer Support Chat")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Enter your message (e.g. 'I was charged twice for ORD-101')")

    if user_query:
        if not api_key:
            st.error("Pehle sidebar me apni Gemini API Key paste karo!")
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            client = genai.Client(api_key=api_key)
            system_instruction = """
            You are an autonomous customer resolution AI.
            CRITICAL RULES:
            1. You MUST call `lookup_order` first whenever an order ID is given.
            2. If double-charged and refund <= RS 3500, you MUST call `issue_refund`.
            3. If refund > $50 OR the item is physically damaged/shattered, DO NOT refund. You MUST call `escalate_to_human`.
            """

            tool_functions = [lookup_order, issue_refund, escalate_to_human]

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_query,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=tool_functions,
                    temperature=0.1
                )
            )

            bot_reply = response.text if response.text else "Request processed successfully."
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            st.rerun()