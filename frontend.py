import streamlit as st
import requests

API_URL = "http://backend:8001/query"


st.title("🧠 Mental Health Assistant")

query = st.text_area("Ask your question")

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        try:
            r = requests.post(API_URL, json={"query": query}, timeout=60)
            if r.status_code == 200:
                st.write(r.json().get("answer"))
            else:
                st.error(r.text)
        except Exception as e:
            st.error(str(e))
