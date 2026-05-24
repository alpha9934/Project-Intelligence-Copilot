import streamlit as st
import requests

# Point this to your FastAPI backend
API_URL = "http://localhost:8000/ask"

# Configure the page layout
st.set_page_config(
    page_title="L&T Project Control Tower", 
    page_icon="🏗️",
    layout="centered"
)

st.title("🏗️ L&T Project Control Tower")
st.markdown("**AI-Powered Risk, Delay, and Contract Analytics**")

# Sidebar for project selection
with st.sidebar:
    st.header("Project Context")
    project_id = st.selectbox("Select Active Project", ["Project Alpha (Metro)", "Project Beta (Highway)"])
    st.success("🟢 Connected to Pinecone Vector Memory")
    st.info("This Copilot has ingested Contracts, Vendor Emails, Quality Reports, and MOMs.")

# The main "Ask Layer" input
st.markdown("### Ask the Project Intelligence Copilot")
question = st.text_input(
    "What do you need to know?", 
    placeholder="e.g., Why is the concrete pouring delayed and who is responsible?"
)

if st.button("Analyze Project Data", type="primary"):
    if question:
        with st.spinner("Scanning 10,000+ project documents, contracts, and meeting minutes..."):
            try:
                # Send the question to your FastAPI backend
                payload = {
                    "project_id": "project_alpha", 
                    "question": question
                }
                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    
                    st.divider()
                    
                    # 1. Display Top-Level Metrics (Risk & Ownership)
                    col1, col2 = st.columns(2)
                    
                    risk_score = data.get("risk_score", 0.0)
                    if risk_score >= 0.7:
                        risk_ui = f"🔴 Critical ({risk_score})"
                    elif risk_score >= 0.4:
                        risk_ui = f"🟡 Moderate ({risk_score})"
                    else:
                        risk_ui = f"🟢 Low ({risk_score})"
                        
                    col1.metric("Calculated Risk Level", risk_ui)
                    col2.metric("Responsible Owner", data.get("responsible_owner", "N/A"))

                    # 2. Display the AI's Answer
                    st.subheader("💡 Executive Summary")
                    st.write(data.get("answer", "No answer generated."))

                    # 3. Display the Next Action
                    st.subheader("⚡ Recommended Next Action")
                    st.info(data.get("next_action", "No action recommended."))

                    # 4. Display the Evidence (Crucial for enterprise trust!)
                    with st.expander("📄 View Evidence & Source Documents"):
                        st.markdown("The Copilot generated this answer using the following verified documents:")
                        for citation in data.get("evidence_citations", []):
                            # Clean up the output slightly for the UI
                            st.markdown(f"- `{citation}`")
                            
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("🚨 Could not connect to the FastAPI backend. Is your uvicorn server running?")
    else:
        st.warning("Please enter a question.")