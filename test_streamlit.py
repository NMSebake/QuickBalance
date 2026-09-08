import streamlit as st

st.set_page_config(
    page_title="Streamlit Test"
)

st.title("Streamlit Selectbox Test")

account = st.selectbox(
    "Select account",
    [
        "Cheque",
        "Savings",
        "Credit Card"
    ]
)

st.write(
    "Selected account:",
    account
)