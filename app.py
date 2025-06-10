import streamlit as st
from agents.log_agent import LogAgent

st.set_page_config(page_title="Log Analyzer Agent", layout="centered")

st.title("🛠️ Log Analyzer Agent")
st.markdown("Analyzes your logs and suggests fixes based on Python code and DB schema.")

# Input prompt for user
user_prompt = st.text_area("💬 Custom Prompt (optional)", 
                           placeholder="e.g., Why is my Flask app throwing a 500 error?")

if st.button("Run Agent"):
    st.info("Running the log analysis agent... please wait.")

    # Initialize and run the Crew agent
    agent = LogAgent()
    result = agent.run(user_prompt=user_prompt.strip())

    st.success("✅ Analysis complete!")
    st.subheader("💡 Suggested Fix:")
    st.code(result, language="text")
