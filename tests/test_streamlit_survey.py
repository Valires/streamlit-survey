#!/usr/bin/env python

"""Tests for `streamlit_survey` package."""

def test_streamlit_survey(response):
    import streamlit as st
    import streamlit_survey as ss

    st.write("## Welcome to Streamlit Survey")

    survey = ss.StreamlitSurvey()

    survey.thumbs("Thumbs:")
    survey.faces("Faces:")
    survey.text_input("Text input:")
    survey.text_area("Area input:")
    survey.multichoice(
        "Multiple choice:", options=["Option 1", "Option 2", "Option 3", "etc"]
    )
    survey.selectbox(
        "Select box:", options=["Option 1", "Option 2", "Option 3", "etc"]
    )
    survey.radio("Radio:", options=["Option 1", "Option 2", "Option 3", "etc"])
    survey.checkbox("Check box")
    survey.dateinput("Date input:")
    survey.timeinput("Time input:")

    st.write("### Current survey state:")
    st.json(survey.to_json())

    st.write("### Current session state:")
    st.json(st.session_state)

