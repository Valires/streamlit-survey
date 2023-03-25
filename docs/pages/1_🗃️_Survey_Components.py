import streamlit as st

import streamlit_survey as ss

st.set_page_config(
    page_title="Streamlit Survey Components",
    page_icon="🗃️",
)

"""
# Streamlit Survey Components

This page gives examples of the survey components available in the `streamlit_survey` package. The survey components are used to create surveys and collect data from users. They are similar to the Streamlit inputs, but they have additional features that make them suitable for surveys.
"""

"""
### StreamlitSurvey Class

The `StreamlitSurvey` class is the main entry point for survey components. It is used to create and manage survey components, store their state, and save the survey data to a JSON file.
"""
with st.echo(code_location="below"):
    survey = ss.StreamlitSurvey("Survey Example")

"""
Most Streamlit inputs have corresponding survey elements. For example, the `st.text_input` function has a corresponding `survey.text_input` function. The survey elements are used in the same way as the Streamlit inputs, but they have an additional `id` parameter. The `id` parameter is used to identify the survey element and store its state. If the `id` parameter is not specified, the survey element will be assigned a unique ID automatically.

Survey objects can be saved to and loaded from JSON files using the `to_json` and `from_json` methods. They store the survey component labels and values in a dictionary, which can be used to resume a survey or to analyze the survey data.
"""

"""
### Radio Components
"""
with st.echo(code_location="below"):
    survey.radio("Thumbs up/down:", options=["NA", "👍", "👎"], horizontal=True)

with st.echo(code_location="below"):
    survey.radio("Likert scale:", options=["NA", "😞", "🙁", "😐", "🙂", "😀"], horizontal=True)

with st.echo(code_location="below"):
    survey.radio("Horizontal radio:", options=["Option 1", "Option 2", "Option 3", "etc"], horizontal=True)

with st.echo(code_location="below"):
    survey.radio("Vertical radio:", options=["Option 1", "Option 2", "Option 3", "etc"])

"""
### Selection Boxes
"""
with st.echo(code_location="below"):
    survey.selectbox("Selection box:", options=["Option 1", "Option 2", "Option 3", "etc"])

with st.echo(code_location="below"):
    survey.multiselect("Multiple choice:", options=["Option 1", "Option 2", "Option 3", "etc"])

"""
### Check Box
"""
with st.echo(code_location="below"):
    survey.checkbox("Check box")

"""
### Date and Time
"""
with st.echo(code_location="below"):
    survey.dateinput("Date input:")

with st.echo(code_location="below"):
    survey.timeinput("Time input:")

"""
### Text Input
"""
with st.echo(code_location="below"):
    survey.text_input("Text input:")

with st.echo(code_location="below"):
    survey.text_area("Area input:")

"""
### Numerical Input
"""
with st.echo(code_location="below"):
    st.number_input("Number input:", min_value=0, max_value=100, value=50)

with st.echo(code_location="below"):
    st.slider("Slider:", min_value=0, max_value=100, value=50)

"""
## Current Survey State:
"""
st.json(survey.to_json(), expanded=False)

"""
## Current Session State:
"""
st.json(st.session_state, expanded=False)
